from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Listar todos os usuários"""
    role = request.args.get('role')
    is_active = request.args.get('is_active')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    if is_active is not None:
        query = query.filter_by(is_active=is_active.lower() == 'true')
    
    users = query.order_by(User.full_name).all()
    
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Obter usuário por ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Atualizar usuário"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Verificar permissões (apenas admin ou o próprio usuário)
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Sem permissão para atualizar este usuário'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos permitidos
    if 'full_name' in data:
        user.full_name = data['full_name']
    
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 409
        user.email = data['email']
    
    # Apenas admin pode alterar role e is_active
    if current_user.role == 'admin':
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Usuário atualizado com sucesso',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar usuário', 'details': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Desativar usuário (soft delete)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))
    
    # Apenas admin pode desativar usuários
    if current_user.role != 'admin':
        return jsonify({'error': 'Sem permissão para desativar usuários'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    user.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'Usuário desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao desativar usuário', 'details': str(e)}), 500
