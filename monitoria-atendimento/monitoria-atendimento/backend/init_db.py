"""Script para inicializar o banco de dados com dados de exemplo"""
import os
import sys
from datetime import datetime, timedelta
import random

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, Call, Evaluation

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    app = create_app('development')
    
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas...")
        db.create_all()
        
        # Verificar se já existem dados
        if User.query.first():
            print("Banco de dados já contém dados. Abortando...")
            return
        
        print("Criando usuários de exemplo...")
        
        # Criar usuários
        admin = User(
            username='admin',
            email='admin@monitoria.com',
            full_name='Administrador do Sistema',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        supervisor = User(
            username='supervisor',
            email='supervisor@monitoria.com',
            full_name='Maria Supervisora',
            role='supervisor',
            is_active=True
        )
        supervisor.set_password('supervisor123')
        db.session.add(supervisor)
        
        # Criar operadores
        operators = []
        operator_names = [
            'João Silva',
            'Ana Santos',
            'Pedro Oliveira',
            'Carla Souza',
            'Lucas Ferreira'
        ]
        
        for i, name in enumerate(operator_names, 1):
            username = name.lower().replace(' ', '.')
            operator = User(
                username=username,
                email=f'{username}@monitoria.com',
                full_name=name,
                role='operator',
                is_active=True
            )
            operator.set_password('operator123')
            operators.append(operator)
            db.session.add(operator)
        
        db.session.commit()
        print(f"Criados {len(operators) + 2} usuários")
        
        print("Criando chamadas de exemplo...")
        
        # Criar chamadas
        categories = ['suporte', 'vendas', 'reclamacao', 'duvida', 'cancelamento']
        priorities = ['low', 'medium', 'high', 'urgent']
        statuses = ['open', 'in_progress', 'resolved', 'closed']
        
        calls = []
        for i in range(50):
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            call = Call(
                protocol=f'CALL-{created_at.strftime("%Y%m%d")}-{str(i).zfill(4)}',
                operator_id=random.choice(operators).id,
                customer_name=f'Cliente {i+1}',
                customer_phone=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                customer_email=f'cliente{i+1}@email.com',
                subject=f'Assunto da chamada {i+1}',
                description=f'Descrição detalhada da chamada {i+1}',
                category=random.choice(categories),
                priority=random.choice(priorities),
                status=random.choice(statuses),
                duration_seconds=random.randint(60, 1800),
                notes=f'Notas sobre a chamada {i+1}',
                created_at=created_at,
                updated_at=created_at
            )
            
            if call.status == 'closed':
                call.closed_at = created_at + timedelta(hours=random.randint(1, 48))
            
            calls.append(call)
            db.session.add(call)
        
        db.session.commit()
        print(f"Criadas {len(calls)} chamadas")
        
        print("Criando avaliações de exemplo...")
        
        # Criar avaliações para algumas chamadas
        evaluations = []
        for call in random.sample(calls, 30):
            evaluation = Evaluation(
                call_id=call.id,
                evaluator_id=supervisor.id,
                greeting_score=random.randint(3, 5),
                communication_score=random.randint(3, 5),
                problem_solving_score=random.randint(2, 5),
                empathy_score=random.randint(3, 5),
                procedure_score=random.randint(3, 5),
                closing_score=random.randint(3, 5),
                positive_points='Atendimento cordial e profissional',
                improvement_points='Pode melhorar na agilidade',
                general_comments='Bom atendimento no geral',
                requires_coaching=random.choice([True, False]),
                is_exemplary=random.choice([True, False]),
                created_at=call.created_at + timedelta(hours=random.randint(1, 24))
            )
            evaluation.calculate_overall_score()
            evaluations.append(evaluation)
            db.session.add(evaluation)
        
        db.session.commit()
        print(f"Criadas {len(evaluations)} avaliações")
        
        print("\n" + "="*50)
        print("Banco de dados inicializado com sucesso!")
        print("="*50)
        print("\nCredenciais de acesso:")
        print("\nAdmin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nSupervisor:")
        print("  Username: supervisor")
        print("  Password: supervisor123")
        print("\nOperadores:")
        for name in operator_names:
            username = name.lower().replace(' ', '.')
            print(f"  Username: {username}")
            print(f"  Password: operator123")
        print("="*50)

if __name__ == '__main__':
    init_database()
