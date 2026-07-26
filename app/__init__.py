py"""Flask application factory."""
import os
from flask import Flask, render_template
from .config import config
from .extensions import db, login_manager, csrf, migrate, mail, bcrypt


def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object(config[config_name])

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)

    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from .blueprints.main import main_bp
    from .blueprints.blog import blog_bp
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Register error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/404.html', message="Access Forbidden"), 403

    @app.template_filter('external_url')
    def external_url_filter(url):
        if not url:
            return '#'
        url = str(url).strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            return f'https://{url}'
        return url

    # Inject site-wide template variables
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from .models.settings import SiteSettings
        try:
            settings = {s.key: s.value for s in SiteSettings.query.all()}
        except Exception:
            settings = {}
        return dict(site_settings=settings, site_name='Noor Zaman', now=datetime.utcnow())

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app
