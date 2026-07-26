"""Application configuration."""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    # Core
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production-please!')
    WTF_CSRF_ENABLED = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "..", "instance", "portfolio.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@noorzaman.dev')
    CONTACT_NOTIFY_EMAIL = os.environ.get('CONTACT_NOTIFY_EMAIL', 'noorzamanktk2@gmail.com')

    # Site
    SITE_NAME = 'Noor Zaman – Python Developer'
    SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')
    POSTS_PER_PAGE = 6
    PROJECTS_PER_PAGE = 9


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Fix Render/Heroku postgres:// → postgresql://
        db_url = os.environ.get('DATABASE_URL', '')
        if db_url.startswith('postgres://'):
            cls.SQLALCHEMY_DATABASE_URI = db_url.replace('postgres://', 'postgresql://', 1)
        else:
            cls.SQLALCHEMY_DATABASE_URI = db_url or Config.SQLALCHEMY_DATABASE_URI


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
