"""Skill model."""
from ..extensions import db


class Skill(db.Model):
    __tablename__ = 'skills'

    CATEGORIES = [
        ('programming', 'Programming Languages'),
        ('backend', 'Backend Frameworks'),
        ('frontend', 'Frontend'),
        ('database', 'Databases'),
        ('tools', 'Tools & DevOps'),
        ('cybersecurity', 'Cybersecurity'),
        ('ml', 'Machine Learning'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=80)        # 0-100 percentage
    icon = db.Column(db.String(100), nullable=True)  # CSS class or image url
    color = db.Column(db.String(20), default='#6366f1')
    order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Skill {self.name} – {self.level}%>'
