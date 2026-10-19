from typing import Optional, Tuple, Dict
from bson import ObjectId
from app.models.user import User


class UserService:
    @staticmethod
    def register(username: str, password: str, email: str = None) -> Tuple[Optional[User], Optional[str]]:
        if User.find_by_username(username):
            return None, '用户名已存在'
        if email and User.find_by_email(email):
            return None, '邮箱已被注册'

        user = User(username=username, email=email, password=password)
        user.save()
        return user, None

    @staticmethod
    def login(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        user = User.find_by_username(username)
        if not user:
            return None, '用户不存在'
        if not user.check_password(password):
            return None, '密码错误'
        if not user.is_active:
            return None, '账号已禁用'
        return user, None

    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        return User.find_by_id(user_id)

    @staticmethod
    def update_user(user_id: str, data: Dict) -> Tuple[bool, Optional[str]]:
        allowed = ['email']
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            return False, '无可更新字段'
        User.update(user_id, filtered)
        return True, None

    @staticmethod
    def change_password(user_id: str, old_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        user = User.find_by_id(user_id)
        if not user:
            return False, '用户不存在'
        if not user.check_password(old_password):
            return False, '原密码错误'
        from werkzeug.security import generate_password_hash
        User.update(user_id, {'password_hash': generate_password_hash(new_password)})
        return True, None