import uuid


def _make_user(client, prefix='bank_user'):
    username = f'{prefix}_{uuid.uuid4().hex[:8]}'
    client.post('/api/auth/register', json={
        'username': username,
        'email': f'{username}@example.com',
        'password': 'BankPass123',
    })
    res = client.post('/api/auth/login', json={
        'username': username,
        'password': 'BankPass123',
    })
    assert res.status_code == 200, res.get_json()
    return {'Authorization': f"Bearer {res.get_json()['data']['access_token']}"}


def _create_survey(client, headers, title='题目库测试问卷'):
    res = client.post('/api/surveys', json={
        'title': title,
        'description': '第二阶段测试',
        'settings': {'allow_anonymous': True},
    }, headers=headers)
    assert res.status_code == 201, res.get_json()
    return res.get_json()['data']['id']


def _create_bank_question(client, headers, title='你的年龄', **extra):
    payload = {
        'title': title,
        'type': 'single_choice',
        'required': True,
        'options': ['18以下', '18-30', '30以上'],
    }
    payload.update(extra)
    res = client.post('/api/question-bank/questions', json=payload, headers=headers)
    assert res.status_code == 201, res.get_json()
    return res.get_json()['data']


def _add_from_bank(client, headers, survey_id, version_id, **extra):
    payload = {'bank_question_id': version_id}
    payload.update(extra)
    res = client.post(
        f'/api/surveys/{survey_id}/questions/from-bank',
        json=payload, headers=headers,
    )
    assert res.status_code == 201, res.get_json()
    return res.get_json()['data']


def _publish(client, headers, survey_id):
    res = client.post(f'/api/surveys/{survey_id}/publish', headers=headers)
    assert res.status_code == 200, res.get_json()


def _submit(client, survey_id, answers):
    start = client.post(f'/api/fill/surveys/{survey_id}/start', json={})
    assert start.status_code == 201, start.get_json()
    response_id = start.get_json()['data']['response_id']
    res = client.post(f'/api/fill/surveys/{survey_id}/submit', json={
        'answers': answers,
        'response_id': response_id,
    })
    assert res.status_code == 200, res.get_json()


def test_bank_question_versions_history_and_restore(client):
    headers = _make_user(client)
    created = _create_bank_question(client, headers)
    v1_id = created['id']
    family_id = created['family_id']
    assert created['version'] == 1
    assert created['owner_name']

    listed = client.get('/api/question-bank/questions?scope=mine', headers=headers)
    assert listed.status_code == 200
    assert any(item['family_id'] == family_id for item in listed.get_json()['data']['items'])

    response = client.put(f'/api/question-bank/questions/{v1_id}', json={
        'title': '你的年龄段',
        'options': ['18以下', '18-30', '30-50', '50以上'],
        'change_note': '细化年龄段',
    }, headers=headers)
    assert response.status_code == 200, response.get_json()
    v2 = response.get_json()['data']
    assert v2['version'] == 2
    assert v2['parent_version_id'] == v1_id
    assert v2['title'] == '你的年龄段'

    old = client.get(f'/api/question-bank/questions/{v1_id}', headers=headers)
    assert old.status_code == 200
    assert old.get_json()['data']['title'] == '你的年龄'

    history = client.get(f'/api/question-bank/families/{family_id}/history', headers=headers)
    assert history.status_code == 200
    items = history.get_json()['data']['items']
    assert [item['version'] for item in items] == [2, 1]
    assert items[0]['parent_version_id'] == v1_id

    # 以 v1 为基准创建 v3，历史关系应指向 v1，而不是当前最新版
    v3_res = client.post(f'/api/question-bank/questions/{v2["id"]}/versions', json={
        'base_version_id': v1_id,
        'title': '你的年龄（简版）',
    }, headers=headers)
    assert v3_res.status_code == 201, v3_res.get_json()
    v3 = v3_res.get_json()['data']
    assert v3['version'] == 3
    assert v3['parent_version_id'] == v1_id

    restore = client.post(f'/api/question-bank/families/{family_id}/restore', json={
        'version_id': v1_id,
    }, headers=headers)
    assert restore.status_code == 200, restore.get_json()
    v4 = restore.get_json()['data']
    assert v4['version'] == 4
    assert v4['restored_from_version_id'] == v1_id
    assert v4['title'] == '你的年龄'


def test_question_snapshot_is_shared_by_multiple_surveys(client):
    headers = _make_user(client)
    created = _create_bank_question(client, headers)
    v1_id = created['id']
    family_id = created['family_id']

    survey_a = _create_survey(client, headers, 'A问卷')
    survey_b = _create_survey(client, headers, 'B问卷')
    qa = _add_from_bank(client, headers, survey_a, v1_id)
    qb = _add_from_bank(client, headers, survey_b, v1_id)
    assert qa['bank_family_id'] == family_id
    assert qb['bank_version'] == 1
    assert qa['id'] != qb['id']

    usage = client.get(f'/api/question-bank/families/{family_id}/usage', headers=headers)
    assert usage.status_code == 200
    used_surveys = {item['survey_id'] for item in usage.get_json()['data']['items']}
    assert used_surveys == {survey_a, survey_b}

    # 修改题库题目只新增版本，不修改两份问卷中的快照
    v2_res = client.put(f'/api/question-bank/questions/{v1_id}', json={
        'title': '你的年龄（新版）',
    }, headers=headers)
    assert v2_res.status_code == 200
    v2_id = v2_res.get_json()['data']['id']
    for survey_id, qid in ((survey_a, qa['id']), (survey_b, qb['id'])):
        res = client.get(f'/api/surveys/{survey_id}/questions', headers=headers)
        item = next(x for x in res.get_json()['data'] if x['id'] == qid)
        assert item['title'] == '你的年龄'
        assert item['bank_version'] == 1
    assert v2_id != v1_id


def test_published_survey_question_is_immutable_and_can_be_duplicated(client):
    headers = _make_user(client)
    survey_id = _create_survey(client, headers, '已发布问卷')
    q_res = client.post(f'/api/surveys/{survey_id}/questions', json={
        'title': '原题', 'type': 'text', 'required': True,
    }, headers=headers)
    qid = q_res.get_json()['data']['id']
    _publish(client, headers, survey_id)

    assert client.put(f'/api/surveys/questions/{qid}', json={
        'title': '发布后修改',
    }, headers=headers).status_code == 400
    assert client.delete(f'/api/surveys/questions/{qid}', headers=headers).status_code == 400
    assert client.post(f'/api/surveys/{survey_id}/questions', json={
        'title': '发布后新增', 'type': 'text',
    }, headers=headers).status_code == 400
    assert client.put(f'/api/surveys/{survey_id}/questions/reorder', json={
        'question_orders': [{'id': qid, 'order': 2}],
    }, headers=headers).status_code == 400

    # 撤回后仍保持题目锁定，避免已收集答案与题目内容错位
    assert client.post(f'/api/surveys/{survey_id}/unpublish', headers=headers).status_code == 200
    assert client.put(f'/api/surveys/questions/{qid}', json={
        'title': '撤回后修改',
    }, headers=headers).status_code == 400

    duplicate = client.post(f'/api/surveys/{survey_id}/duplicate', headers=headers)
    assert duplicate.status_code == 201, duplicate.get_json()
    copy = duplicate.get_json()['data']
    assert copy['id'] != survey_id
    copy_questions = client.get(f'/api/surveys/{copy["id"]}/questions', headers=headers)
    assert copy_questions.status_code == 200
    copied = copy_questions.get_json()['data'][0]
    assert copied['title'] == '原题'
    assert copied['id'] != qid
    update = client.put(f'/api/surveys/questions/{copied["id"]}', json={
        'title': '副本中可修改',
    }, headers=headers)
    assert update.status_code == 200, update.get_json()
    original = client.get(f'/api/surveys/{survey_id}/questions', headers=headers)
    assert next(x for x in original.get_json()['data'] if x['id'] == qid)['title'] == '原题'


def test_share_question_and_fork(client):
    owner = _make_user(client, 'owner')
    other = _make_user(client, 'student')
    created = _create_bank_question(client, owner, '老师出的题')
    version_id = created['id']
    family_id = created['family_id']
    other_name = client.get('/api/auth/me', headers=other).get_json()['data']['username']

    share = client.post(f'/api/question-bank/families/{family_id}/share', json={
        'username': other_name,
    }, headers=owner)
    assert share.status_code == 200, share.get_json()
    assert any(item['username'] == other_name for item in share.get_json()['data']['shared_users'])

    shared_list = client.get('/api/question-bank/questions?scope=shared', headers=other)
    assert shared_list.status_code == 200
    assert any(item['family_id'] == family_id for item in shared_list.get_json()['data']['items'])

    # 默认“全部可用”应包含共享题；共享题不会自动进入被共享者的题库
    all_list = client.get('/api/question-bank/questions?scope=all', headers=other)
    assert all_list.status_code == 200
    assert any(item['family_id'] == family_id for item in all_list.get_json()['data']['items'])
    banks = client.get('/api/question-bank/banks', headers=other).get_json()['data']
    default_bank = next(bank for bank in banks if bank['is_default'])
    bank_questions = client.get(
        f'/api/question-bank/banks/{default_bank["id"]}/questions', headers=other
    )
    assert bank_questions.status_code == 200
    assert not any(
        item['family_id'] == family_id
        for item in bank_questions.get_json()['data']['items']
    )

    survey_id = _create_survey(client, other, '学生问卷')
    copied = _add_from_bank(client, other, survey_id, version_id)
    assert copied['bank_family_id'] == family_id

    # 被共享者可以选用，但不能直接修改原题
    assert client.put(f'/api/question-bank/questions/{version_id}', json={
        'title': '学生直接改原题',
    }, headers=other).status_code == 400
    fork = client.post(f'/api/question-bank/questions/{version_id}/fork', json={
        'title': '学生自己的题',
    }, headers=other)
    assert fork.status_code == 201, fork.get_json()
    forked = fork.get_json()['data']
    assert forked['family_id'] != family_id
    assert forked['title'] == '学生自己的题'
    assert forked['derived_from_family_id'] == family_id

    # 取消共享后，被共享者不再能看到原题，但已复制的问卷和派生题不受影响
    unshare = client.delete('/api/question-bank/families/%s/share' % family_id,
                            json={'username': other_name}, headers=owner)
    assert unshare.status_code == 200, unshare.get_json()
    after = client.get('/api/question-bank/questions?scope=shared', headers=other)
    assert not any(item['family_id'] == family_id for item in after.get_json()['data']['items'])
    own_survey_questions = client.get(f'/api/surveys/{survey_id}/questions', headers=other)
    assert own_survey_questions.status_code == 200



def test_cross_survey_stats_aggregates_versions(client):
    headers = _make_user(client)
    created = _create_bank_question(client, headers, '跨问卷年龄题')
    v1_id = created['id']
    family_id = created['family_id']

    survey_a = _create_survey(client, headers, '年龄调查A')
    qa = _add_from_bank(client, headers, survey_a, v1_id)
    _publish(client, headers, survey_a)
    _submit(client, survey_a, {qa['id']: '18-30'})

    v2_res = client.put(f'/api/question-bank/questions/{v1_id}', json={
        'title': '跨问卷年龄题（新版）',
        'options': ['18以下', '18-30', '30以上', '不愿透露'],
    }, headers=headers)
    assert v2_res.status_code == 200
    v2 = v2_res.get_json()['data']

    survey_b = _create_survey(client, headers, '年龄调查B')
    qb = _add_from_bank(client, headers, survey_b, v2['id'])
    _publish(client, headers, survey_b)
    _submit(client, survey_b, {qb['id']: '30以上'})

    stats = client.get(f'/api/question-bank/families/{family_id}/stats', headers=headers)
    assert stats.status_code == 200, stats.get_json()
    data = stats.get_json()['data']
    assert data['total_surveys'] == 2
    assert data['total_usage'] == 2
    assert data['total_responses'] == 2
    assert data['total_answers'] == 2
    assert len(data['versions']) == 2
    counts = {item['text']: item['count'] for item in data['aggregate']['options']}
    assert counts['18-30'] == 1
    assert counts['30以上'] == 1
    assert counts['不愿透露'] == 0


def test_bank_management_add_remove_and_default(client):
    headers = _make_user(client)
    created = _create_bank_question(client, headers)
    family_id = created['family_id']

    banks = client.get('/api/question-bank/banks', headers=headers)
    assert banks.status_code == 200
    default_bank = next(b for b in banks.get_json()['data'] if b['is_default'])
    assert default_bank['question_count'] >= 1

    new_bank = client.post('/api/question-bank/banks', json={
        'name': '英语题库',
        'description': '常用英语题',
    }, headers=headers)
    assert new_bank.status_code == 201, new_bank.get_json()
    bank_id = new_bank.get_json()['data']['id']

    add = client.post(f'/api/question-bank/banks/{bank_id}/questions', json={
        'family_id': family_id,
    }, headers=headers)
    assert add.status_code == 200, add.get_json()
    listed = client.get(f'/api/question-bank/banks/{bank_id}/questions', headers=headers)
    assert listed.status_code == 200
    assert listed.get_json()['data']['total'] == 1

    remove = client.delete(f'/api/question-bank/banks/{bank_id}/questions/{family_id}', headers=headers)
    assert remove.status_code == 200
    assert client.get(f'/api/question-bank/banks/{bank_id}/questions', headers=headers).get_json()['data']['total'] == 0

    assert client.delete(f'/api/question-bank/banks/{default_bank["id"]}', headers=headers).status_code == 400
    assert client.delete(f'/api/question-bank/banks/{bank_id}', headers=headers).status_code == 200


def test_shared_question_stats_only_include_own_surveys(client):
    owner = _make_user(client, 'owner_stats')
    other = _make_user(client, 'other_stats')
    created = _create_bank_question(client, owner, '共享统计题')
    family_id = created['family_id']
    version_id = created['id']
    other_name = client.get('/api/auth/me', headers=other).get_json()['data']['username']
    client.post(f'/api/question-bank/families/{family_id}/share', json={
        'username': other_name,
    }, headers=owner)

    owner_survey = _create_survey(client, owner, '作者问卷')
    owner_q = _add_from_bank(client, owner, owner_survey, version_id)
    _publish(client, owner, owner_survey)
    _submit(client, owner_survey, {owner_q['id']: '18以下'})

    other_survey = _create_survey(client, other, '使用者问卷')
    other_q = _add_from_bank(client, other, other_survey, version_id)
    _publish(client, other, other_survey)
    _submit(client, other_survey, {other_q['id']: '30以上'})

    owner_stats = client.get(f'/api/question-bank/families/{family_id}/stats', headers=owner)
    assert owner_stats.status_code == 200
    assert owner_stats.get_json()['data']['total_surveys'] == 2

    other_stats = client.get(f'/api/question-bank/families/{family_id}/stats', headers=other)
    assert other_stats.status_code == 200
    assert other_stats.get_json()['data']['total_surveys'] == 1


def test_public_question_and_batch_add_from_bank(client):
    owner = _make_user(client, 'public_owner')
    other = _make_user(client, 'public_user')
    q1 = _create_bank_question(client, owner, '公开题一')
    q2 = _create_bank_question(client, owner, '公开题二', type='text', options=[])
    family_id = q1['family_id']

    visibility = client.put(f'/api/question-bank/families/{family_id}/visibility', json={
        'is_public': True,
    }, headers=owner)
    assert visibility.status_code == 200, visibility.get_json()
    visibility2 = client.put(f'/api/question-bank/families/{q2["family_id"]}/visibility', json={
        'is_public': True,
    }, headers=owner)
    assert visibility2.status_code == 200, visibility2.get_json()
    shared = client.get('/api/question-bank/questions?scope=shared&latest_only=false', headers=other)
    assert shared.status_code == 200
    assert any(item['family_id'] == family_id for item in shared.get_json()['data']['items'])

    survey_id = _create_survey(client, other, '批量题库问卷')
    res = client.post(f'/api/surveys/{survey_id}/questions/from-bank/batch', json={
        'questions': [
            {'bank_question_id': q1['id'], 'order': 0},
            {'bank_question_id': q2['id'], 'order': 1},
        ],
    }, headers=other)
    assert res.status_code == 201, res.get_json()
    items = res.get_json()['data']
    assert len(items) == 2
    assert items[0]['bank_family_id'] == q1['family_id']
    assert items[1]['bank_family_id'] == q2['family_id']


def test_private_question_cannot_be_used_by_other_user(client):
    owner = _make_user(client, 'private_owner')
    other = _make_user(client, 'private_user')
    q = _create_bank_question(client, owner, '私有题')
    survey_id = _create_survey(client, other, '无权使用')
    res = client.post(f'/api/surveys/{survey_id}/questions/from-bank', json={
        'bank_question_id': q['id'],
    }, headers=other)
    assert res.status_code == 400
    assert '无权' in res.get_json()['message']
