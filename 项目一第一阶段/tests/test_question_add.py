def test_add_question(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "您的年龄段？",
        "type": "single_choice",
        "order": 0,
        "required": True,
        "options": ["18以下", "18-30", "30-50", "50以上"]
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["code"] == 201
    assert data["data"]["title"] == "您的年龄段？"
    assert "id" in data["data"]


def test_add_question_missing_fields(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "只标题"
    }, headers=auth_headers)
    assert res.status_code == 400


def test_add_question_published_survey(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "已有题目", "type": "text", "order": 0, "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "新题目",
        "type": "text"
    }, headers=auth_headers)
    assert res.status_code == 400


def test_batch_add_questions(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions/batch", json={
        "questions": [
            {"title": "题目1", "type": "text", "order": 0},
            {"title": "题目2", "type": "number", "order": 1}
        ]
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert len(data["data"]) == 2


def test_get_questions(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题目",
        "type": "text",
        "order": 0
    }, headers=auth_headers)
    res = client.get(f"/api/surveys/{survey_id}/questions", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["data"]) >= 1


def test_update_question(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "原题目",
        "type": "text",
        "order": 0
    }, headers=auth_headers)
    qid = res.get_json()["data"]["id"]
    res = client.put(f"/api/surveys/questions/{qid}", json={
        "title": "修改后的题目"
    }, headers=auth_headers)
    assert res.status_code == 200


def test_delete_question(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "待删除题目",
        "type": "text",
        "order": 0
    }, headers=auth_headers)
    qid = res.get_json()["data"]["id"]
    res = client.delete(f"/api/surveys/questions/{qid}", headers=auth_headers)
    assert res.status_code == 200


def test_reorder_questions(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "题目A", "type": "text", "order": 0
    }, headers=auth_headers)
    res2 = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "题目B", "type": "text", "order": 1
    }, headers=auth_headers)
    q1 = res.get_json()["data"]["id"]
    q2 = res2.get_json()["data"]["id"]
    res = client.put(f"/api/surveys/{survey_id}/questions/reorder", json={
        "question_orders": [
            {"id": q2, "order": 0},
            {"id": q1, "order": 1}
        ]
    }, headers=auth_headers)
    assert res.status_code == 200