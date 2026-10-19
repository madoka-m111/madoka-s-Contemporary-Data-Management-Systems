def test_get_survey_stats(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "评分",
        "type": "rating",
        "order": 0,
        "required": True,
        "validation": {"min": 1, "max": 5}
    }, headers=auth_headers)
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    client.post(f"/api/fill/surveys/{survey_id}/start", headers=auth_headers)
    res = client.get(f"/api/stats/surveys/{survey_id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["code"] == 200
    assert "total_responses" in data["data"]


def test_get_question_stats(client, auth_headers, survey_id):
    res = client.post(f"/api/surveys/{survey_id}/questions", json={
        "title": "选择题",
        "type": "single_choice",
        "order": 0,
        "required": True,
        "options": ["A", "B", "C"]
    }, headers=auth_headers)
    qid = res.get_json()["data"]["id"]
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.get(f"/api/stats/questions/{qid}", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["code"] == 200


def test_export_responses(client, auth_headers, survey_id):
    client.post(f"/api/surveys/{survey_id}/publish", headers=auth_headers)
    res = client.get(f"/api/stats/surveys/{survey_id}/export?format=json", headers=auth_headers)
    assert res.status_code == 200


def test_stats_no_token(client, survey_id):
    res = client.get(f"/api/stats/surveys/{survey_id}")
    assert res.status_code == 401