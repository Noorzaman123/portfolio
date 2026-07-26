"""Gallery model."""
from datetime import datetime
from ..extensions import db


class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Gallery {self.title}>'
