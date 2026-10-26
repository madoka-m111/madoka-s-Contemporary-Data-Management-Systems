from typing import List, Optional, Dict, Any, Tuple
from bson import ObjectId
from app.models.question import Question
from app.models.survey import Survey
from app.services.validation_service import ValidationService
from app.services.jump_service import JumpService
from app import db


class QuestionService:
    @staticmethod
    def _questions_editable(survey: Survey) -> bool:
        """发布过的问卷题目视为不可变快照，撤回后也不能直接改题。"""
        return (
            survey.status == Survey.STATUS_DRAFT
            and not getattr(survey, 'published_at', None)
        )

    @staticmethod
    def add_question(survey_id: str, user_id: str, data: Dict) -> Tuple[Optional[Question], Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return None, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return None, '无权限添加题目'
        if not QuestionService._questions_editable(survey):
            return None, '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        order = data.get('order')
        if order is None:
            existing = Question.find_by_survey_id(survey_id)
            order = len(existing)

        question = Question(
            survey_id=ObjectId(survey_id),
            title=data['title'],
            q_type=data['type'],
            order=order,
            required=data.get('required', False),
            options=data.get('options', []),
            validation=data.get('validation', {}),
            jump_logic=data.get('jump_logic', {})
        )
        question.save()
        return question, None

    @staticmethod
    def batch_add_questions(survey_id: str, user_id: str, questions_data: List[Dict]) -> Tuple[List[Question], Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return [], '问卷不存在'
        if str(survey.creator_id) != user_id:
            return [], '无权限添加题目'
        if not QuestionService._questions_editable(survey):
            return [], '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        existing = Question.find_by_survey_id(survey_id)
        base_order = len(existing)

        questions = []
        for i, q_data in enumerate(questions_data):
            question = Question(
                survey_id=ObjectId(survey_id),
                title=q_data['title'],
                q_type=q_data['type'],
                order=base_order + i,
                required=q_data.get('required', False),
                options=q_data.get('options', []),
                validation=q_data.get('validation', {}),
                jump_logic=q_data.get('jump_logic', {})
            )
            question.save()
            questions.append(question)
        return questions, None

    @staticmethod
    def add_question_from_bank(survey_id: str, user_id: str, data: Dict) -> Tuple[Optional[Question], Optional[str]]:
        from app.services.question_bank_service import QuestionBankService
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return None, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return None, '无权限添加题目'
        if not QuestionService._questions_editable(survey):
            return None, '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        version_id = data.get('bank_question_id') or data.get('version_id') or data.get('question_id')
        if not version_id:
            return None, '缺少题库题目版本 ID'
        version = QuestionBankService._get_version(version_id)
        if not version:
            return None, '题库题目版本不存在'
        family = QuestionBankService._get_family(version.family_id)
        if not family or not QuestionBankService.can_view(family, user_id):
            return None, '无权使用该题库题目'

        order = data.get('order')
        if order is None:
            order = len(Question.find_by_survey_id(survey_id))
        question = Question(
            survey_id=ObjectId(survey_id),
            title=data.get('title') or version.title,
            q_type=version.type,
            order=order,
            required=data.get('required', version.required),
            options=version.options,
            validation=version.validation,
            jump_logic=data.get('jump_logic', version.jump_logic),
            bank_family_id=family._id,
            bank_question_id=version._id,
            bank_version=version.version_number,
        )
        question.save()
        return question, None

    @staticmethod
    def batch_add_questions_from_bank(survey_id: str, user_id: str,
                                      questions_data: List[Dict]) -> Tuple[List[Question], Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return [], '问卷不存在'
        if str(survey.creator_id) != user_id:
            return [], '无权限添加题目'
        if not QuestionService._questions_editable(survey):
            return [], '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'
        existing = Question.find_by_survey_id(survey_id)
        base_order = len(existing)
        from app.services.question_bank_service import QuestionBankService
        # 先完整校验再写入，避免批量题目中途失败留下半批数据
        for item in questions_data:
            version_id = item.get('bank_question_id') or item.get('version_id') or item.get('question_id')
            if not version_id:
                return [], '缺少题库题目版本 ID'
            version = QuestionBankService._get_version(version_id)
            if not version:
                return [], '题库题目版本不存在'
            family = QuestionBankService._get_family(version.family_id)
            if not family or not QuestionBankService.can_view(family, user_id):
                return [], '无权使用该题库题目'
        questions = []
        for i, item in enumerate(questions_data):
            payload = dict(item)
            payload.setdefault('order', base_order + i)
            question, err = QuestionService.add_question_from_bank(survey_id, user_id, payload)
            if err:
                return questions, err
            questions.append(question)
        return questions, None


    @staticmethod
    def update_question(question_id: str, user_id: str, data: Dict) -> Tuple[bool, Optional[str]]:
        question = Question.find_by_id(question_id)
        if not question:
            return False, '题目不存在'

        survey = Survey.find_by_id(str(question.survey_id))
        if not survey or str(survey.creator_id) != user_id:
            return False, '无权限修改'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态的问卷可以修改题目'
        if getattr(survey, 'published_at', None):
            return False, '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        allowed = ['title', 'type', 'order', 'required', 'options', 'validation', 'jump_logic']
        filtered = {k: v for k, v in data.items() if k in allowed}
        Question.update(question_id, filtered)
        return True, None

    @staticmethod
    def delete_question(question_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        question = Question.find_by_id(question_id)
        if not question:
            return False, '题目不存在'

        survey = Survey.find_by_id(str(question.survey_id))
        if not survey or str(survey.creator_id) != user_id:
            return False, '无权限删除'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态的问卷可以删除题目'
        if getattr(survey, 'published_at', None):
            return False, '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        Question.delete(question_id)
        Question.reorder(str(question.survey_id), [])
        return True, None

    @staticmethod
    def reorder_questions(survey_id: str, user_id: str, question_orders: List[Dict]) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限排序'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态的问卷可以调整题目顺序'
        if getattr(survey, 'published_at', None):
            return False, '已发布问卷的题目不可修改；请复制问卷为新版本后再编辑'

        orders = [(qo['id'], qo['order']) for qo in question_orders]
        Question.reorder(survey_id, orders)
        return True, None

    @staticmethod
    def get_questions(survey_id: str) -> List[Question]:
        return Question.find_by_survey_id(survey_id)

    @staticmethod
    def validate_answers(survey_id: str, answers: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        questions = Question.find_by_survey_id(survey_id)
        return ValidationService.validate_all(questions, answers)

    @staticmethod
    def get_visible_questions(survey_id: str, answers: Dict[str, Any]) -> List[Question]:
        questions = Question.find_by_survey_id(survey_id)
        return JumpService.get_visible_questions(questions, answers)

    @staticmethod
    def get_next_question(survey_id: str, current_qid: str, answers: Dict[str, Any]) -> Optional[str]:
        questions = Question.find_by_survey_id(survey_id)
        return JumpService.get_next_question_id(questions, current_qid, answers)