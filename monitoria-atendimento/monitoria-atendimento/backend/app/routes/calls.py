from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.call import Call
from app.models.user import User
import uuid

calls_bp = Blueprint('calls', __name__)

def generate_protocol():
    """Gera um protocolo único para a chamada"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_suffix = str(uuid.uuid4())[:6].upper()
    return f'CALL-{timestamp}-{random_suffix}'

@calls_bp.route('/', methods=['GET'])
@jwt_required()
def get_calls():
    """Listar chamadas com filtros"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Parâmetros de filtro
    operator_id = request.args.get('operator_id', type=int)
    status = request.args.get('status')
    category = request.args.get('category')
    priority = request.args.get('priority')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Call.query
    
    # Operadores só veem suas próprias chamadas
    if current_user.role == 'operator':
        query = query.filter_by(operator_id=current_user_id)
    elif operator_id:
        query = query.filter_by(operator_id=operator_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if category:
        query = query.filter_by(category=category)
    
    if priority:
        query = query.filter_by(priority=priority)
    
    if date_from:
        try:
            date_from_obj = datetime.fromisoformat(date_from)
            query = query.filter(Call.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.fromisoformat(date_to)
            query = query.filter(Call.created_at <= date_to_obj)
        except ValueError:
            pass
    
    # Paginação
    pagination = query.order_by(Call.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'calls': [call.to_dict() for call in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@calls_bp.route('/<int:call_id>', methods=['GET'])
@jwt_required()
def get_call(call_id):
    """Obter chamada por ID"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    call = Call.query.get(call_id)
    
    if not call:
        return jsonify({'error': 'Chamada não encontrada'}), 404
    
    # Operadores só podem ver suas próprias chamadas
    if current_user.role == 'operator' and call.operator_id != current_user_id:
        return jsonify({'error': 'Sem permissão para visualizar esta chamada'}), 403
    
    return jsonify(call.to_dict(include_evaluations=True)), 200

@calls_bp.route('/', methods=['POST'])
@jwt_required()
def create_call():
    """Criar nova chamada"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar campos obrigatórios
    required_fields = ['customer_name', 'subject']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    # Criar chamada
    call = Call(
        protocol=generate_protocol(),
        operator_id=data.get('operator_id', current_user_id),
        customer_name=data['customer_name'],
        customer_phone=data.get('customer_phone'),
        customer_email=data.get('customer_email'),
        subject=data['subject'],
        description=data.get('description'),
        category=data.get('category'),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        duration_seconds=data.get('duration_seconds'),
        recording_url=data.get('recording_url'),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(call)
        db.session.commit()
        return jsonify({
            'message': 'Chamada criada com sucesso',
            'call': call.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar chamada', 'details': str(e)}), 500

@calls_bp.route('/<int:call_id>', methods=['PUT'])
@jwt_required()
def update_call(call_id):
    """Atualizar chamada"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    call = Call.query.get(call_id)
    
    if not call:
        return jsonify({'error': 'Chamada não encontrada'}), 404
    
    # Operadores só podem atualizar suas próprias chamadas
    if current_user.role == 'operator' and call.operator_id != current_user_id:
        return jsonify({'error': 'Sem permissão para atualizar esta chamada'}), 403
    
    data = request.get_json()
    
    # Atualizar campos
    updatable_fields = [
        'customer_name', 'customer_phone', 'customer_email',
        'subject', 'description', 'category', 'priority',
        'status', 'duration_seconds', 'recording_url', 'notes'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(call, field, data[field])
    
    # Se status mudou para closed, registrar data de fechamento
    if 'status' in data and data['status'] == 'closed' and not call.closed_at:
        call.closed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Chamada atualizada com sucesso',
            'call': call.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar chamada', 'details': str(e)}), 500

@calls_bp.route('/<int:call_id>', methods=['DELETE'])
@jwt_required()
def delete_call(call_id):
    """Deletar chamada"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas admin e supervisor podem deletar
    if current_user.role not in ['admin', 'supervisor']:
        return jsonify({'error': 'Sem permissão para deletar chamadas'}), 403
    
    call = Call.query.get(call_id)
    
    if not call:
        return jsonify({'error': 'Chamada não encontrada'}), 404
    
    try:
        db.session.delete(call)
        db.session.commit()
        return jsonify({'message': 'Chamada deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar chamada', 'details': str(e)}), 500
