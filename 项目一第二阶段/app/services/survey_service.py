from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from bson import ObjectId
from app.models.survey import Survey
from app.models.question import Question
from app.models.response import Response
from app.models.user import User
from app.services.validation_service import ValidationService
from app.services.jump_service import JumpService
from app import db


class SurveyService:
    @staticmethod
    def _parse_deadline(value) -> Optional[datetime]:
        """把前端传入的截止时间统一转换为 UTC naive datetime。"""
        if value is None or value == '':
            return None
        if isinstance(value, datetime):
            deadline_dt = value
        elif isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            try:
                deadline_dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('截止日期格式不正确')
        else:
            raise ValueError('截止日期格式不正确')

        if deadline_dt.tzinfo is not None:
            deadline_dt = deadline_dt.astimezone(timezone.utc).replace(tzinfo=None)
        if deadline_dt <= datetime.utcnow():
            raise ValueError('截止日期必须在当前时间之后')
        return deadline_dt

    @staticmethod
    def create_survey(creator_id: str, title: str, description: str = '', settings: Dict = None, deadline: str = None) -> Survey:
        deadline_dt = SurveyService._parse_deadline(deadline)
        survey = Survey(
            title=title,
            description=description,
            creator_id=ObjectId(creator_id),
            settings=settings or {},
            deadline=deadline_dt
        )
        return survey.save()

    @staticmethod
    def get_survey(survey_id: str) -> Optional[Survey]:
        return Survey.find_by_id(survey_id)

    @staticmethod
    def get_survey_by_link_code(link_code: str) -> Optional[Dict]:
        survey = Survey.find_by_link_code(link_code)
        if not survey or survey.status != Survey.STATUS_PUBLISHED:
            return None
        if survey.is_expired():
            return None
        questions = Question.find_by_survey_id(str(survey._id))
        data = survey.to_dict()
        data['questions'] = [q.to_dict() for q in questions]
        return data

    @staticmethod
    def get_survey_with_questions(survey_id: str) -> Optional[Dict]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return None
        questions = Question.find_by_survey_id(survey_id)
        data = survey.to_dict()
        data['questions'] = [q.to_dict() for q in questions]
        return data

    @staticmethod
    def update_survey(survey_id: str, user_id: str, update_data: Dict) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限修改'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态的问卷可以修改基本信息'

        allowed = ['title', 'description', 'settings', 'deadline']
        filtered = {k: v for k, v in update_data.items() if k in allowed}
        if 'deadline' in filtered:
            try:
                filtered['deadline'] = SurveyService._parse_deadline(filtered['deadline'])
            except ValueError as exc:
                return False, str(exc)
        Survey.update(survey_id, filtered)
        return True, None

    @staticmethod
    def publish_survey(survey_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限发布'
        if survey.status != Survey.STATUS_DRAFT:
            return False, '只有草稿状态可发布'
        if survey.is_expired():
            return False, '问卷已超过截止日期，无法发布'

        questions = Question.find_by_survey_id(survey_id)
        if not questions:
            return False, '问卷至少需要一道题目'

        Survey.update(survey_id, {'status': Survey.STATUS_PUBLISHED})
        return True, None

    @staticmethod
    def close_survey(survey_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限关闭'
        if survey.status != Survey.STATUS_PUBLISHED:
            return False, '只有已发布的问卷可关闭'

        Survey.update(survey_id, {'status': Survey.STATUS_CLOSED})
        return True, None

    @staticmethod
    def unpublish_survey(survey_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限撤回'
        if survey.status != Survey.STATUS_PUBLISHED:
            return False, '只有已发布的问卷可撤回'

        Survey.update(survey_id, {'status': Survey.STATUS_DRAFT})
        return True, None

    @staticmethod
    def delete_survey(survey_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return False, '问卷不存在'
        if str(survey.creator_id) != user_id:
            return False, '无权限删除'

        Question.collection.delete_many({'survey_id': ObjectId(survey_id)})
        Response.collection.delete_many({'survey_id': ObjectId(survey_id)})
        Survey.delete(survey_id)
        return True, None

    @staticmethod
    def duplicate_survey(survey_id: str, user_id: str) -> Tuple[Optional[Survey], Optional[str]]:
        """把问卷复制为新的草稿版本，用于在不改变旧问卷的前提下继续编辑。"""
        source = Survey.find_by_id(survey_id)
        if not source:
            return None, '问卷不存在'
        if str(source.creator_id) != user_id:
            return None, '无权限复制'
        deadline = getattr(source, 'deadline', None)
        if deadline and source.is_expired():
            deadline = None
        copy = Survey(
            title=f'{source.title} - 副本',
            description=source.description,
            creator_id=source.creator_id,
            settings=dict(getattr(source, 'settings', {}) or {}),
            deadline=deadline,
        )
        copy.save()

        old_questions = Question.find_by_survey_id(str(source._id))
        id_map = {}
        created = []
        for old in old_questions:
            new_q = Question(
                survey_id=copy._id,
                title=old.title,
                q_type=old.type,
                order=old.order,
                required=old.required,
                options=list(old.options or []),
                validation=dict(old.validation or {}),
                jump_logic=dict(old.jump_logic or {}),
                bank_family_id=getattr(old, 'bank_family_id', None),
                bank_question_id=getattr(old, 'bank_question_id', None),
                bank_version=getattr(old, 'bank_version', None),
            )
            new_q.save()
            id_map[str(old._id)] = str(new_q._id)
            created.append((old, new_q))

        # 复制后题目 id 变了，跳转条件需要重写，避免指向旧问卷题目
        for old, new_q in created:
            jump_logic = dict(new_q.jump_logic or {})
            changed = False
            for key in ('source_question_id', 'target_question_id'):
                ref = jump_logic.get(key)
                if ref is not None and str(ref) in id_map:
                    jump_logic[key] = id_map[str(ref)]
                    changed = True
            if changed:
                Question.update(str(new_q._id), {'jump_logic': jump_logic})
        return copy, None

    @staticmethod
    def list_user_surveys(user_id: str, status: str = None, page: int = 1, per_page: int = 10) -> Dict:
        surveys = Survey.find_by_creator(user_id, status)
        total = len(surveys)
        start = (page - 1) * per_page
        end = start + per_page
        items = surveys[start:end]

        result_items = []
        for s in items:
            d = s.to_dict()
            d['response_count'] = Response.collection.count_documents({
                'survey_id': s._id,
                'status': Response.STATUS_SUBMITTED
            })
            result_items.append(d)

        return {
            'items': result_items,
            'total': total,
            'page': page,
            'per_page': per_page
        }

    @staticmethod
    def list_published_surveys(page: int = 1, per_page: int = 10, keyword: str = None) -> Dict:
        query = {
            'status': Survey.STATUS_PUBLISHED,
            '$or': [{'deadline': None}, {'deadline': {'$gt': datetime.utcnow()}}]
        }
        if keyword:
            query['title'] = {'$regex': keyword, '$options': 'i'}

        total = db.surveys.count_documents(query)
        surveys = list(db.surveys.find(query).sort('published_at', -1).skip((page - 1) * per_page).limit(per_page))

        items = []
        for s in surveys:
            survey = Survey.__new__(Survey)
            survey.__dict__.update(s)
            items.append(survey.to_dict())

        return {'items': items, 'total': total, 'page': page, 'per_page': per_page}