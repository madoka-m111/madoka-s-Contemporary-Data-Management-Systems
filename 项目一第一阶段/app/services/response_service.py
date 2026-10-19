from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from bson import ObjectId
from app.models.response import Response
from app.models.survey import Survey
from app.models.question import Question
from app.services.validation_service import ValidationService
from app.utils.validators import validate_email
from app import db


class ResponseService:
    @staticmethod
    def start_response(survey_id: str, user_id: str = None, ip: str = None, ua: str = None) -> Tuple[Optional[Response], Optional[str]]:
        survey = Survey.find_by_id(survey_id)
        if not survey:
            return None, '问卷不存在'
        if survey.status != Survey.STATUS_PUBLISHED:
            return None, '问卷未发布或已关闭'
        if survey.is_expired():
            return None, '问卷已截止，无法填写'

        settings = getattr(survey, 'settings', None) or {}
        if not user_id and not settings.get('allow_anonymous', True):
            return None, '该问卷要求登录后填写'

        if user_id:
            user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
            # 同一用户重复打开填写页时复用未完成的记录，避免产生多条草稿
            existing = Response.collection.find_one({
                'survey_id': ObjectId(survey_id),
                'user_id': user_oid,
                'status': Response.STATUS_IN_PROGRESS
            })
            if existing:
                response = Response.__new__(Response)
                response.__dict__.update(existing)
                return response, None
            if settings.get('one_per_user'):
                submitted = Response.collection.find_one({
                    'survey_id': ObjectId(survey_id),
                    'user_id': user_oid,
                    'status': Response.STATUS_SUBMITTED
                })
                if submitted:
                    return None, '您已提交过此问卷'

        response = Response(
            survey_id=ObjectId(survey_id),
            user_id=ObjectId(user_id) if user_id else None,
            status=Response.STATUS_IN_PROGRESS
        )
        if ip:
            response.ip_address = ip
        if ua:
            response.user_agent = ua
        response.save()
        return response, None

    @staticmethod
    def save_draft(response_id: str, answers: Dict[str, Any], user_id: str = None) -> Tuple[bool, Optional[str]]:
        response = Response.find_by_id(response_id)
        if not response:
            return False, '回答记录不存在'
        if response.user_id and str(response.user_id) != str(user_id or ''):
            return False, '无权修改该回答记录'
        if response.status == Response.STATUS_SUBMITTED:
            return False, '已提交的问卷不能修改'

        Response.update(response_id, {'answers': answers, 'status': Response.STATUS_IN_PROGRESS})
        return True, None

    @staticmethod
    def submit_response(response_id: str, answers: Dict[str, Any], email: str = None) -> Tuple[bool, Optional[str], Optional[Dict]]:
        response = Response.find_by_id(response_id)
        if not response:
            return False, '回答记录不存在', None
        if response.status == Response.STATUS_SUBMITTED:
            return False, '已提交过', None

        survey = Survey.find_by_id(str(response.survey_id))
        if not survey or survey.status != Survey.STATUS_PUBLISHED:
            return False, '问卷不可用', None
        if survey.is_expired():
            return False, '问卷已截止，无法提交', None

        settings = getattr(survey, 'settings', None) or {}
        if not response.user_id and not settings.get('allow_anonymous', True):
            return False, '该问卷要求登录后填写', None

        questions = Question.find_by_survey_id(str(response.survey_id))
        valid, errors = ValidationService.validate_all(questions, answers)
        if not valid:
            return False, '校验失败', errors

        effective_answers = ValidationService.get_effective_answers(questions, answers)
        update_data = {
            'answers': effective_answers,
            'status': Response.STATUS_SUBMITTED
        }
        if settings.get('collect_email'):
            normalized_email = email.strip() if isinstance(email, str) else ''
            if normalized_email and not validate_email(normalized_email):
                return False, '校验失败', {'email': '邮箱格式不正确'}
            if normalized_email:
                update_data['email'] = normalized_email

        Response.update(response_id, update_data)
        return True, None, None

    @staticmethod
    def get_response(response_id: str) -> Optional[Response]:
        return Response.find_by_id(response_id)

    @staticmethod
    def get_user_response(survey_id: str, user_id: str) -> Optional[Response]:
        return Response.find_by_survey_and_user(survey_id, user_id)

    @staticmethod
    def list_responses(survey_id: str, status: str = None, page: int = 1, per_page: int = 20) -> Dict:
        query = {'survey_id': ObjectId(survey_id)}
        if status:
            query['status'] = status

        total = db.responses.count_documents(query)
        responses = list(db.responses.find(query).sort('submitted_at', -1).skip((page - 1) * per_page).limit(per_page))

        items = []
        for r in responses:
            resp = Response.__new__(Response)
            resp.__dict__.update(r)
            items.append(resp.to_dict())

        return {'items': items, 'total': total, 'page': page, 'per_page': per_page}