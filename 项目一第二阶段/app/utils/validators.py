import re
from typing import Any, Dict, Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 20 and re.match(r'^[a-zA-Z0-9_]+$', username)


def validate_password(password: str) -> tuple:
    if len(password) < 8:
        return False, '密码长度至少8位'
    if not re.search(r'[A-Z]', password):
        return False, '密码需包含大写字母'
    if not re.search(r'[a-z]', password):
        return False, '密码需包含小写字母'
    if not re.search(r'\d', password):
        return False, '密码需包含数字'
    return True, None


def sanitize_input(text: str, max_len: int = 1000) -> str:
    if not text:
        return ''
    text = text.strip()[:max_len]
    text = re.sub(r'[<>&"\']', '', text)
    return text


def validate_question_data(data: Dict) -> tuple:
    if 'title' not in data or not data['title'].strip():
        return False, '题目标题不能为空'
    if 'type' not in data:
        return False, '题目类型不能为空'

    valid_types = [
        'single_choice', 'multiple_choice', 'dropdown',
        'text', 'textarea', 'number', 'rating', 'date', 'file'
    ]
    if data['type'] not in valid_types:
        return False, '无效的题目类型'

    q_type = data['type']
    if q_type in ['single_choice', 'multiple_choice', 'dropdown']:
        options = data.get('options', [])
        if not options or len(options) < 2:
            return False, '选择题至少需要2个选项'

    return True, None