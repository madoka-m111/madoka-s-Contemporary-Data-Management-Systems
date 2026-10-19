from datetime import datetime, timezone
from bson import ObjectId
import uuid


class Survey:
    collection = None

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CLOSED = 'closed'

    DEFAULT_SETTINGS = {
        'allow_anonymous': True,
        'show_progress': True,
        'one_per_user': False,
        'collect_email': False
    }

    def __init__(self, title, description, creator_id, status=STATUS_DRAFT, settings=None, deadline=None, link_code=None):
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.status = status
        merged_settings = dict(self.DEFAULT_SETTINGS)
        if settings:
            merged_settings.update(settings)
        self.settings = merged_settings
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.published_at = None
        self.closed_at = None
        self.deadline = deadline
        self.link_code = link_code or str(uuid.uuid4())[:8]

    @staticmethod
    def _iso_utc(value):
        """统一输出带 Z 的 UTC 时间，避免浏览器按本地时区误解析。"""
        if not value:
            return None
        if isinstance(value, str):
            return value
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value.isoformat() + 'Z'

    def is_expired(self):
        deadline = getattr(self, 'deadline', None)
        if not deadline:
            return False
        if isinstance(deadline, str):
            try:
                deadline = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
            except ValueError:
                return False
        if deadline.tzinfo is not None:
            deadline = deadline.astimezone(timezone.utc).replace(tzinfo=None)
        return deadline <= datetime.utcnow()

    def to_dict(self, include_questions=False):
        data = {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'title': self.title,
            'description': self.description,
            'creator_id': str(self.creator_id) if isinstance(self.creator_id, ObjectId) else self.creator_id,
            'status': self.status,
            'settings': self.settings,
            'created_at': self._iso_utc(getattr(self, 'created_at', None)),
            'updated_at': self._iso_utc(getattr(self, 'updated_at', None)),
            'published_at': self._iso_utc(getattr(self, 'published_at', None)),
            'closed_at': self._iso_utc(getattr(self, 'closed_at', None)),
            'deadline': self._iso_utc(getattr(self, 'deadline', None)),
            'is_expired': self.is_expired(),
            'link_code': getattr(self, 'link_code', None)
        }
        if include_questions:
            from app.models.question import Question
            data['questions'] = Question.find_by_survey_id(str(self._id))
        return data

    def save(self):
        self.updated_at = datetime.utcnow()
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, survey_id):
        if not survey_id or not ObjectId.is_valid(survey_id):
            return None
        data = cls.collection.find_one({'_id': ObjectId(survey_id)})
        if data:
            survey = cls.__new__(cls)
            survey.__dict__.update(data)
            return survey
        return None

    @classmethod
    def find_by_link_code(cls, link_code):
        data = cls.collection.find_one({'link_code': link_code})
        if data:
            survey = cls.__new__(cls)
            survey.__dict__.update(data)
            return survey
        return None

    @classmethod
    def find_by_creator(cls, creator_id, status=None):
        query = {'creator_id': ObjectId(creator_id) if isinstance(creator_id, str) else creator_id}
        if status:
            query['status'] = status
        result = []
        for data in cls.collection.find(query).sort('created_at', -1):
            s = cls.__new__(cls)
            s.__dict__.update(data)
            result.append(s)
        return result

    @classmethod
    def find_published(cls):
        result = []
        for data in cls.collection.find({'status': cls.STATUS_PUBLISHED}).sort('published_at', -1):
            s = cls.__new__(cls)
            s.__dict__.update(data)
            result.append(s)
        return result

    @classmethod
    def update(cls, survey_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        if 'status' in update_data:
            if update_data['status'] == cls.STATUS_PUBLISHED:
                update_data['published_at'] = datetime.utcnow()
            elif update_data['status'] == cls.STATUS_CLOSED:
                update_data['closed_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': ObjectId(survey_id)},
            {'$set': update_data}
        )

    @classmethod
    def delete(cls, survey_id):
        return cls.collection.delete_one({'_id': ObjectId(survey_id)})