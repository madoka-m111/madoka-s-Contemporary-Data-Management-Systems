from datetime import datetime
from bson import ObjectId


def _to_object_id(value):
    if isinstance(value, ObjectId):
        return value
    if isinstance(value, str) and ObjectId.is_valid(value):
        return ObjectId(value)
    return None


class QuestionFamily:
    """题目的稳定身份。

    一个 family 代表“同一个题目”，其下可以存在多个不可变版本。
    问卷使用题目时保存的是某个版本的快照，因此后续新增版本不会影响旧问卷。
    """

    collection = None

    def __init__(self, owner_id, title, description='', latest_version_id=None,
                 version_count=0, is_public=False, shared_with=None,
                 derived_from_family_id=None, derived_from_version_id=None,
                 archived=False):
        self.owner_id = _to_object_id(owner_id)
        self.title = title
        self.description = description or ''
        self.latest_version_id = _to_object_id(latest_version_id)
        self.version_count = version_count
        self.is_public = bool(is_public)
        self.shared_with = shared_with or []
        self.derived_from_family_id = _to_object_id(derived_from_family_id)
        self.derived_from_version_id = _to_object_id(derived_from_version_id)
        self.archived = bool(archived)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'owner_id': str(self.owner_id),
            'title': self.title,
            'description': self.description,
            'latest_version_id': str(self.latest_version_id) if self.latest_version_id else None,
            'version_count': self.version_count,
            'is_public': self.is_public,
            'shared_with': [str(uid) for uid in self.shared_with],
            'derived_from_family_id': str(self.derived_from_family_id) if self.derived_from_family_id else None,
            'derived_from_version_id': str(self.derived_from_version_id) if self.derived_from_version_id else None,
            'archived': self.archived,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        self.updated_at = datetime.utcnow()
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, family_id):
        oid = _to_object_id(family_id)
        if not oid:
            return None
        data = cls.collection.find_one({'_id': oid})
        if data:
            family = cls.__new__(cls)
            family.__dict__.update(data)
            return family
        return None

    @classmethod
    def update(cls, family_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': _to_object_id(family_id)},
            {'$set': update_data}
        )

    @classmethod
    def delete(cls, family_id):
        return cls.collection.delete_one({'_id': _to_object_id(family_id)})



class QuestionVersion:
    """题目的一个不可变版本。更新题目时只能追加新版本。"""

    collection = None

    CONTENT_FIELDS = [
        'title', 'type', 'required', 'options', 'validation', 'jump_logic'
    ]

    def __init__(self, family_id, version_number, title, q_type, required=False,
                 options=None, validation=None, jump_logic=None,
                 parent_version_id=None, created_by=None, change_note='',
                 restored_from_version_id=None):
        self.family_id = _to_object_id(family_id)
        self.version_number = int(version_number)
        self.title = title
        self.type = q_type
        self.required = bool(required)
        self.options = options or []
        self.validation = validation or {}
        self.jump_logic = jump_logic or {}
        self.parent_version_id = _to_object_id(parent_version_id)
        self.created_by = _to_object_id(created_by)
        self.change_note = change_note or ''
        self.restored_from_version_id = _to_object_id(restored_from_version_id)
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'family_id': str(self.family_id),
            'version': self.version_number,
            'version_number': self.version_number,
            'title': self.title,
            'type': self.type,
            'required': self.required,
            'options': self.options,
            'validation': self.validation,
            'jump_logic': self.jump_logic,
            'parent_version_id': str(self.parent_version_id) if self.parent_version_id else None,
            'restored_from_version_id': str(self.restored_from_version_id) if self.restored_from_version_id else None,
            'created_by': str(self.created_by) if self.created_by else None,
            'change_note': self.change_note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def save(self):
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, version_id):
        oid = _to_object_id(version_id)
        if not oid:
            return None
        data = cls.collection.find_one({'_id': oid})
        if data:
            version = cls.__new__(cls)
            version.__dict__.update(data)
            return version
        return None

    @classmethod
    def find_by_family(cls, family_id):
        oid = _to_object_id(family_id)
        if not oid:
            return []
        result = []
        for data in cls.collection.find({'family_id': oid}).sort('version_number', -1):
            version = cls.__new__(cls)
            version.__dict__.update(data)
            result.append(version)
        return result

    @classmethod
    def find_latest(cls, family_id):
        oid = _to_object_id(family_id)
        if not oid:
            return None
        data = cls.collection.find_one({'family_id': oid}, sort=[('version_number', -1)])
        if data:
            version = cls.__new__(cls)
            version.__dict__.update(data)
            return version
        return None

    @classmethod
    def next_version_number(cls, family_id):
        latest = cls.find_latest(family_id)


class QuestionBank:
    """用户维护的题库，一个用户可以拥有多个题库。"""

    collection = None

    def __init__(self, owner_id, name, description='', is_default=False):
        self.owner_id = _to_object_id(owner_id)
        self.name = name
        self.description = description or ''
        self.is_default = bool(is_default)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'owner_id': str(self.owner_id),
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        self.updated_at = datetime.utcnow()
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_id(cls, bank_id):
        oid = _to_object_id(bank_id)
        if not oid:
            return None
        data = cls.collection.find_one({'_id': oid})
        if data:
            bank = cls.__new__(cls)
            bank.__dict__.update(data)
            return bank
        return None

    @classmethod
    def find_by_owner(cls, owner_id):
        oid = _to_object_id(owner_id)
        if not oid:
            return []
        result = []
        for data in cls.collection.find({'owner_id': oid}).sort('created_at', 1):
            bank = cls.__new__(cls)
            bank.__dict__.update(data)
            result.append(bank)
        return result

    @classmethod
    def update(cls, bank_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        return cls.collection.update_one(
            {'_id': _to_object_id(bank_id)},
            {'$set': update_data}
        )

    @classmethod
    def delete(cls, bank_id):
        return cls.collection.delete_one({'_id': _to_object_id(bank_id)})


class QuestionBankEntry:
    """题库与题目 family 的关联，允许多个用户把共享题加入自己的题库。"""

    collection = None

    def __init__(self, bank_id, family_id, added_by):
        self.bank_id = _to_object_id(bank_id)
        self.family_id = _to_object_id(family_id)
        self.added_by = _to_object_id(added_by)
        self.added_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'bank_id': str(self.bank_id),
            'family_id': str(self.family_id),
            'added_by': str(self.added_by) if self.added_by else None,
            'added_at': self.added_at.isoformat() if self.added_at else None,
        }

    def save(self):
        result = self.collection.insert_one(self.__dict__)
        self._id = result.inserted_id
        return self

    @classmethod
    def find_by_bank(cls, bank_id):
        oid = _to_object_id(bank_id)
        if not oid:
            return []
        result = []
        for data in cls.collection.find({'bank_id': oid}).sort('added_at', 1):
            entry = cls.__new__(cls)
            entry.__dict__.update(data)
            result.append(entry)
        return result

    @classmethod
    def find_one(cls, bank_id, family_id):
        data = cls.collection.find_one({
            'bank_id': _to_object_id(bank_id),
            'family_id': _to_object_id(family_id),
        })
        if data:
            entry = cls.__new__(cls)
            entry.__dict__.update(data)
            return entry
        return None

    @classmethod
    def delete(cls, bank_id, family_id):
        return cls.collection.delete_one({
            'bank_id': _to_object_id(bank_id),
            'family_id': _to_object_id(family_id),
        })

    @classmethod
    def delete_by_bank(cls, bank_id):
        return cls.collection.delete_many({'bank_id': _to_object_id(bank_id)})

        return latest.version_number + 1 if latest else 1
