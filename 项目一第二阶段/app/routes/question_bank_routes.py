from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.question_bank_service import QuestionBankService
from app.services.stats_service import StatsService
from app.utils.response_util import success_response, error_response

question_bank_bp = Blueprint('question_bank', __name__)


@question_bank_bp.route('/questions', methods=['GET'])
@jwt_required()
def list_questions():
    user_id = get_jwt_identity()
    result, err = QuestionBankService.list_questions(
        user_id,
        scope=request.args.get('scope', 'all'),
        bank_id=request.args.get('bank_id'),
        keyword=request.args.get('keyword'),
        family_id=request.args.get('family_id'),
        latest_only=request.args.get('latest_only', 'true').lower() != 'false',
        page=max(int(request.args.get('page', 1)), 1),
        per_page=min(max(int(request.args.get('per_page', 50)), 1), 200),
    )
    if err:
        return error_response(err, 400)
    return success_response(result)


@question_bank_bp.route('/questions', methods=['POST'])
@jwt_required()
def create_question():
    payload, err = QuestionBankService.create_question(
        get_jwt_identity(), request.get_json() or {}
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '创建成功', 201)


@question_bank_bp.route('/questions/<version_id>', methods=['GET'])
@jwt_required()
def get_question(version_id):
    payload, err = QuestionBankService.get_question(version_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/questions/<version_id>', methods=['PUT'])
@jwt_required()
def update_question(version_id):
    payload, err = QuestionBankService.create_version(
        get_jwt_identity(), version_id, request.get_json() or {}
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '新版本已创建')


@question_bank_bp.route('/questions/<version_id>/versions', methods=['POST'])
@jwt_required()
def create_version(version_id):
    payload, err = QuestionBankService.create_version(
        get_jwt_identity(), version_id, request.get_json() or {}
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '新版本已创建', 201)


@question_bank_bp.route('/questions/<version_id>/fork', methods=['POST'])
@jwt_required()
def fork_question(version_id):
    data = request.get_json() or {}
    payload, err = QuestionBankService.fork_question(
        get_jwt_identity(), version_id, data.get('title')
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '已创建自己的题目副本', 201)


@question_bank_bp.route('/questions/<version_id>/history', methods=['GET'])
@jwt_required()
def get_version_history_alias(version_id):
    version = QuestionBankService._get_version(version_id)
    if not version:
        return error_response('题目版本不存在', 404)
    payload, err = QuestionBankService.get_history(str(version.family_id), get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/questions/<version_id>/versions', methods=['GET'])
@jwt_required()
def get_version_history(version_id):
    version = QuestionBankService._get_version(version_id)
    if not version:
        return error_response('题目版本不存在', 404)
    payload, err = QuestionBankService.get_history(str(version.family_id), get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/questions/<version_id>/usage', methods=['GET'])
@jwt_required()
def get_version_usage(version_id):
    version = QuestionBankService._get_version(version_id)
    if not version:
        return error_response('题目版本不存在', 404)
    payload, err = QuestionBankService.get_usage(str(version.family_id), get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/questions/<version_id>/stats', methods=['GET'])
@jwt_required()
def get_version_stats(version_id):
    version = QuestionBankService._get_version(version_id)
    if not version:
        return error_response('题目版本不存在', 404)
    payload = StatsService.get_family_stats(str(version.family_id), get_jwt_identity())
    if payload is None:
        return error_response('题目不存在或无权查看', 404)
    return success_response(payload)


@question_bank_bp.route('/families/<family_id>/versions', methods=['GET'])
@jwt_required()
def get_family_versions(family_id):
    payload, err = QuestionBankService.get_history(family_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/families/<family_id>/history', methods=['GET'])
@jwt_required()
def get_history(family_id):
    payload, err = QuestionBankService.get_history(family_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/families/<family_id>/restore', methods=['POST'])
@jwt_required()
def restore_version(family_id):
    data = request.get_json() or {}
    version_id = data.get('version_id')
    if not version_id:
        return error_response('缺少版本 ID', 400)
    payload, err = QuestionBankService.restore_version(
        get_jwt_identity(), family_id, version_id
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '旧版本已恢复为新版本')


@question_bank_bp.route('/families/<family_id>/share', methods=['POST'])
@jwt_required()
def share_question(family_id):
    data = request.get_json() or {}
    payload, err = QuestionBankService.share_question(
        get_jwt_identity(), family_id, data.get('username')
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '共享成功')


@question_bank_bp.route('/families/<family_id>/share', methods=['DELETE'])
@jwt_required()
def unshare_question(family_id):
    data = request.get_json() or {}
    ok, err = QuestionBankService.unshare_question(
        get_jwt_identity(), family_id, data.get('username')
    )
    if not ok:
        return error_response(err, 400)
    return success_response(None, '已取消共享')


@question_bank_bp.route('/families/<family_id>/visibility', methods=['PUT'])
@jwt_required()
def set_visibility(family_id):
    data = request.get_json() or {}
    payload, err = QuestionBankService.set_public(
        get_jwt_identity(), family_id, bool(data.get('is_public'))
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '共享范围已更新')


@question_bank_bp.route('/families/<family_id>/usage', methods=['GET'])
@jwt_required()
def get_usage(family_id):
    payload, err = QuestionBankService.get_usage(family_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(payload)


@question_bank_bp.route('/families/<family_id>/stats', methods=['GET'])
@jwt_required()
def get_family_stats(family_id):
    payload = StatsService.get_family_stats(family_id, get_jwt_identity())
    if payload is None:
        return error_response('题目不存在或无权查看', 404)
    return success_response(payload)


@question_bank_bp.route('/banks', methods=['GET'])
@jwt_required()
def list_banks():
    return success_response(QuestionBankService.list_banks(get_jwt_identity()))


@question_bank_bp.route('/banks', methods=['POST'])
@jwt_required()
def create_bank():
    data = request.get_json() or {}
    payload, err = QuestionBankService.create_bank(
        get_jwt_identity(), data.get('name'), data.get('description', '')
    )
    if err:
        return error_response(err, 400)
    return success_response(payload, '题库创建成功', 201)


@question_bank_bp.route('/banks/<bank_id>', methods=['PUT'])
@jwt_required()
def update_bank(bank_id):
    ok, err = QuestionBankService.update_bank(
        get_jwt_identity(), bank_id, request.get_json() or {}
    )
    if not ok:
        return error_response(err, 400)
    return success_response(None, '题库更新成功')


@question_bank_bp.route('/banks/<bank_id>', methods=['DELETE'])
@jwt_required()
def delete_bank(bank_id):
    ok, err = QuestionBankService.delete_bank(get_jwt_identity(), bank_id)
    if not ok:
        return error_response(err, 400)
    return success_response(None, '题库删除成功')


@question_bank_bp.route('/banks/<bank_id>/questions', methods=['GET'])
@jwt_required()
def list_bank_questions(bank_id):
    result, err = QuestionBankService.list_questions(
        get_jwt_identity(), bank_id=bank_id,
        latest_only=request.args.get('latest_only', 'true').lower() != 'false',
    )
    if err:
        return error_response(err, 400)
    return success_response(result)


@question_bank_bp.route('/banks/<bank_id>/questions', methods=['POST'])
@jwt_required()
def add_bank_question(bank_id):
    data = request.get_json() or {}
    family_id = data.get('family_id')
    version_id = data.get('question_id') or data.get('version_id')
    if not family_id and version_id:
        version = QuestionBankService._get_version(version_id)
        if not version:
            return error_response('题目版本不存在', 404)
        family_id = str(version.family_id)
    ok, err = QuestionBankService.add_to_bank(
        get_jwt_identity(), bank_id, family_id
    )
    if not ok:
        return error_response(err, 400)
    return success_response(None, '已加入题库')


@question_bank_bp.route('/banks/<bank_id>/questions/<family_id>', methods=['DELETE'])
@jwt_required()
def remove_bank_question(bank_id, family_id):
    ok, err = QuestionBankService.remove_from_bank(
        get_jwt_identity(), bank_id, family_id
    )
    if not ok:
        return error_response(err, 400)
    return success_response(None, '已从题库移除')
