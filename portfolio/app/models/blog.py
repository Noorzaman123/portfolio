"""Blog models: BlogPost, Category, Comment."""
from datetime import datetime
from ..extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=True)
    posts = db.relationship('BlogPost', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(400), nullable=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(256), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    read_time = db.Column(db.Integer, default=5)  # minutes
    meta_description = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy='dynamic')

    def increment_views(self):
        self.views += 1
        db.session.commit()

    def approved_comments(self):
        return self.comments.filter_by(is_approved=True).all()

    def __repr__(self):
        return f'<BlogPost {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment by {self.name}>'
