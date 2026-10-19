from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.utils.response_util import success_response, error_response

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return error_response('用户名和密码不能为空', 400)

    user, err = UserService.register(username, password, email or None)
    if err:
        return error_response(err, 400)

    token = create_access_token(identity=str(user._id))
    return success_response({
        'user': user.to_dict(),
        'access_token': token
    }, '注册成功', 201)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return error_response('用户名和密码不能为空', 400)

    user, err = UserService.login(username, password)
    if err:
        return error_response(err, 401)

    token = create_access_token(identity=str(user._id))
    return success_response({
        'user': user.to_dict(),
        'access_token': token
    }, '登录成功')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = UserService.get_user(user_id)
    if not user:
        return error_response('用户不存在', 404)
    return success_response(user.to_dict())