"""Site settings and visitor statistics models."""
from datetime import datetime
from ..extensions import db


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(300), nullable=True)

    @classmethod
    def get(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    def __repr__(self):
        return f'<Setting {self.key}={self.value}>'


class VisitorStat(db.Model):
    __tablename__ = 'visitor_stats'

    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(300), nullable=True)
    referrer = db.Column(db.String(300), nullable=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Visit {self.page} at {self.visited_at}>'
