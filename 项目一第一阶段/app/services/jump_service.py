from typing import Dict, Any, List, Optional, Set
from app.models.question import Question


class JumpService:
    @staticmethod
    def evaluate_jump_logic(question: Question, answer: Any) -> Optional[str]:
        jump_logic = question.jump_logic or {}
        if not jump_logic:
            return None

        condition = jump_logic.get('condition')
        value = jump_logic.get('value')
        target_id = jump_logic.get('target_question_id')
        action = jump_logic.get('action', 'skip_to')

        # hide/show 只控制当前题目自身是否可见，不参与“下一题”跳转；
        # 否则目标题目指向自身时会造成原地打转。
        if action != 'skip_to':
            return None
        if not condition or target_id is None:
            return None

        matched = JumpService._check_condition(answer, condition, value)
        if matched:
            return target_id
        return None

    @staticmethod
    def _check_condition(answer: Any, condition: str, value: Any) -> bool:
        if answer is None:
            return False

        if condition == 'equals':
            return str(answer) == str(value)
        elif condition == 'not_equals':
            return str(answer) != str(value)
        elif condition == 'contains':
            if isinstance(answer, list):
                return str(value) in [str(v) for v in answer]
            return str(value) in str(answer)
        elif condition == 'greater_than':
            try:
                return float(answer) > float(value)
            except (ValueError, TypeError):
                return False
        elif condition == 'less_than':
            try:
                return float(answer) < float(value)
            except (ValueError, TypeError):
                return False
        return False

    @staticmethod
    def get_visible_questions(
        questions: List[Question],
        answers: Dict[str, Any]
    ) -> List[Question]:
        question_map = {str(q._id): q for q in questions if hasattr(q, '_id')}
        visible = set()
        hidden = set()

        for q in questions:
            qid = str(q._id) if hasattr(q, '_id') else None
            if not qid:
                continue

            if JumpService._should_show_question(q, answers, question_map):
                visible.add(qid)
            else:
                hidden.add(qid)

        return [q for q in questions if str(q._id) in visible]

    @staticmethod
    def _should_show_question(
        question: Question,
        answers: Dict[str, Any],
        question_map: Dict[str, Question]
    ) -> bool:
        jump_logic = question.jump_logic or {}
        if not jump_logic:
            return True

        action = jump_logic.get('action', 'skip_to')
        if action == 'show':
            return JumpService._evaluate_show_condition(question, answers, question_map)
        elif action == 'hide':
            return not JumpService._evaluate_show_condition(question, answers, question_map)

        return True

    @staticmethod
    def _evaluate_show_condition(
        question: Question,
        answers: Dict[str, Any],
        question_map: Dict[str, Question]
    ) -> bool:
        jump_logic = question.jump_logic or {}
        source_qid = jump_logic.get('source_question_id')
        if source_qid is None or source_qid == '':
            return False

        source_answer = answers.get(source_qid)
        if source_answer is None:
            # 兼容旧数据：source_question_id 可能存的是题目顺序（order）
            src_q = next(
                (q for q in question_map.values() if str(getattr(q, 'order', '')) == str(source_qid)),
                None
            )
            if src_q is not None:
                source_answer = answers.get(str(src_q._id))
        if source_answer is None:
            return False

        condition = jump_logic.get('condition')
        value = jump_logic.get('value')
        return JumpService._check_condition(source_answer, condition, value)

    @staticmethod
    def get_next_question_id(
        questions: List[Question],
        current_qid: str,
        answers: Dict[str, Any]
    ) -> Optional[str]:
        question_map = {str(q._id): q for q in questions if hasattr(q, '_id')}
        current = question_map.get(current_qid)
        if not current:
            return None

        jump_target = JumpService.evaluate_jump_logic(current, answers.get(current_qid))
        if jump_target:
            if jump_target in question_map:
                return jump_target
            # 兼容旧数据：target_question_id 可能存的是题目顺序（order）
            tgt_q = next(
                (q for q in question_map.values() if str(getattr(q, 'order', '')) == str(jump_target)),
                None
            )
            if tgt_q is not None:
                return str(tgt_q._id)

        sorted_questions = sorted(questions, key=lambda q: q.order)
        current_index = next((i for i, q in enumerate(sorted_questions) if str(q._id) == current_qid), -1)
        if current_index == -1 or current_index + 1 >= len(sorted_questions):
            return None

        next_q = sorted_questions[current_index + 1]
        if JumpService._should_show_question(next_q, answers, question_map):
            return str(next_q._id)

        for i in range(current_index + 2, len(sorted_questions)):
            q = sorted_questions[i]
            if JumpService._should_show_question(q, answers, question_map):
                return str(q._id)

        return None