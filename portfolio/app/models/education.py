"""Education model."""
from ..extensions import db


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    field = db.Column(db.String(200), nullable=True)
    institution = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    start_year = db.Column(db.String(10), nullable=False)
    end_year = db.Column(db.String(10), nullable=True)
    is_current = db.Column(db.Boolean, default=False)
    gpa = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(256), nullable=True)
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Education {self.degree} @ {self.institution}>'
