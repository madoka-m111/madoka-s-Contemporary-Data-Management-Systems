from app.services.jump_service import JumpService


class FakeQuestion:
    def __init__(self, qid, title, jump_logic=None, order=0):
        self._id = qid
        self.title = title
        self.order = order
        self.jump_logic = jump_logic or {}


def test_evaluate_jump_equals_match():
    q = FakeQuestion("q1", "年龄", {
        "condition": "equals",
        "value": "18-30",
        "target_question_id": "q2",
        "action": "skip_to"
    })
    result = JumpService.evaluate_jump_logic(q, "18-30")
    assert result == "q2"


def test_evaluate_jump_equals_no_match():
    q = FakeQuestion("q1", "年龄", {
        "condition": "equals",
        "value": "18-30",
        "target_question_id": "q2",
        "action": "skip_to"
    })
    result = JumpService.evaluate_jump_logic(q, "30-50")
    assert result is None


def test_evaluate_jump_not_equals():
    q = FakeQuestion("q1", "年龄", {
        "condition": "not_equals",
        "value": "18以下",
        "target_question_id": "q3",
        "action": "skip_to"
    })
    assert JumpService.evaluate_jump_logic(q, "18-30") == "q3"
    assert JumpService.evaluate_jump_logic(q, "18以下") is None


def test_evaluate_jump_contains():
    q = FakeQuestion("q1", "兴趣", {
        "condition": "contains",
        "value": "音乐",
        "target_question_id": "q4",
        "action": "skip_to"
    })
    assert JumpService.evaluate_jump_logic(q, ["音乐", "运动"]) == "q4"
    assert JumpService.evaluate_jump_logic(q, ["运动"]) is None


def test_evaluate_jump_greater_than():
    q = FakeQuestion("q1", "评分", {
        "condition": "greater_than",
        "value": "3",
        "target_question_id": "q5",
        "action": "skip_to"
    })
    assert JumpService.evaluate_jump_logic(q, 5) == "q5"
    assert JumpService.evaluate_jump_logic(q, 2) is None


def test_evaluate_jump_less_than():
    q = FakeQuestion("q1", "评分", {
        "condition": "less_than",
        "value": "3",
        "target_question_id": "q6",
        "action": "skip_to"
    })
    assert JumpService.evaluate_jump_logic(q, 1) == "q6"
    assert JumpService.evaluate_jump_logic(q, 4) is None


def test_get_visible_questions_show():
    q1 = FakeQuestion("q1", "是否喜欢运动", {
        "source_question_id": "q0",
        "condition": "equals",
        "value": "是",
        "target_question_id": "q1",
        "action": "show"
    })
    q2 = FakeQuestion("q2", "其他题目", {})
    q0 = FakeQuestion("q0", "运动吗", {})
    questions = [q0, q1, q2]
    visible = JumpService.get_visible_questions(questions, {"q0": "是"})
    visible_ids = [q._id for q in visible]
    assert "q1" in visible_ids


def test_get_visible_questions_hide():
    q1 = FakeQuestion("q1", "敏感题目", {
        "source_question_id": "q0",
        "condition": "equals",
        "value": "是",
        "target_question_id": "q1",
        "action": "hide"
    })
    q2 = FakeQuestion("q2", "正常题目", {})
    q0 = FakeQuestion("q0", "触发题", {})
    questions = [q0, q1, q2]
    visible = JumpService.get_visible_questions(questions, {"q0": "是"})
    visible_ids = [q._id for q in visible]
    assert "q1" not in visible_ids
    assert "q2" in visible_ids


def test_get_next_question_skip():
    q1 = FakeQuestion("q1", "题目1", {
        "condition": "equals",
        "value": "A",
        "target_question_id": "q3",
        "action": "skip_to"
    }, order=0)
    q2 = FakeQuestion("q2", "题目2", {}, order=1)
    q3 = FakeQuestion("q3", "题目3", {}, order=2)
    questions = [q1, q2, q3]
    next_id = JumpService.get_next_question_id(questions, "q1", {"q1": "A"})
    assert next_id == "q3"


def test_get_next_question_normal():
    q1 = FakeQuestion("q1", "题目1", {}, order=0)
    q2 = FakeQuestion("q2", "题目2", {}, order=1)
    q3 = FakeQuestion("q3", "题目3", {}, order=2)
    questions = [q1, q2, q3]
    next_id = JumpService.get_next_question_id(questions, "q1", {})
    assert next_id == "q2"