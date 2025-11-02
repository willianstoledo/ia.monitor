from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.evaluation import Evaluation
from app.models.call import Call
from app.models.user import User

evaluations_bp = Blueprint('evaluations', __name__)

@evaluations_bp.route('/', methods=['GET'])
@jwt_required()
def get_evaluations():
    """Listar avaliações com filtros"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Parâmetros de filtro
    call_id = request.args.get('call_id', type=int)
    evaluator_id = request.args.get('evaluator_id', type=int)
    operator_id = request.args.get('operator_id', type=int)
    requires_coaching = request.args.get('requires_coaching')
    is_exemplary = request.args.get('is_exemplary')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Evaluation.query
    
    if call_id:
        query = query.filter_by(call_id=call_id)
    
    if evaluator_id:
        query = query.filter_by(evaluator_id=evaluator_id)
    
    if operator_id:
        # Filtrar por operador através da chamada
        query = query.join(Call).filter(Call.operator_id == operator_id)
    
    if requires_coaching is not None:
        query = query.filter_by(requires_coaching=requires_coaching.lower() == 'true')
    
    if is_exemplary is not None:
        query = query.filter_by(is_exemplary=is_exemplary.lower() == 'true')
    
    # Operadores só veem avaliações de suas próprias chamadas
    if current_user.role == 'operator':
        query = query.join(Call).filter(Call.operator_id == current_user_id)
    
    # Paginação
    pagination = query.order_by(Evaluation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'evaluations': [evaluation.to_dict() for evaluation in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@evaluations_bp.route('/<int:evaluation_id>', methods=['GET'])
@jwt_required()
def get_evaluation(evaluation_id):
    """Obter avaliação por ID"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    evaluation = Evaluation.query.get(evaluation_id)
    
    if not evaluation:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    # Operadores só podem ver avaliações de suas próprias chamadas
    if current_user.role == 'operator':
        call = Call.query.get(evaluation.call_id)
        if call.operator_id != current_user_id:
            return jsonify({'error': 'Sem permissão para visualizar esta avaliação'}), 403
    
    return jsonify(evaluation.to_dict()), 200

@evaluations_bp.route('/', methods=['POST'])
@jwt_required()
def create_evaluation():
    """Criar nova avaliação"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas supervisores e admins podem criar avaliações
    if current_user.role not in ['supervisor', 'admin']:
        return jsonify({'error': 'Sem permissão para criar avaliações'}), 403
    
    data = request.get_json()
    
    # Validar campos obrigatórios
    if 'call_id' not in data:
        return jsonify({'error': 'Campo call_id é obrigatório'}), 400
    
    # Verificar se a chamada existe
    call = Call.query.get(data['call_id'])
    if not call:
        return jsonify({'error': 'Chamada não encontrada'}), 404
    
    # Criar avaliação
    evaluation = Evaluation(
        call_id=data['call_id'],
        evaluator_id=current_user_id,
        greeting_score=data.get('greeting_score'),
        communication_score=data.get('communication_score'),
        problem_solving_score=data.get('problem_solving_score'),
        empathy_score=data.get('empathy_score'),
        procedure_score=data.get('procedure_score'),
        closing_score=data.get('closing_score'),
        positive_points=data.get('positive_points'),
        improvement_points=data.get('improvement_points'),
        general_comments=data.get('general_comments'),
        requires_coaching=data.get('requires_coaching', False),
        is_exemplary=data.get('is_exemplary', False)
    )
    
    # Calcular pontuação geral
    evaluation.calculate_overall_score()
    
    try:
        db.session.add(evaluation)
        db.session.commit()
        return jsonify({
            'message': 'Avaliação criada com sucesso',
            'evaluation': evaluation.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar avaliação', 'details': str(e)}), 500

@evaluations_bp.route('/<int:evaluation_id>', methods=['PUT'])
@jwt_required()
def update_evaluation(evaluation_id):
    """Atualizar avaliação"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas supervisores e admins podem atualizar avaliações
    if current_user.role not in ['supervisor', 'admin']:
        return jsonify({'error': 'Sem permissão para atualizar avaliações'}), 403
    
    evaluation = Evaluation.query.get(evaluation_id)
    
    if not evaluation:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    # Apenas o avaliador original ou admin pode atualizar
    if current_user.role != 'admin' and evaluation.evaluator_id != current_user_id:
        return jsonify({'error': 'Sem permissão para atualizar esta avaliação'}), 403
    
    data = request.get_json()
    
    # Atualizar campos
    score_fields = [
        'greeting_score', 'communication_score', 'problem_solving_score',
        'empathy_score', 'procedure_score', 'closing_score'
    ]
    
    for field in score_fields:
        if field in data:
            setattr(evaluation, field, data[field])
    
    text_fields = ['positive_points', 'improvement_points', 'general_comments']
    for field in text_fields:
        if field in data:
            setattr(evaluation, field, data[field])
    
    if 'requires_coaching' in data:
        evaluation.requires_coaching = data['requires_coaching']
    
    if 'is_exemplary' in data:
        evaluation.is_exemplary = data['is_exemplary']
    
    # Recalcular pontuação geral
    evaluation.calculate_overall_score()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Avaliação atualizada com sucesso',
            'evaluation': evaluation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar avaliação', 'details': str(e)}), 500

@evaluations_bp.route('/<int:evaluation_id>', methods=['DELETE'])
@jwt_required()
def delete_evaluation(evaluation_id):
    """Deletar avaliação"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas admin pode deletar avaliações
    if current_user.role != 'admin':
        return jsonify({'error': 'Sem permissão para deletar avaliações'}), 403
    
    evaluation = Evaluation.query.get(evaluation_id)
    
    if not evaluation:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    try:
        db.session.delete(evaluation)
        db.session.commit()
        return jsonify({'message': 'Avaliação deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar avaliação', 'details': str(e)}), 500
