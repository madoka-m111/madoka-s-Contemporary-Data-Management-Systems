from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    collection = None

    def __init__(self, username, email, password, role='user'):
        self.username = username
        if email:
            self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_active = True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'username': self.username,
            'email': getattr(self, 'email', None),
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def save(self):
        self.updated_at = datetime.utcnow()
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, user_id):
        from bson import ObjectId
        data = cls.collection.find_one({'_id': ObjectId(user_id)})
        if data:
            user = cls.__new__(cls)
            user.__dict__.update(data)
            return user
        return None

    @classmethod
    def find_by_username(cls, username):
        data = cls.collection.find_one({'username': username})
        if data:
            user = cls.__new__(cls)
            user.__dict__.update(data)
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        data = cls.collection.find_one({'email': email})
        if data:
            user = cls.__new__(cls)
            user.__dict__.update(data)
            return user
        return None

    @classmethod
    def update(cls, user_id, update_data):
        from bson import ObjectId
        update_data['updated_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )