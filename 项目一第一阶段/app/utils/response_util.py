from flask import jsonify
from typing import Any, Optional, Dict


def success_response(data: Any = None, message: str = 'success', code: int = 200):
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code


def error_response(message: str, code: int = 400, data: Any = None):
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code