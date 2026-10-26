import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import pymongo
from config.settings import config

mongo_client = None
db = None


def create_app(config_name=None):
    global mongo_client, db

    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(config[config_name])

    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    JWTManager(app)

    mongo_client = pymongo.MongoClient(app.config['MONGO_URI'])
    db = mongo_client[app.config['MONGO_DB_NAME']]

    bind_collections(db)
    init_indexes(db)

    from app.routes.auth_routes import auth_bp
    from app.routes.survey_routes import survey_bp
    from app.routes.fill_routes import fill_bp
    from app.routes.stats_routes import stats_bp
    from app.routes.question_bank_routes import question_bank_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(survey_bp, url_prefix='/api/surveys')
    app.register_blueprint(fill_bp, url_prefix='/api/fill')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    app.register_blueprint(question_bank_bp, url_prefix='/api/question-bank')

    @app.route('/')
    def index():
        return app.send_static_file('login.html')

    @app.route('/frontend/<path:filename>')
    def legacy_frontend(filename):
        """兼容直接打开 /frontend/xxx.html 的旧地址。"""
        return app.send_static_file(filename)

    @app.route('/survey/<link_code>')
    def survey_link(link_code):
        """分享链接统一为 /survey/<link_code>，由前端根据路径解析链接码。"""
        return app.send_static_file('survey.html')

    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'survey-system'}

    return app


def bind_collections(database):
    from app.models.user import User
    from app.models.survey import Survey
    from app.models.question import Question
    from app.models.response import Response
    from app.models.question_bank import (
        QuestionFamily, QuestionVersion, QuestionBank, QuestionBankEntry
    )
    User.collection = database.users
    Survey.collection = database.surveys
    Question.collection = database.questions
    Response.collection = database.responses
    QuestionFamily.collection = database.question_families
    QuestionVersion.collection = database.question_versions
    QuestionBank.collection = database.question_banks
    QuestionBankEntry.collection = database.question_bank_entries


def init_indexes(database):
    database.users.create_index('username', unique=True)
    database.users.create_index('email', unique=True, sparse=True)
    database.surveys.create_index('creator_id')
    database.surveys.create_index('status')
    database.surveys.create_index('link_code', unique=True)
    database.questions.create_index('survey_id')
    database.questions.create_index('bank_family_id')
    database.questions.create_index('bank_question_id')
    database.question_families.create_index('owner_id')
    database.question_families.create_index('shared_with')
    database.question_families.create_index('is_public')
    database.question_versions.create_index(
        [('family_id', 1), ('version_number', -1)], unique=True
    )
    database.question_versions.create_index('parent_version_id')
    database.question_banks.create_index([('owner_id', 1), ('name', 1)], unique=True)
    database.question_bank_entries.create_index(
        [('bank_id', 1), ('family_id', 1)], unique=True
    )
    database.responses.create_index([('survey_id', 1), ('user_id', 1)])
    database.responses.create_index('submitted_at')