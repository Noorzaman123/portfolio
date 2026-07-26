"""Experience model."""
import json
from datetime import datetime
from ..extensions import db


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=True)
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True)
    _achievements = db.Column('achievements', db.Text, default='[]')
    company_logo = db.Column(db.String(256), nullable=True)
    company_url = db.Column(db.String(256), nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def achievements(self):
        try:
            return json.loads(self._achievements)
        except (TypeError, ValueError):
            return []

    @achievements.setter
    def achievements(self, value):
        self._achievements = json.dumps(value if isinstance(value, list) else [])

    def __repr__(self):
        return f'<Experience {self.title} @ {self.company}>'
