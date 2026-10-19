from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from collections import Counter
from app.models.response import Response
from app.models.question import Question
from app import db


class StatsService:
    @staticmethod
    def get_survey_stats(survey_id: str) -> Dict[str, Any]:
        pipeline = [
            {'$match': {'survey_id': ObjectId(survey_id), 'status': Response.STATUS_SUBMITTED}},
            {'$group': {
                '_id': None,
                'total': {'$sum': 1},
            }}
        ]
        result = list(db.responses.aggregate(pipeline))
        base = result[0] if result else {'total': 0}

        # 在 Python 端计算平均耗时，避免 MongoDB 聚合中 $subtract 日期嵌套 $avg 的兼容性问题
        responses = list(db.responses.find({
            'survey_id': ObjectId(survey_id),
            'status': Response.STATUS_SUBMITTED
        }))
        durations = []
        for r in responses:
            started = r.get('started_at')
            submitted = r.get('submitted_at')
            if started and submitted:
                try:
                    durations.append((submitted - started).total_seconds())
                except (TypeError, AttributeError):
                    pass
        avg_duration = round(sum(durations) / len(durations), 1) if durations else 0

        questions = Question.find_by_survey_id(survey_id)
        question_stats = []
        for q in questions:
            qs = StatsService.get_question_stats(str(q._id))
            question_stats.append(qs)

        daily_trend = StatsService._get_daily_trend(survey_id)

        answered_total = base.get('total', 0)
        started_total = db.responses.count_documents({'survey_id': ObjectId(survey_id)})
        completion_rate = round(answered_total / started_total, 4) if started_total else 0.0

        return {
            'total_responses': answered_total,
            'completion_rate': completion_rate,
            'avg_duration_seconds': avg_duration,
            'daily_trend': daily_trend,
            'question_stats': question_stats
        }

    @staticmethod
    def get_question_stats(question_id: str) -> Dict[str, Any]:
        question = Question.find_by_id(question_id)
        if not question:
            return {}

        pipeline = [
            {'$match': {
                'survey_id': question.survey_id,
                f'answers.{question_id}': {'$exists': True},
                'status': Response.STATUS_SUBMITTED
            }},
            {'$project': {'answer': f'$answers.{question_id}'}}
        ]
        results = list(db.responses.aggregate(pipeline))

        total_submitted = db.responses.count_documents({'survey_id': question.survey_id, 'status': Response.STATUS_SUBMITTED})
        answered = len(results)
        skip_count = total_submitted - answered

        base = {
            'question_id': question_id,
            'title': question.title,
            'type': question.type,
            'order': question.order,
            'required': question.required,
            'total_answers': answered,
            'skip_count': skip_count
        }

        if question.type in [Question.TYPE_SINGLE_CHOICE, Question.TYPE_MULTIPLE_CHOICE, Question.TYPE_DROPDOWN]:
            return {**base, **StatsService._stats_choice(question, results, answered)}
        elif question.type in [Question.TYPE_TEXT, Question.TYPE_TEXTAREA]:
            return {**base, **StatsService._stats_text(results)}
        elif question.type in [Question.TYPE_NUMBER, Question.TYPE_RATING]:
            return {**base, **StatsService._stats_numeric(question, results)}
        elif question.type == Question.TYPE_DATE:
            return {**base, **StatsService._stats_date(results)}

        return base

    @staticmethod
    def _stats_choice(question: Question, results: List[Dict], answered: int) -> Dict:
        options = question.options or []
        counter = Counter()

        for r in results:
            ans = r.get('answer')
            if question.type == Question.TYPE_MULTIPLE_CHOICE and isinstance(ans, list):
                for opt in ans:
                    counter[str(opt)] += 1
            elif ans is not None:
                counter[str(ans)] += 1

        option_stats = []
        for opt in options:
            count = counter.get(opt, 0)
            option_stats.append({
                'text': opt,
                'count': count,
                'percentage': round(count / answered * 100, 1) if answered else 0
            })

        return {'options': option_stats}

    @staticmethod
    def _stats_text(results: List[Dict]) -> Dict:
        answers = [str(r.get('answer', '')) for r in results if r.get('answer')]
        return {'answers': answers}

    @staticmethod
    def _stats_numeric(question: Question, results: List[Dict]) -> Dict:
        values = []
        for r in results:
            ans = r.get('answer')
            try:
                values.append(float(ans))
            except (ValueError, TypeError):
                pass

        if not values:
            return {'avg': 0, 'min': 0, 'max': 0, 'median': 0, 'distribution': []}

        values.sort()
        n = len(values)
        avg = sum(values) / n
        median = values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2

        min_v, max_v = values[0], values[-1]
        ranges = StatsService._create_ranges(min_v, max_v, 5)
        dist = []
        for idx, (r_min, r_max) in enumerate(ranges):
            is_last = idx == len(ranges) - 1
            # 除最后一档外使用左闭右开，避免边界值被重复计数
            cnt = sum(1 for v in values if r_min <= v < r_max or (is_last and v == r_max))
            dist.append({'range': f'{r_min:.0f}-{r_max:.0f}', 'count': cnt})

        return {
            'avg': round(avg, 2),
            'min': min_v,
            'max': max_v,
            'median': median,
            'distribution': dist
        }

    @staticmethod
    def _stats_date(results: List[Dict]) -> Dict:
        dates = [r.get('answer') for r in results if r.get('answer')]
        counter = Counter(dates)
        return {
            'distribution': [{'date': d, 'count': c} for d, c in counter.most_common()]
        }

    @staticmethod
    def _create_ranges(min_v: float, max_v: float, bins: int) -> List[tuple]:
        if min_v == max_v:
            return [(min_v, max_v)]
        step = (max_v - min_v) / bins
        ranges = []
        for i in range(bins):
            r_min = min_v + i * step
            r_max = min_v + (i + 1) * step
            ranges.append((r_min, r_max))
        return ranges

    @staticmethod
    def _get_daily_trend(survey_id: str, days: int = 30) -> List[Dict]:
        start_date = datetime.utcnow() - timedelta(days=days)
        pipeline = [
            {'$match': {
                'survey_id': ObjectId(survey_id),
                'status': Response.STATUS_SUBMITTED,
                'submitted_at': {'$gte': start_date}
            }},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$submitted_at'}},
                'count': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        results = list(db.responses.aggregate(pipeline))
        return [{'date': r['_id'], 'count': r['count']} for r in results]

    @staticmethod
    def export_responses(survey_id: str, format: str = 'json') -> Any:
        responses = Response.find_by_survey(survey_id, Response.STATUS_SUBMITTED)
        questions = Question.find_by_survey_id(survey_id)
        q_map = {str(q._id): q for q in questions}

        if format == 'csv':
            import csv
            import io
            output = io.StringIO()
            headers = ['response_id', 'user_id', 'email', 'submitted_at'] + [q.title for q in questions]
            writer = csv.writer(output)
            writer.writerow(headers)

            for r in responses:
                row = [str(r._id), str(r.user_id) if r.user_id else '', getattr(r, 'email', '') or '', r.submitted_at.isoformat() if r.submitted_at else '']
                for q in questions:
                    qid = str(q._id)
                    ans = r.answers.get(qid, '')
                    if isinstance(ans, list):
                        ans = '; '.join(str(v) for v in ans)
                    row.append(str(ans))
                writer.writerow(row)
            return output.getvalue()

        return [r.to_dict() for r in responses]