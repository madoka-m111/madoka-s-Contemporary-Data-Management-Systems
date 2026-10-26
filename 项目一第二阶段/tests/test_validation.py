from app.services.validation_service import ValidationService


class FakeQuestion:
    def __init__(self, qid, q_type, required=False, options=None, validation=None, jump_logic=None):
        self._id = qid
        self.type = q_type
        self.required = required
        self.options = options or []
        self.validation = validation or {}
        self.jump_logic = jump_logic or {}


def test_validate_required_empty():
    q = FakeQuestion("q1", "text", required=True)
    valid, msg = ValidationService.validate_answer(q, None)
    assert valid is False
    assert "必填" in msg


def test_validate_required_not_empty():
    q = FakeQuestion("q1", "text", required=True)
    valid, msg = ValidationService.validate_answer(q, "hello")
    assert valid is True


def test_validate_optional_empty():
    q = FakeQuestion("q1", "text", required=False)
    valid, msg = ValidationService.validate_answer(q, "")
    assert valid is True


def test_validate_single_choice_valid():
    q = FakeQuestion("q1", "single_choice", options=["A", "B", "C"])
    valid, msg = ValidationService.validate_answer(q, "A")
    assert valid is True


def test_validate_single_choice_invalid():
    q = FakeQuestion("q1", "single_choice", options=["A", "B", "C"])
    valid, msg = ValidationService.validate_answer(q, "D")
    assert valid is False


def test_validate_multiple_choice_valid():
    q = FakeQuestion("q1", "multiple_choice", options=["A", "B", "C"])
    valid, msg = ValidationService.validate_answer(q, ["A", "B"])
    assert valid is True


def test_validate_multiple_choice_min_max_count():
    q = FakeQuestion("q1", "multiple_choice", options=["A", "B", "C"], validation={"min_select": 2, "max_select": 3})
    valid, msg = ValidationService.validate_answer(q, ["A", "B"])
    assert valid is True
    valid, msg = ValidationService.validate_answer(q, ["A"])
    assert valid is False
    assert "至少" in msg
    valid, msg = ValidationService.validate_answer(q, ["A", "B", "C"])
    assert valid is True
    q.validation = {"min_select": 2, "max_select": 2}
    valid, msg = ValidationService.validate_answer(q, ["A", "B", "C"])
    assert valid is False
    assert "最多" in msg


def test_validate_multiple_choice_exact_count():
    q = FakeQuestion("q1", "multiple_choice", options=["A", "B", "C"], validation={"exact_select": 2})
    valid, msg = ValidationService.validate_answer(q, ["A", "B"])
    assert valid is True
    valid, msg = ValidationService.validate_answer(q, ["A"])
    assert valid is False
    assert "必须选择 2" in msg
    valid, msg = ValidationService.validate_answer(q, ["A", "B", "C"])
    assert valid is False
    assert "必须选择 2" in msg
    # 历史或直接 API 写入的冲突配置中，exact_select 优先于 min/max
    q.validation = {"exact_select": 2, "min_select": 3}
    valid, msg = ValidationService.validate_answer(q, ["A", "B"])
    assert valid is True


def test_validate_multiple_choice_count_requires_answer_when_optional():
    q = FakeQuestion("q1", "multiple_choice", options=["A", "B"], validation={"min_select": 2})
    valid, msg = ValidationService.validate_answer(q, [])
    assert valid is False
    assert "至少" in msg

    q.validation = {"exact_select": 2}
    valid, msg = ValidationService.validate_answer(q, [])
    assert valid is False
    assert "必须选择 2" in msg

    q.validation = {"max_select": 2}
    valid, msg = ValidationService.validate_answer(q, [])
    assert valid is True


def test_validate_text_min_length():
    q = FakeQuestion("q1", "text", validation={"min_length": 5})
    valid, msg = ValidationService.validate_answer(q, "hi")
    assert valid is False


def test_validate_text_max_length():
    q = FakeQuestion("q1", "text", validation={"max_length": 3})
    valid, msg = ValidationService.validate_answer(q, "hello")
    assert valid is False


def test_validate_number_range():
    q = FakeQuestion("q1", "number", validation={"min": 0, "max": 100})
    valid, msg = ValidationService.validate_answer(q, 50)
    assert valid is True
    valid, msg = ValidationService.validate_answer(q, 150)
    assert valid is False


def test_validate_number_integer_only():
    q = FakeQuestion("q1", "number", validation={"min": 1, "max": 10, "integer_only": True})
    valid, msg = ValidationService.validate_answer(q, "3")
    assert valid is True
    valid, msg = ValidationService.validate_answer(q, "3.5")
    assert valid is False
    assert "整数" in msg
    valid, msg = ValidationService.validate_answer(q, 11)
    assert valid is False


def test_validate_rating_range():
    q = FakeQuestion("q1", "rating", validation={"min": 1, "max": 5})
    valid, msg = ValidationService.validate_answer(q, 3)
    assert valid is True
    valid, msg = ValidationService.validate_answer(q, 6)
    assert valid is False


def test_validate_all():
    q1 = FakeQuestion("q1", "text", required=True)
    q2 = FakeQuestion("q2", "single_choice", options=["A", "B"])
    questions = [q1, q2]
    valid, errors = ValidationService.validate_all(questions, {"q1": "hello", "q2": "A"})
    assert valid is True
    assert errors == {}

    valid, errors = ValidationService.validate_all(questions, {"q1": "", "q2": "C"})
    assert valid is False
    assert "q1" in errors
    assert "q2" in errors