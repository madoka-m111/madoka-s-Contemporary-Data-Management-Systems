from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.survey_service import SurveyService
from app.services.question_service import QuestionService
from app.utils.response_util import success_response, error_response

survey_bp = Blueprint('survey', __name__, url_prefix='/surveys')


@survey_bp.route('', methods=['POST'])
@jwt_required()
def create_survey():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    settings = data.get('settings', {})
    deadline = data.get('deadline')

    if not title:
        return error_response('问卷标题不能为空', 400)

    try:
        survey = SurveyService.create_survey(user_id, title, description, settings, deadline)
    except ValueError as exc:
        return error_response(str(exc), 400)
    return success_response(survey.to_dict(), '创建成功', 201)


@survey_bp.route('', methods=['GET'])
@jwt_required()
def list_my_surveys():
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    result = SurveyService.list_user_surveys(user_id, status, page, per_page)
    return success_response(result)


@survey_bp.route('/public', methods=['GET'])
def list_public_surveys():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    keyword = request.args.get('keyword')

    result = SurveyService.list_published_surveys(page, per_page, keyword)
    return success_response(result)


@survey_bp.route('/<survey_id>', methods=['GET'])
@jwt_required(optional=True)
def get_survey(survey_id):
    user_id = get_jwt_identity()
    survey_data = SurveyService.get_survey_with_questions(survey_id)
    if not survey_data:
        return error_response('问卷不存在', 404)

    survey = SurveyService.get_survey(survey_id)
    if survey and survey.status != 'published':
        if not user_id or str(survey.creator_id) != user_id:
            return error_response('问卷不存在或无权访问', 404)

    return success_response(survey_data)


@survey_bp.route('/link/<link_code>', methods=['GET'])
def get_survey_by_link(link_code):
    survey_data = SurveyService.get_survey_by_link_code(link_code)
    if not survey_data:
        return error_response('问卷不存在、未发布或已截止', 404)
    return success_response(survey_data)


@survey_bp.route('/<survey_id>', methods=['PUT'])
@jwt_required()
def update_survey(survey_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    ok, err = SurveyService.update_survey(survey_id, user_id, data)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '更新成功')


@survey_bp.route('/<survey_id>/publish', methods=['POST'])
@jwt_required()
def publish_survey(survey_id):
    user_id = get_jwt_identity()
    ok, err = SurveyService.publish_survey(survey_id, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '发布成功')


@survey_bp.route('/<survey_id>/close', methods=['POST'])
@jwt_required()
def close_survey(survey_id):
    user_id = get_jwt_identity()
    ok, err = SurveyService.close_survey(survey_id, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '关闭成功')


@survey_bp.route('/<survey_id>/unpublish', methods=['POST'])
@jwt_required()
def unpublish_survey(survey_id):
    user_id = get_jwt_identity()
    ok, err = SurveyService.unpublish_survey(survey_id, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '撤回成功')


@survey_bp.route('/<survey_id>', methods=['DELETE'])
@jwt_required()
def delete_survey(survey_id):
    user_id = get_jwt_identity()
    ok, err = SurveyService.delete_survey(survey_id, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '删除成功')


@survey_bp.route('/<survey_id>/questions', methods=['GET'])
@jwt_required(optional=True)
def get_questions(survey_id):
    user_id = get_jwt_identity()
    survey = SurveyService.get_survey(survey_id)
    if not survey:
        return error_response('问卷不存在', 404)
    if survey.status != 'published' and (not user_id or str(survey.creator_id) != user_id):
        return error_response('无权访问', 403)

    questions = QuestionService.get_questions(survey_id)
    return success_response([q.to_dict() for q in questions])


@survey_bp.route('/<survey_id>/questions', methods=['POST'])
@jwt_required()
def add_question(survey_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    required = ['title', 'type']
    if not all(k in data for k in required):
        return error_response('缺少必要字段', 400)

    question, err = QuestionService.add_question(survey_id, user_id, data)
    if err:
        return error_response(err, 400)
    return success_response(question.to_dict(), '添加成功', 201)


@survey_bp.route('/<survey_id>/questions/batch', methods=['POST'])
@jwt_required()
def batch_add_questions(survey_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    questions_data = data.get('questions', [])
    if not questions_data:
        return error_response('题目列表不能为空', 400)

    questions, err = QuestionService.batch_add_questions(survey_id, user_id, questions_data)
    if err:
        return error_response(err, 400)
    return success_response([q.to_dict() for q in questions], '批量添加成功', 201)


@survey_bp.route('/<survey_id>/questions/reorder', methods=['PUT'])
@jwt_required()
def reorder_questions(survey_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    question_orders = data.get('question_orders', [])
    if not question_orders:
        return error_response('排序数据不能为空', 400)

    ok, err = QuestionService.reorder_questions(survey_id, user_id, question_orders)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '排序成功')


@survey_bp.route('/questions/<question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    ok, err = QuestionService.update_question(question_id, user_id, data)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '更新成功')


@survey_bp.route('/questions/<question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    user_id = get_jwt_identity()
    ok, err = QuestionService.delete_question(question_id, user_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '删除成功')