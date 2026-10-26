from datetime import datetime, timezone
from bson import ObjectId


class Response:
    collection = None

    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUBMITTED = 'submitted'

    def __init__(self, survey_id, user_id=None, answers=None, status=STATUS_IN_PROGRESS):
        self.survey_id = ObjectId(survey_id) if isinstance(survey_id, str) else survey_id
        self.user_id = ObjectId(user_id) if user_id and isinstance(user_id, str) else user_id
        self.answers = answers or {}
        self.status = status
        self.started_at = datetime.utcnow()
        self.submitted_at = None
        self.ip_address = None
        self.user_agent = None
        self.email = None

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

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'survey_id': str(self.survey_id),
            'user_id': str(self.user_id) if self.user_id else None,
            'answers': self.answers,
            'status': self.status,
            'email': getattr(self, 'email', None),
            'started_at': self._iso_utc(self.started_at),
            'submitted_at': self._iso_utc(self.submitted_at),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

    def save(self):
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, response_id):
        data = cls.collection.find_one({'_id': ObjectId(response_id)})
        if data:
            resp = cls.__new__(cls)
            resp.__dict__.update(data)
            return resp
        return None

    @classmethod
    def find_by_survey_and_user(cls, survey_id, user_id):
        query = {
            'survey_id': ObjectId(survey_id),
            'user_id': ObjectId(user_id) if isinstance(user_id, str) else user_id
        }
        # 优先返回未完成的记录，避免重复打开填写页时拿到旧的已提交记录
        data = cls.collection.find_one(
            {**query, 'status': cls.STATUS_IN_PROGRESS},
            sort=[('started_at', -1)]
        )
        if not data:
            data = cls.collection.find_one(query, sort=[('started_at', -1)])
        if data:
            resp = cls.__new__(cls)
            resp.__dict__.update(data)
            return resp
        return None

    @classmethod
    def find_by_survey(cls, survey_id, status=None):
        query = {'survey_id': ObjectId(survey_id)}
        if status:
            query['status'] = status
        result = []
        for data in cls.collection.find(query).sort('submitted_at', -1):
            resp = cls.__new__(cls)
            resp.__dict__.update(data)
            result.append(resp)
        return result

    @classmethod
    def update(cls, response_id, update_data):
        if 'status' in update_data and update_data['status'] == cls.STATUS_SUBMITTED:
            update_data['submitted_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': ObjectId(response_id)},
            {'$set': update_data}
        )

    @classmethod
    def get_stats(cls, survey_id):
        pipeline = [
            {'$match': {'survey_id': ObjectId(survey_id), 'status': cls.STATUS_SUBMITTED}},
            {'$group': {
                '_id': None,
                'total': {'$sum': 1},
                'completed': {'$sum': 1}
            }}
        ]
        result = list(cls.collection.aggregate(pipeline))
        return result[0] if result else {'total': 0, 'completed': 0}