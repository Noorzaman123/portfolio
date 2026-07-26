"""Message model for contact form submissions."""
from datetime import datetime
from ..extensions import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def mark_read(self):
        self.is_read = True
        db.session.commit()

    def __repr__(self):
        return f'<Message from {self.name} — {self.subject}>'
