import re
from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List

from bson import ObjectId

from app import db
from app.models.question import Question
from app.models.user import User
from app.models.question_bank import (
    QuestionFamily, QuestionVersion, QuestionBank, QuestionBankEntry
)


class QuestionBankService:
    """题目库、题目共享与题目版本管理。"""

    DEFAULT_BANK_NAME = '我的题库'

    @staticmethod
    def _content_from_data(data: Dict, base: Optional[QuestionVersion] = None) -> Dict:
        base_data = base.to_dict() if base else {}
        content = {}
        for field in QuestionVersion.CONTENT_FIELDS:
            if field in data:
                content[field] = data[field]
            elif field in base_data:
                content[field] = base_data[field]
        content.setdefault('title', '')
        content.setdefault('type', '')
        content.setdefault('required', False)
        content.setdefault('options', [])
        content.setdefault('validation', {})
        content.setdefault('jump_logic', {})
        return content

    @staticmethod
    def _validate_content(content: Dict) -> Optional[str]:
        title = content.get('title')
        if not isinstance(title, str) or not title.strip():
            return '题目内容不能为空'
        if content.get('type') not in Question.TYPES:
            return '题目类型不合法'
        if not isinstance(content.get('required', False), bool):
            return 'required 必须为布尔值'
        if content.get('options') is not None and not isinstance(content['options'], list):
            return '选项必须为数组'
        if content.get('options') and not all(isinstance(x, str) for x in content['options']):
            return '选项内容必须为字符串'
        if content.get('validation') is not None and not isinstance(content['validation'], dict):
            return '校验配置必须为对象'
        if content.get('jump_logic') is not None and not isinstance(content['jump_logic'], dict):
            return '跳转配置必须为对象'
        content['title'] = title.strip()
        return None

    @staticmethod
    def _get_version(version_id: str) -> Optional[QuestionVersion]:
        return QuestionVersion.find_by_id(version_id)

    @staticmethod
    def _get_family(family_id: str) -> Optional[QuestionFamily]:
        return QuestionFamily.find_by_id(family_id)

    @staticmethod
    def _is_owner(family: QuestionFamily, user_id: str) -> bool:
        return str(family.owner_id) == str(user_id or '')

    @staticmethod
    def can_view(family: QuestionFamily, user_id: str) -> bool:
        if not family or not user_id:
            return False
        if QuestionBankService._is_owner(family, user_id):
            return True
        if getattr(family, 'is_public', False):
            return True
        return any(str(uid) == str(user_id) for uid in getattr(family, 'shared_with', []))

    @staticmethod
    def can_edit(family: QuestionFamily, user_id: str) -> bool:
        return bool(family and QuestionBankService._is_owner(family, user_id))

    @staticmethod
    def get_or_create_default_bank(user_id: str) -> QuestionBank:
        for bank in QuestionBank.find_by_owner(user_id):
            if getattr(bank, 'is_default', False):
                return bank
        existing = db.question_banks.find_one({
            'owner_id': ObjectId(user_id),
            'name': QuestionBankService.DEFAULT_BANK_NAME,
        })
        if existing:
            bank = QuestionBank.__new__(QuestionBank)
            bank.__dict__.update(existing)
            if not getattr(bank, 'is_default', False):
                QuestionBank.update(str(bank._id), {'is_default': True})
                bank.is_default = True
            return bank
        bank = QuestionBank(user_id, QuestionBankService.DEFAULT_BANK_NAME, is_default=True)
        return bank.save()

    @staticmethod
    def _get_owned_bank(bank_id: str, user_id: str) -> Tuple[Optional[QuestionBank], Optional[str]]:
        bank = QuestionBank.find_by_id(bank_id)
        if not bank:
            return None, '题库不存在'
        if str(bank.owner_id) != str(user_id or ''):
            return None, '无权限管理该题库'
        return bank, None

    @staticmethod
    def add_to_bank(user_id: str, bank_id: str, family_id: str) -> Tuple[bool, Optional[str]]:
        bank, err = QuestionBankService._get_owned_bank(bank_id, user_id)
        if err:
            return False, err
        family = QuestionBankService._get_family(family_id)
        if not family:
            return False, '题目不存在'
        if not QuestionBankService.can_view(family, user_id):
            return False, '无权限使用该题目'
        if not QuestionBankEntry.find_one(bank._id, family._id):
            QuestionBankEntry(bank._id, family._id, user_id).save()
        return True, None

    @staticmethod
    def remove_from_bank(user_id: str, bank_id: str, family_id: str) -> Tuple[bool, Optional[str]]:
        _, err = QuestionBankService._get_owned_bank(bank_id, user_id)
        if err:
            return False, err
        QuestionBankEntry.delete(bank_id, family_id)
        return True, None

    @staticmethod
    def create_question(user_id: str, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        content = QuestionBankService._content_from_data(data)
        err = QuestionBankService._validate_content(content)
        if err:
            return None, err

        bank_id = data.get('bank_id')
        if bank_id:
            bank, bank_err = QuestionBankService._get_owned_bank(bank_id, user_id)
            if bank_err:
                return None, bank_err
        else:
            bank = QuestionBankService.get_or_create_default_bank(user_id)

        family = QuestionFamily(
            owner_id=user_id,
            title=content['title'],
            description=data.get('description', ''),
        )
        family.save()
        version = QuestionVersion(
            family_id=family._id,
            version_number=1,
            title=content['title'],
            q_type=content['type'],
            required=content.get('required', False),
            options=content.get('options', []),
            validation=content.get('validation', {}),
            jump_logic=content.get('jump_logic', {}),
            parent_version_id=None,
            created_by=user_id,
            change_note=data.get('change_note', '创建题目'),
        )
        version.save()
        QuestionFamily.update(family._id, {
            'latest_version_id': version._id,
            'version_count': 1,
        })
        family.latest_version_id = version._id
        family.version_count = 1
        QuestionBankService.add_to_bank(user_id, str(bank._id), str(family._id))
        return QuestionBankService._version_payload(version, family, user_id), None

    @staticmethod
    def _next_version_number(family_id) -> int:
        latest = QuestionVersion.find_latest(family_id)
        return (latest.version_number if latest else 0) + 1

    @staticmethod
    def create_version(user_id: str, version_id: str, data: Dict,
                       change_note: str = None) -> Tuple[Optional[Dict], Optional[str]]:
        source = QuestionBankService._get_version(version_id)
        if not source:
            return None, '题目版本不存在'
        family = QuestionBankService._get_family(source.family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService.can_edit(family, user_id):
            return None, '无权限修改该题目，可先创建自己的副本'

        base = source
        base_version_id = data.get('base_version_id')
        if base_version_id:
            candidate = QuestionBankService._get_version(base_version_id)
            if not candidate or str(candidate.family_id) != str(family._id):
                return None, '基准版本不属于该题目'
            base = candidate

        content = QuestionBankService._content_from_data(data, base)
        err = QuestionBankService._validate_content(content)
        if err:
            return None, err

        version_number = QuestionBankService._next_version_number(family._id)
        version = QuestionVersion(
            family_id=family._id,
            version_number=version_number,
            title=content['title'],
            q_type=content['type'],
            required=content.get('required', False),
            options=content.get('options', []),
            validation=content.get('validation', {}),
            jump_logic=content.get('jump_logic', {}),
            parent_version_id=base._id,
            created_by=user_id,
            change_note=change_note or data.get('change_note') or f'基于 v{base.version_number} 修改',
        )
        version.save()
        QuestionFamily.update(family._id, {
            'title': content['title'],
            'latest_version_id': version._id,
            'version_count': version_number,
        })
        family.title = content['title']
        family.latest_version_id = version._id
        family.version_count = version_number
        return QuestionBankService._version_payload(version, family, user_id), None



    @staticmethod
    def restore_version(user_id: str, family_id: str, version_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService.can_edit(family, user_id):
            return None, '无权限恢复该题目'
        target = QuestionBankService._get_version(version_id)
        if not target or str(target.family_id) != str(family._id):
            return None, '要恢复的版本不存在'
        latest = QuestionVersion.find_latest(family._id)
        version_number = QuestionBankService._next_version_number(family._id)
        version = QuestionVersion(
            family_id=family._id,
            version_number=version_number,
            title=target.title,
            q_type=target.type,
            required=target.required,
            options=target.options,
            validation=target.validation,
            jump_logic=target.jump_logic,
            parent_version_id=latest._id if latest else None,
            created_by=user_id,
            change_note=f'恢复自 v{target.version_number}',
            restored_from_version_id=target._id,
        )
        version.save()
        QuestionFamily.update(family._id, {
            'title': target.title,
            'latest_version_id': version._id,
            'version_count': version_number,
        })
        family.title = target.title
        family.latest_version_id = version._id
        family.version_count = version_number
        return QuestionBankService._version_payload(version, family, user_id), None

    @staticmethod
    def fork_question(user_id: str, version_id: str, title: str = None) -> Tuple[Optional[Dict], Optional[str]]:
        source = QuestionBankService._get_version(version_id)
        if not source:
            return None, '题目版本不存在'
        source_family = QuestionBankService._get_family(source.family_id)
        if not source_family or not QuestionBankService.can_view(source_family, user_id):
            return None, '无权限使用该题目'
        family = QuestionFamily(
            owner_id=user_id,
            title=title or source.title,
            description=f'从题目 {source_family.title} 派生',
            derived_from_family_id=source_family._id,
            derived_from_version_id=source._id,
        )
        family.save()
        version = QuestionVersion(
            family_id=family._id,
            version_number=1,
            title=title or source.title,
            q_type=source.type,
            required=source.required,
            options=source.options,
            validation=source.validation,
            jump_logic=source.jump_logic,
            parent_version_id=None,
            created_by=user_id,
            change_note=f'派生自 {source_family.title} v{source.version_number}',
        )
        version.save()
        QuestionFamily.update(family._id, {
            'latest_version_id': version._id,
            'version_count': 1,
        })
        family.latest_version_id = version._id
        family.version_count = 1
        bank = QuestionBankService.get_or_create_default_bank(user_id)
        QuestionBankService.add_to_bank(user_id, str(bank._id), str(family._id))
        return QuestionBankService._version_payload(version, family, user_id), None

    @staticmethod
    def share_question(user_id: str, family_id: str, username: str) -> Tuple[Optional[Dict], Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService._is_owner(family, user_id):
            return None, '只有题目创建者可以共享'
        target = User.find_by_username((username or '').strip())
        if not target:
            return None, '目标用户不存在'
        if str(target._id) == str(user_id):
            return None, '不能共享给自己'
        db.question_families.update_one(
            {'_id': family._id},
            {'$addToSet': {'shared_with': target._id}, '$set': {'updated_at': datetime.utcnow()}}
        )
        family = QuestionBankService._get_family(family_id)
        return QuestionBankService._family_payload(family, user_id), None

    @staticmethod
    def unshare_question(user_id: str, family_id: str, username: str) -> Tuple[bool, Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return False, '题目不存在'
        if not QuestionBankService._is_owner(family, user_id):
            return False, '只有题目创建者可以取消共享'
        target = User.find_by_username((username or '').strip())
        if not target:
            return False, '目标用户不存在'
        db.question_families.update_one(
            {'_id': family._id},
            {'$pull': {'shared_with': target._id}, '$set': {'updated_at': datetime.utcnow()}}
        )
        return True, None

    @staticmethod
    def set_public(user_id: str, family_id: str, is_public: bool) -> Tuple[Optional[Dict], Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService._is_owner(family, user_id):
            return None, '只有题目创建者可以修改共享范围'
        family.is_public = bool(is_public)
        QuestionFamily.update(family._id, {'is_public': family.is_public})
        return QuestionBankService._family_payload(family, user_id), None



    @staticmethod
    def _user_name(user_id) -> Optional[str]:
        if not user_id:
            return None
        user = User.find_by_id(str(user_id))
        return getattr(user, 'username', None) if user else None

    @staticmethod
    def _family_payload(family: QuestionFamily, user_id: str = None) -> Dict:
        data = family.to_dict()
        data['owner_name'] = QuestionBankService._user_name(family.owner_id)
        data['shared_users'] = [
            {'id': str(uid), 'username': QuestionBankService._user_name(uid)}
            for uid in getattr(family, 'shared_with', [])
        ]
        data['usage_count'] = db.questions.count_documents({'bank_family_id': family._id})
        data['can_edit'] = QuestionBankService.can_edit(family, user_id)
        data['can_view'] = QuestionBankService.can_view(family, user_id)
        return data

    @staticmethod
    def _version_payload(version: QuestionVersion, family: QuestionFamily = None,
                         user_id: str = None) -> Dict:
        family = family or QuestionBankService._get_family(version.family_id)
        data = version.to_dict()
        data['owner_id'] = str(family.owner_id)
        data['owner_name'] = QuestionBankService._user_name(family.owner_id)
        data['family_title'] = family.title
        data['latest_version_id'] = str(family.latest_version_id) if family.latest_version_id else None
        data['is_latest'] = str(family.latest_version_id) == str(version._id)
        data['version_count'] = family.version_count
        data['is_public'] = getattr(family, 'is_public', False)
        data['shared_with'] = [str(uid) for uid in getattr(family, 'shared_with', [])]
        data['usage_count'] = db.questions.count_documents({'bank_family_id': family._id})
        data['can_edit'] = QuestionBankService.can_edit(family, user_id)
        data['can_view'] = QuestionBankService.can_view(family, user_id)
        data['derived_from_family_id'] = str(family.derived_from_family_id) if getattr(family, 'derived_from_family_id', None) else None
        data['derived_from_version_id'] = str(family.derived_from_version_id) if getattr(family, 'derived_from_version_id', None) else None
        return data

    @staticmethod
    def _visible_query(user_id: str, scope: str = 'all') -> Dict:
        user_oid = ObjectId(user_id)
        if scope == 'mine':
            return {'owner_id': user_oid, 'archived': {'$ne': True}}
        if scope == 'shared':
            return {
                'owner_id': {'$ne': user_oid},
                'archived': {'$ne': True},
                '$or': [{'shared_with': user_oid}, {'is_public': True}],
            }
        return {
            'archived': {'$ne': True},
            '$or': [
                {'owner_id': user_oid},
                {'shared_with': user_oid},
                {'is_public': True},
            ],
        }



    @staticmethod
    def list_questions(user_id: str, scope: str = 'all', bank_id: str = None,
                       keyword: str = None, family_id: str = None,
                       latest_only: bool = True, page: int = 1,
                       per_page: int = 50) -> Tuple[Optional[Dict], Optional[str]]:
        query = QuestionBankService._visible_query(user_id, scope)
        if bank_id:
            bank, err = QuestionBankService._get_owned_bank(bank_id, user_id)
            if err:
                return None, err
            family_ids = [entry.family_id for entry in QuestionBankEntry.find_by_bank(bank._id)]
            query['_id'] = {'$in': family_ids}
        if family_id:
            family_oid = ObjectId(family_id) if ObjectId.is_valid(family_id) else None
            if not family_oid:
                return {'items': [], 'total': 0, 'page': page, 'per_page': per_page}, None
            query['_id'] = family_oid
        if keyword:
            query['title'] = {'$regex': re.escape(keyword.strip()), '$options': 'i'}

        total = db.question_families.count_documents(query)
        cursor = db.question_families.find(query).sort('updated_at', -1).skip((page - 1) * per_page).limit(per_page)
        items = []
        for raw in cursor:
            family = QuestionFamily.__new__(QuestionFamily)
            family.__dict__.update(raw)
            if latest_only:
                version = QuestionVersion.find_by_id(family.latest_version_id) or QuestionVersion.find_latest(family._id)
                if version:
                    items.append(QuestionBankService._version_payload(version, family, user_id))
            else:
                for version in QuestionVersion.find_by_family(family._id):
                    items.append(QuestionBankService._version_payload(version, family, user_id))
        return {'items': items, 'total': total, 'page': page, 'per_page': per_page}, None

    @staticmethod
    def get_question(version_id: str, user_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        version = QuestionBankService._get_version(version_id)
        if not version:
            return None, '题目版本不存在'
        family = QuestionBankService._get_family(version.family_id)
        if not family or not QuestionBankService.can_view(family, user_id):
            return None, '题目不存在或无权访问'
        data = QuestionBankService._version_payload(version, family, user_id)
        data['family'] = QuestionBankService._family_payload(family, user_id)
        return data, None

    @staticmethod
    def get_history(family_id: str, user_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService.can_view(family, user_id):
            return None, '无权查看该题目'
        versions = QuestionVersion.find_by_family(family._id)
        items = [QuestionBankService._version_payload(v, family, user_id) for v in versions]
        for item in items:
            item['is_current'] = item['is_latest']
        return {
            'family': QuestionBankService._family_payload(family, user_id),
            'items': items,
            'total': len(items),
        }, None



    @staticmethod
    def get_usage(family_id: str, user_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        family = QuestionBankService._get_family(family_id)
        if not family:
            return None, '题目不存在'
        if not QuestionBankService.can_view(family, user_id):
            return None, '无权查看该题目的使用情况'
        is_owner = QuestionBankService._is_owner(family, user_id)
        items = []
        for doc in db.questions.find({'bank_family_id': family._id}).sort('created_at', -1):
            survey = db.surveys.find_one({'_id': doc.get('survey_id')})
            if not survey:
                continue
            if not is_owner and str(survey.get('creator_id')) != str(user_id):
                continue
            response_count = db.responses.count_documents({
                'survey_id': survey['_id'],
                'status': 'submitted',
            })
            items.append({
                'survey_id': str(survey['_id']),
                'survey_title': survey.get('title', ''),
                'survey_status': survey.get('status', ''),
                'question_id': str(doc['_id']),
                'bank_version': doc.get('bank_version'),
                'response_count': response_count,
                'creator_id': str(survey.get('creator_id')),
                'is_mine': str(survey.get('creator_id')) == str(user_id),
            })
        return {
            'family': QuestionBankService._family_payload(family, user_id),
            'items': items,
            'total': len(items),
        }, None

    @staticmethod
    def list_banks(user_id: str) -> List[Dict]:
        QuestionBankService.get_or_create_default_bank(user_id)
        items = []
        for bank in QuestionBank.find_by_owner(user_id):
            data = bank.to_dict()
            data['question_count'] = len(QuestionBankEntry.find_by_bank(bank._id))
            items.append(data)
        return items

    @staticmethod
    def create_bank(user_id: str, name: str, description: str = '') -> Tuple[Optional[Dict], Optional[str]]:
        name = (name or '').strip()
        if not name:
            return None, '题库名称不能为空'
        if db.question_banks.find_one({'owner_id': ObjectId(user_id), 'name': name}):
            return None, '同名题库已存在'
        bank = QuestionBank(user_id, name, description=description, is_default=False)
        bank.save()
        data = bank.to_dict()
        data['question_count'] = 0
        return data, None

    @staticmethod
    def update_bank(user_id: str, bank_id: str, data: Dict) -> Tuple[bool, Optional[str]]:
        bank, err = QuestionBankService._get_owned_bank(bank_id, user_id)
        if err:
            return False, err
        update_data = {}
        if 'name' in data:
            name = (data.get('name') or '').strip()
            if not name:
                return False, '题库名称不能为空'
            duplicate = db.question_banks.find_one({
                'owner_id': ObjectId(user_id),
                'name': name,
                '_id': {'$ne': bank._id},
            })
            if duplicate:
                return False, '同名题库已存在'
            update_data['name'] = name
        if 'description' in data:
            update_data['description'] = data.get('description') or ''
        if not update_data:
            return False, '无可更新字段'
        QuestionBank.update(bank._id, update_data)
        return True, None

    @staticmethod
    def delete_bank(user_id: str, bank_id: str) -> Tuple[bool, Optional[str]]:
        bank, err = QuestionBankService._get_owned_bank(bank_id, user_id)
        if err:
            return False, err
        if getattr(bank, 'is_default', False):
            return False, '默认题库不能删除'
        QuestionBankEntry.delete_by_bank(bank._id)
        QuestionBank.delete(bank._id)
        return True, None

    @staticmethod
    def get_bank(user_id: str, bank_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        bank, err = QuestionBankService._get_owned_bank(bank_id, user_id)
        if err:
            return None, err
        data = bank.to_dict()
        data['question_count'] = len(QuestionBankEntry.find_by_bank(bank._id))
        return data, None
