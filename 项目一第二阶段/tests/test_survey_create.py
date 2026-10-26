def test_create_survey(client, auth_headers):
    res = client.post("/api/surveys", json={
        "title": "满意度调查",
        "description": "请对服务进行评分",
        "settings": {"allow_anonymous": True}
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["code"] == 201
    assert data["data"]["title"] == "满意度调查"
    assert "id" in data["data"]


def test_create_survey_missing_title(client, auth_headers):
    res = client.post("/api/surveys", json={
        "description": "无标题"
    }, headers=auth_headers)
    assert res.status_code == 400


def test_get_my_surveys(client, auth_headers, survey_id):
    res = client.get("/api/surveys", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["code"] == 200
    assert data["data"]["total"] >= 1
    assert any(s["id"] == survey_id for s in data["data"]["items"])


def test_get_my_surveys_no_token(client):
    res = client.get("/api/surveys")
    assert res.status_code == 401


def test_get_public_surveys(client, auth_headers, survey_id):
    res = client.get("/api/surveys/public")
    assert res.status_code == 200


def test_get_survey_detail(client, auth_headers, survey_id):
    res = client.get(f"/api/surveys/{survey_id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["code"] == 200
    assert data["data"]["id"] == survey_id


def test_get_survey_invalid_id_returns_404(client, auth_headers):
    res = client.get("/api/surveys/null", headers=auth_headers)
    assert res.status_code == 404


def test_update_survey(client, auth_headers, survey_id):
    res = client.put(f"/api/surveys/{survey_id}", json={
        "title": "更新后的标题"
    }, headers=auth_headers)
    assert res.status_code == 200


def test_publish_survey(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题", "type": "text", "order": 0, "required": True
    }, headers=auth_headers)
    res = client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    assert res.status_code == 200


def test_close_survey(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "测试题", "type": "text", "order": 0, "required": True
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.post(f"/api/surveys/{survey_id}/close", headers=auth_headers)
    assert res.status_code == 200


def test_delete_survey(client, auth_headers):
    res = client.post("/api/surveys", json={
        "title": "待删除问卷"
    }, headers=auth_headers)
    sid = res.get_json()["data"]["id"]
    res = client.delete(f"/api/surveys/{sid}", headers=auth_headers)
    assert res.status_code == 200