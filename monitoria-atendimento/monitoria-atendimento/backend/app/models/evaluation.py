from datetime import datetime
from app import db

class Evaluation(db.Model):
    """Modelo de avaliação de atendimento"""
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id'), nullable=False, index=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Critérios de avaliação (escala de 1 a 5)
    greeting_score = db.Column(db.Integer)  # Saudação e apresentação
    communication_score = db.Column(db.Integer)  # Clareza e comunicação
    problem_solving_score = db.Column(db.Integer)  # Resolução do problema
    empathy_score = db.Column(db.Integer)  # Empatia e cordialidade
    procedure_score = db.Column(db.Integer)  # Seguimento de procedimentos
    closing_score = db.Column(db.Integer)  # Encerramento adequado
    
    # Pontuação geral (calculada automaticamente)
    overall_score = db.Column(db.Float)
    
    # Feedback textual
    positive_points = db.Column(db.Text)
    improvement_points = db.Column(db.Text)
    general_comments = db.Column(db.Text)
    
    # Flags
    requires_coaching = db.Column(db.Boolean, default=False)
    is_exemplary = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def calculate_overall_score(self):
        """Calcula a pontuação geral baseada nos critérios"""
        scores = [
            self.greeting_score,
            self.communication_score,
            self.problem_solving_score,
            self.empathy_score,
            self.procedure_score,
            self.closing_score
        ]
        
        # Remove None values
        valid_scores = [s for s in scores if s is not None]
        
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
        else:
            self.overall_score = 0.0
        
        return self.overall_score
    
    def to_dict(self):
        """Converte a avaliação para dicionário"""
        return {
            'id': self.id,
            'call_id': self.call_id,
            'evaluator_id': self.evaluator_id,
            'evaluator_name': self.evaluator.full_name if self.evaluator else None,
            'greeting_score': self.greeting_score,
            'communication_score': self.communication_score,
            'problem_solving_score': self.problem_solving_score,
            'empathy_score': self.empathy_score,
            'procedure_score': self.procedure_score,
            'closing_score': self.closing_score,
            'overall_score': self.overall_score,
            'positive_points': self.positive_points,
            'improvement_points': self.improvement_points,
            'general_comments': self.general_comments,
            'requires_coaching': self.requires_coaching,
            'is_exemplary': self.is_exemplary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Evaluation {self.id} for Call {self.call_id}>'
