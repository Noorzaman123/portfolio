"""Project model."""
import json
from datetime import datetime
from ..extensions import db


class ProjectTag(db.Model):
    __tablename__ = 'project_tags'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'))
    name = db.Column(db.String(50), nullable=False)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    short_description = db.Column(db.String(300), nullable=False)
    long_description = db.Column(db.Text, nullable=True)
    _tech_stack = db.Column('tech_stack', db.Text, default='[]')  # JSON list
    _features = db.Column('features', db.Text, default='[]')       # JSON list
    github_url = db.Column(db.String(256), nullable=True)
    live_url = db.Column(db.String(256), nullable=True)
    image_url = db.Column(db.String(256), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('ProjectTag', backref='project', cascade='all, delete-orphan', lazy=True)

    @property
    def tech_stack(self):
        try:
            return json.loads(self._tech_stack)
        except (TypeError, ValueError):
            return []

    @tech_stack.setter
    def tech_stack(self, value):
        self._tech_stack = json.dumps(value if isinstance(value, list) else [])

    @property
    def features(self):
        try:
            return json.loads(self._features)
        except (TypeError, ValueError):
            return []

    @features.setter
    def features(self, value):
        self._features = json.dumps(value if isinstance(value, list) else [])

    def increment_views(self):
        self.views += 1
        db.session.commit()

    def __repr__(self):
        return f'<Project {self.title}>'
