from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.stats_service import StatsService
from app.services.survey_service import SurveyService
from app.utils.response_util import success_response, error_response
import io

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')


@stats_bp.route('/surveys/<survey_id>', methods=['GET'])
@jwt_required()
def get_survey_stats(survey_id):
    user_id = get_jwt_identity()
    survey = SurveyService.get_survey(survey_id)
    if not survey:
        return error_response('问卷不存在', 404)
    if str(survey.creator_id) != user_id:
        return error_response('无权限查看统计', 403)

    stats = StatsService.get_survey_stats(survey_id)
    return success_response(stats)


@stats_bp.route('/questions/<question_id>', methods=['GET'])
@jwt_required()
def get_question_stats(question_id):
    user_id = get_jwt_identity()
    from app.models.question import Question
    question = Question.find_by_id(question_id)
    if not question:
        return error_response('题目不存在', 404)

    survey = SurveyService.get_survey(str(question.survey_id))
    if not survey or str(survey.creator_id) != user_id:
        return error_response('无权限查看统计', 403)

    stats = StatsService.get_question_stats(question_id)
    return success_response(stats)


@stats_bp.route('/surveys/<survey_id>/export', methods=['GET'])
@jwt_required()
def export_responses(survey_id):
    user_id = get_jwt_identity()
    survey = SurveyService.get_survey(survey_id)
    if not survey:
        return error_response('问卷不存在', 404)
    if str(survey.creator_id) != user_id:
        return error_response('无权限导出', 403)

    format = request.args.get('format', 'json')
    data = StatsService.export_responses(survey_id, format)

    if format == 'csv':
        return send_file(
            io.BytesIO(data.encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'survey_{survey_id}_export.csv'
        )
    elif format == 'xlsx':
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Responses'

        questions = [q for q in __import__('app.models.question', fromlist=['Question']).Question.find_by_survey_id(survey_id)]
        headers = ['response_id', 'user_id', 'email', 'submitted_at'] + [q.title for q in questions]
        ws.append(headers)

        responses = __import__('app.models.response', fromlist=['Response']).Response.find_by_survey(survey_id, __import__('app.models.response', fromlist=['Response']).Response.STATUS_SUBMITTED)
        for r in responses:
            row = [str(r._id), str(r.user_id) if r.user_id else '', getattr(r, 'email', '') or '', r.submitted_at.isoformat() if r.submitted_at else '']
            for q in questions:
                qid = str(q._id)
                ans = r.answers.get(qid, '')
                if isinstance(ans, list):
                    ans = '; '.join(str(v) for v in ans)
                row.append(str(ans))
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'survey_{survey_id}_export.xlsx'
        )

    return success_response(data)