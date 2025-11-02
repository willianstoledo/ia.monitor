from datetime import datetime
from app import db

class Call(db.Model):
    """Modelo de chamada/atendimento"""
    __tablename__ = 'calls'
    
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(50), unique=True, nullable=False, index=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(120))
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # suporte, vendas, reclamacao, etc
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    duration_seconds = db.Column(db.Integer)  # duração em segundos
    recording_url = db.Column(db.String(500))  # URL da gravação (se houver)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    closed_at = db.Column(db.DateTime)
    
    # Relacionamentos
    evaluations = db.relationship('Evaluation', backref='call', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_evaluations=False):
        """Converte a chamada para dicionário"""
        data = {
            'id': self.id,
            'protocol': self.protocol,
            'operator_id': self.operator_id,
            'operator_name': self.operator.full_name if self.operator else None,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'subject': self.subject,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'duration_seconds': self.duration_seconds,
            'recording_url': self.recording_url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        }
        
        if include_evaluations:
            data['evaluations'] = [eval.to_dict() for eval in self.evaluations]
        
        return data
    
    def __repr__(self):
        return f'<Call {self.protocol}>'
