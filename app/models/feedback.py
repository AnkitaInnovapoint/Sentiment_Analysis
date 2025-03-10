from app import db
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100))
    sentiment = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'department': self.department,
            'sentiment': self.sentiment,
            'score': self.score,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat()
        } 