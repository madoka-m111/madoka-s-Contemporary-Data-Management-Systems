from typing import List, Optional, Dict, Any, Tuple
from bson import ObjectId
from app.models.question import Question
from app.models.survey import Survey
from app.services.validation_service import ValidationService
from app.services.jump_service import JumpService
from app import db


class QuestionService:
    @staticmethod
    def add_question(survey_id: str, user_id: str, data: Dict) -> Tuple[Optional[Question], Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return None, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return None, '无权限添加题目'
        if survey.status != Survey.STATUS_DRAFT:
            return None, '只有草稿状态的问卷可以添加题目'

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
        if survey.status != Survey.STATUS_DRAFT:
            return [], '只有草稿状态的问卷可以添加题目'

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
    def update_question(question_id: str, user_id: str, data: Dict) -> Tuple[bool, Optional[str]]:
        question = Question.find_by_id(question_id)
        if not question:
            return False, '题目不存在'

        survey = Survey.find_by_id(str(question.survey_id))
        if not survey or str(survey.creator_id) != user_id:
            return False, '无权限修改'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态的问卷可以修改题目'

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