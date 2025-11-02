from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app import db
from app.models.user import User
from app.models.call import Call
from app.models.evaluation import Evaluation

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Obter estatísticas gerais do dashboard"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Parâmetros de período
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Base query - operadores veem apenas suas próprias estatísticas
    calls_query = Call.query.filter(Call.created_at >= date_from)
    if current_user.role == 'operator':
        calls_query = calls_query.filter_by(operator_id=current_user_id)
    
    # Total de chamadas
    total_calls = calls_query.count()
    
    # Chamadas por status
    calls_by_status = db.session.query(
        Call.status,
        func.count(Call.id)
    ).filter(Call.created_at >= date_from)
    
    if current_user.role == 'operator':
        calls_by_status = calls_by_status.filter_by(operator_id=current_user_id)
    
    calls_by_status = calls_by_status.group_by(Call.status).all()
    
    # Chamadas por prioridade
    calls_by_priority = db.session.query(
        Call.priority,
        func.count(Call.id)
    ).filter(Call.created_at >= date_from)
    
    if current_user.role == 'operator':
        calls_by_priority = calls_by_priority.filter_by(operator_id=current_user_id)
    
    calls_by_priority = calls_by_priority.group_by(Call.priority).all()
    
    # Chamadas por categoria
    calls_by_category = db.session.query(
        Call.category,
        func.count(Call.id)
    ).filter(Call.created_at >= date_from)
    
    if current_user.role == 'operator':
        calls_by_category = calls_by_category.filter_by(operator_id=current_user_id)
    
    calls_by_category = calls_by_category.group_by(Call.category).all()
    
    # Tempo médio de atendimento
    avg_duration = db.session.query(
        func.avg(Call.duration_seconds)
    ).filter(
        and_(
            Call.created_at >= date_from,
            Call.duration_seconds.isnot(None)
        )
    )
    
    if current_user.role == 'operator':
        avg_duration = avg_duration.filter_by(operator_id=current_user_id)
    
    avg_duration = avg_duration.scalar() or 0
    
    # Estatísticas de avaliações
    evaluations_query = Evaluation.query.join(Call).filter(Evaluation.created_at >= date_from)
    
    if current_user.role == 'operator':
        evaluations_query = evaluations_query.filter(Call.operator_id == current_user_id)
    
    total_evaluations = evaluations_query.count()
    
    # Pontuação média geral
    avg_overall_score = db.session.query(
        func.avg(Evaluation.overall_score)
    ).join(Call).filter(Evaluation.created_at >= date_from)
    
    if current_user.role == 'operator':
        avg_overall_score = avg_overall_score.filter(Call.operator_id == current_user_id)
    
    avg_overall_score = avg_overall_score.scalar() or 0
    
    # Avaliações que requerem coaching
    coaching_needed = db.session.query(Evaluation).join(Call).filter(
        Evaluation.created_at >= date_from,
        Evaluation.requires_coaching == True
    )
    if current_user.role == 'operator':
        coaching_needed = coaching_needed.filter(Call.operator_id == current_user_id)
    coaching_needed = coaching_needed.count()
    
    # Avaliações exemplares
    exemplary_count = db.session.query(Evaluation).join(Call).filter(
        Evaluation.created_at >= date_from,
        Evaluation.is_exemplary == True
    )
    if current_user.role == 'operator':
        exemplary_count = exemplary_count.filter(Call.operator_id == current_user_id)
    exemplary_count = exemplary_count.count()
    
    return jsonify({
        'period_days': days,
        'calls': {
            'total': total_calls,
            'by_status': dict(calls_by_status),
            'by_priority': dict(calls_by_priority),
            'by_category': dict(calls_by_category),
            'avg_duration_seconds': round(avg_duration, 2)
        },
        'evaluations': {
            'total': total_evaluations,
            'avg_overall_score': round(avg_overall_score, 2),
            'coaching_needed': coaching_needed,
            'exemplary': exemplary_count
        }
    }), 200

@dashboard_bp.route('/operator-performance', methods=['GET'])
@jwt_required()
def get_operator_performance():
    """Obter performance dos operadores"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas supervisores e admins podem ver performance de todos
    if current_user.role == 'operator':
        return jsonify({'error': 'Sem permissão para visualizar esta informação'}), 403
    
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Performance por operador
    performance = db.session.query(
        User.id,
        User.full_name,
        func.count(Call.id).label('total_calls'),
        func.avg(Call.duration_seconds).label('avg_duration'),
        func.avg(Evaluation.overall_score).label('avg_score')
    ).join(Call, User.id == Call.operator_id)\
     .outerjoin(Evaluation, Call.id == Evaluation.call_id)\
     .filter(Call.created_at >= date_from)\
     .group_by(User.id, User.full_name)\
     .all()
    
    result = []
    for operator_id, full_name, total_calls, avg_duration, avg_score in performance:
        result.append({
            'operator_id': operator_id,
            'operator_name': full_name,
            'total_calls': total_calls,
            'avg_duration_seconds': round(avg_duration or 0, 2),
            'avg_score': round(avg_score or 0, 2)
        })
    
    return jsonify({
        'period_days': days,
        'operators': result
    }), 200

@dashboard_bp.route('/recent-activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Obter atividades recentes"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    limit = request.args.get('limit', 10, type=int)
    
    # Chamadas recentes
    calls_query = Call.query
    if current_user.role == 'operator':
        calls_query = calls_query.filter_by(operator_id=current_user_id)
    
    recent_calls = calls_query.order_by(Call.created_at.desc()).limit(limit).all()
    
    # Avaliações recentes
    evaluations_query = Evaluation.query.join(Call)
    if current_user.role == 'operator':
        evaluations_query = evaluations_query.filter(Call.operator_id == current_user_id)
    
    recent_evaluations = evaluations_query.order_by(Evaluation.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'recent_calls': [call.to_dict() for call in recent_calls],
        'recent_evaluations': [evaluation.to_dict() for evaluation in recent_evaluations]
    }), 200
