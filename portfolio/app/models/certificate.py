"""Certificate model."""
from datetime import datetime
from ..extensions import db


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    issue_date = db.Column(db.String(20), nullable=True)
    expiry_date = db.Column(db.String(20), nullable=True)
    credential_id = db.Column(db.String(200), nullable=True)
    credential_url = db.Column(db.String(256), nullable=True)
    image_url = db.Column(db.String(256), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Certificate {self.name}>'
