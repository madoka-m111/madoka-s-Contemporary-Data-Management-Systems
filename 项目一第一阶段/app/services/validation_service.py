from typing import Dict, Any, List, Optional, Tuple
from app.models.question import Question


class ValidationService:
    @staticmethod
    def validate_answer(question: Question, answer: Any) -> Tuple[bool, Optional[str]]:
        q_type = question.type
        validation = question.validation or {}
        is_empty = (
            answer is None
            or answer == ''
            or (isinstance(answer, list) and len(answer) == 0)
        )
        if is_empty:
            if question.required:
                return False, '此题为必填项'
            # 多选题设置了“必须选择数”或“最少选择数”时，空答也不满足数量要求
            if q_type == Question.TYPE_MULTIPLE_CHOICE:
                exact_select = validation.get('exact_select')
                if exact_select is not None:
                    return False, f'必须选择 {exact_select} 个选项'
                min_select = validation.get('min_select')
                if min_select is not None and min_select > 0:
                    return False, f'至少需要选择 {min_select} 个选项'
            return True, None

        if q_type in [Question.TYPE_SINGLE_CHOICE, Question.TYPE_DROPDOWN]:
            return ValidationService._validate_single_choice(question, answer)
        elif q_type == Question.TYPE_MULTIPLE_CHOICE:
            return ValidationService._validate_multiple_choice(question, answer)
        elif q_type in [Question.TYPE_TEXT, Question.TYPE_TEXTAREA]:
            return ValidationService._validate_text(question, answer, validation)
        elif q_type == Question.TYPE_NUMBER:
            return ValidationService._validate_number(question, answer, validation)
        elif q_type == Question.TYPE_RATING:
            return ValidationService._validate_rating(question, answer, validation)
        elif q_type == Question.TYPE_DATE:
            return ValidationService._validate_date(question, answer)
        elif q_type == Question.TYPE_FILE:
            return ValidationService._validate_file(question, answer)

        return True, None

    @staticmethod
    def _validate_single_choice(question: Question, answer: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(answer, str):
            return False, '答案格式错误，应为字符串'
        if question.options and answer not in question.options:
            return False, '选项不在有效范围内'
        return True, None

    @staticmethod
    def _validate_multiple_choice(question: Question, answer: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(answer, list):
            return False, '答案格式错误，应为数组'
        if question.options:
            for opt in answer:
                if opt not in question.options:
                    return False, f'选项 {opt} 不在有效范围内'
        validation = question.validation or {}
        exact_select = validation.get('exact_select')
        min_select = validation.get('min_select')
        max_select = validation.get('max_select')
        count = len(answer)
        # “必须选择数”优先于最少/最多选择数，配置时前端会禁止同时设置
        if exact_select is not None and count != exact_select:
            return False, f'必须选择 {exact_select} 个选项'
        if exact_select is None and min_select is not None and count < min_select:
            return False, f'至少需要选择 {min_select} 个选项'
        if exact_select is None and max_select is not None and count > max_select:
            return False, f'最多只能选择 {max_select} 个选项'
        return True, None

    @staticmethod
    def _validate_text(question: Question, answer: Any, validation: Dict) -> Tuple[bool, Optional[str]]:
        if not isinstance(answer, str):
            return False, '答案格式错误，应为字符串'
        min_len = validation.get('min_length', 0)
        max_len = validation.get('max_length', 10000)
        if len(answer) < min_len:
            return False, f'长度不能少于 {min_len} 字符'
        if len(answer) > max_len:
            return False, f'长度不能超过 {max_len} 字符'
        pattern = validation.get('pattern')
        if pattern:
            import re
            if not re.match(pattern, answer):
                return False, '格式不符合要求'
        return True, None

    @staticmethod
    def _validate_number(question: Question, answer: Any, validation: Dict) -> Tuple[bool, Optional[str]]:
        try:
            num = float(answer) if not isinstance(answer, (int, float)) else answer
        except (ValueError, TypeError):
            return False, '答案格式错误，应为数字'
        if validation.get('integer_only') and not float(num).is_integer():
            return False, '必须为整数'
        min_val = validation.get('min')
        max_val = validation.get('max')
        if min_val is not None and num < min_val:
            return False, f'数值不能小于 {min_val}'
        if max_val is not None and num > max_val:
            return False, f'数值不能大于 {max_val}'
        return True, None

    @staticmethod
    def _validate_rating(question: Question, answer: Any, validation: Dict) -> Tuple[bool, Optional[str]]:
        try:
            rating = int(answer)
        except (ValueError, TypeError):
            return False, '评分必须为整数'
        min_val = validation.get('min', 1)
        max_val = validation.get('max', 5)
        if rating < min_val or rating > max_val:
            return False, f'评分范围为 {min_val}-{max_val}'
        return True, None

    @staticmethod
    def _validate_date(question: Question, answer: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(answer, str):
            return False, '日期格式错误'
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', answer):
            return False, '日期格式应为 年-月-日'
        return True, None

    @staticmethod
    def _validate_file(question: Question, answer: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(answer, str):
            return False, '文件标识格式错误'
        return True, None

    @staticmethod
    def validate_all(questions: List[Question], answers: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        from app.services.jump_service import JumpService
        skipped = ValidationService._get_skipped_ids(questions, answers, JumpService)
        errors = {}
        for q in questions:
            qid = str(q._id) if hasattr(q, '_id') else None
            if not qid:
                continue
            if qid in skipped:
                continue
            answer = answers.get(qid)
            valid, msg = ValidationService.validate_answer(q, answer)
            if not valid:
                errors[qid] = msg
        return len(errors) == 0, errors

    @staticmethod
    def get_effective_answers(questions: List[Question], answers: Dict[str, Any]) -> Dict[str, Any]:
        """只保留实际展示给填写者的题目答案，隐藏/跳过题目的陈旧答案不落库、不参与统计。"""
        from app.services.jump_service import JumpService
        skipped = ValidationService._get_skipped_ids(questions, answers, JumpService)
        allowed = {str(q._id) for q in questions if hasattr(q, '_id')}
        return {
            qid: value for qid, value in answers.items()
            if qid in allowed and qid not in skipped
        }

    @staticmethod
    def _get_skipped_ids(questions: List[Question], answers: Dict[str, Any], jump_service) -> set:
        sorted_qs = sorted(questions, key=lambda q: getattr(q, 'order', 0))
        skipped = set()

        def resolve(ref):
            if ref is None or ref == '':
                return None
            for x in sorted_qs:
                if str(getattr(x, '_id', '')) == str(ref):
                    return x
            for x in sorted_qs:
                if str(getattr(x, 'order', '')) == str(ref):
                    return x
            return None

        idx = 0
        while idx < len(sorted_qs):
            q = sorted_qs[idx]
            jl = q.jump_logic or {}
            action = jl.get('action')
            if action in ('hide', 'show'):
                src_q = resolve(jl.get('source_question_id'))
                if src_q is None:
                    idx += 1
                    continue
                src_ans = answers.get(str(src_q._id))
                if src_ans is None or src_ans == '':
                    visible = action == 'hide'
                else:
                    matched = jump_service._check_condition(src_ans, jl.get('condition'), jl.get('value'))
                    visible = (not matched) if action == 'hide' else matched
                if not visible and hasattr(q, '_id'):
                    skipped.add(str(q._id))
                idx += 1
                continue
            if action != 'skip_to':
                idx += 1
                continue
            src_q = resolve(jl.get('source_question_id'))
            tgt_q = resolve(jl.get('target_question_id'))
            if src_q is None or tgt_q is None:
                idx += 1
                continue
            src_ans = answers.get(str(src_q._id))
            if src_ans is None or src_ans == '':
                idx += 1
                continue
            if not jump_service._check_condition(src_ans, jl.get('condition'), jl.get('value')):
                idx += 1
                continue
            src_idx = sorted_qs.index(src_q)
            tgt_idx = sorted_qs.index(tgt_q)
            if tgt_idx <= src_idx:
                idx += 1
                continue
            # 只标记跳过的中间题目，并直接跳到目标题，继续从目标题向后推演
            for k in range(src_idx + 1, tgt_idx):
                if hasattr(sorted_qs[k], '_id'):
                    skipped.add(str(sorted_qs[k]._id))
            idx = tgt_idx
        return skipped