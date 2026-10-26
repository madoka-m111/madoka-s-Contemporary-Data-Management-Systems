def test_start_fill(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题", "type": "text", "order": 0, "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert "response_id" in data["data"]


def test_start_fill_unpublished(client, auth_headers, survey_id):
    res = client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    assert res.status_code == 400


def test_save_draft(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题", "type": "text", "order": 0, "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    rid = res.get_json()["data"]["response_id"]
    res = client.put(f"/api/fill/responses/{rid}/draft", json={
        "answers": {}
    }, headers=auth_headers)
    assert res.status_code == 200


def test_validate_answers(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "必填题",
        "type": "text",
        "order": 0,
        "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.get(f"/api/fill/surveys/{survey_id}/validate?answers={{}}", headers=auth_headers)
    assert res.status_code == 200


def test_submit_survey(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题",
        "type": "text",
        "order": 0,
        "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    rid = res.get_json()["data"]["response_id"]
    res = client.post(f"/api/fill/surveys/{survey_id}/submit", json={
        "answers": {"dummy": "answer"}
    }, headers=auth_headers)
    assert res.status_code in (200, 422)


def test_submit_missing_required(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "必填题",
        "type": "text",
        "order": 0,
        "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    rid = res.get_json()["data"]["response_id"]
    res = client.post(f"/api/fill/surveys/{survey_id}/submit", json={
        "answers": {}
    }, headers=auth_headers)
    assert res.status_code == 422