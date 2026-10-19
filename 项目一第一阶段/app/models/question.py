from datetime import datetime
from bson import ObjectId
from pymongo import UpdateOne


class Question:
    collection = None

    TYPE_SINGLE_CHOICE = 'single_choice'
    TYPE_MULTIPLE_CHOICE = 'multiple_choice'
    TYPE_TEXT = 'text'
    TYPE_TEXTAREA = 'textarea'
    TYPE_NUMBER = 'number'
    TYPE_RATING = 'rating'
    TYPE_DROPDOWN = 'dropdown'
    TYPE_DATE = 'date'
    TYPE_FILE = 'file'

    TYPES = [
        TYPE_SINGLE_CHOICE, TYPE_MULTIPLE_CHOICE, TYPE_TEXT, TYPE_TEXTAREA,
        TYPE_NUMBER, TYPE_RATING, TYPE_DROPDOWN, TYPE_DATE, TYPE_FILE
    ]

    def __init__(self, survey_id, title, q_type, order, required=False, options=None, validation=None, jump_logic=None):
        self.survey_id = ObjectId(survey_id) if isinstance(survey_id, str) else survey_id
        self.title = title
        self.type = q_type
        self.order = order
        self.required = required
        self.options = options or []
        self.validation = validation or {}
        self.jump_logic = jump_logic or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'survey_id': str(self.survey_id),
            'title': self.title,
            'type': self.type,
            'order': self.order,
            'required': self.required,
            'options': self.options,
            'validation': self.validation,
            'jump_logic': self.jump_logic,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        self.updated_at = datetime.utcnow()
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, question_id):
        data = cls.collection.find_one({'_id': ObjectId(question_id)})
        if data:
            q = cls.__new__(cls)
            q.__dict__.update(data)
            return q
        return None

    @classmethod
    def find_by_survey_id(cls, survey_id):
        result = []
        for data in cls.collection.find(
            {'survey_id': ObjectId(survey_id)}
        ).sort('order', 1):
            q = cls.__new__(cls)
            q.__dict__.update(data)
            result.append(q)
        return result

    @classmethod
    def update(cls, question_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': update_data}
        )

    @classmethod
    def delete(cls, question_id):
        return cls.collection.delete_one({'_id': ObjectId(question_id)})

    @classmethod
    def reorder(cls, survey_id, question_orders):
        bulk_ops = []
        for q_id, order in question_orders:
            bulk_ops.append(UpdateOne(
                {'_id': ObjectId(q_id), 'survey_id': ObjectId(survey_id)},
                {'$set': {'order': order, 'updated_at': datetime.utcnow()}}
            ))
        if bulk_ops:
            return cls.collection.bulk_write(bulk_ops)
        return None