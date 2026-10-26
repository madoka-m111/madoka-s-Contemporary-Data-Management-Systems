from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.response_service import ResponseService
from app.services.question_service import QuestionService
from app.utils.response_util import success_response, error_response

fill_bp = Blueprint('fill', __name__, url_prefix='/fill')


@fill_bp.route('/surveys/<survey_id>/start', methods=['POST'])
@jwt_required(optional=True)
def start_fill(survey_id):
    user_id = get_jwt_identity()
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')

    response, err = ResponseService.start_response(survey_id, user_id, ip, ua)
    if err:
        return error_response(err, 400)
    return success_response({'response_id': str(response._id), 'started_at': response.started_at.isoformat()}, '创建成功', 201)


@fill_bp.route('/responses/<response_id>/draft', methods=['PUT'])
@jwt_required(optional=True)
def save_draft(response_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    answers = data.get('answers', {})

    ok, err = ResponseService.save_draft(response_id, answers, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '保存成功')


@fill_bp.route('/responses/<response_id>', methods=['GET'])
@jwt_required(optional=True)
def get_fill_progress(response_id):
    user_id = get_jwt_identity()
    response = ResponseService.get_response(response_id)
    if not response:
        return error_response('回答记录不存在', 404)
    if response.user_id and str(response.user_id) != str(user_id or ''):
        return error_response('无权查看该回答记录', 403)
    return success_response(response.to_dict())


@fill_bp.route('/surveys/<survey_id>/validate', methods=['GET'])
@jwt_required(optional=True)
def validate_answers(survey_id):
    import json
    answers_str = request.args.get('answers', '{}')
    try:
        answers = json.loads(answers_str)
    except json.JSONDecodeError:
        return error_response('答案格式错误', 400)

    valid, errors = QuestionService.validate_answers(survey_id, answers)
    return success_response({'valid': valid, 'errors': errors})


@fill_bp.route('/surveys/<survey_id>/submit', methods=['POST'])
@jwt_required(optional=True)
def submit_survey(survey_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    answers = data.get('answers', {})
    email = data.get('email')
    response_id = data.get('response_id')

    response = None
    if response_id:
        candidate = ResponseService.get_response(response_id)
        if candidate and str(candidate.survey_id) == survey_id:
            owner = str(candidate.user_id) if candidate.user_id else None
            if owner is None or owner == user_id:
                response = candidate
    if not response and user_id:
        response = ResponseService.get_user_response(survey_id, user_id)
    if not response:
        response, err = ResponseService.start_response(survey_id, user_id, request.remote_addr, request.headers.get('User-Agent'))
        if err:
            return error_response(err, 400)

    ok, err, validation_errors = ResponseService.submit_response(str(response._id), answers, email)
    if not ok:
        if validation_errors:
            return error_response(err, 422, validation_errors)
        return error_response(err, 400)

    return success_response({'response_id': str(response._id)}, '提交成功')