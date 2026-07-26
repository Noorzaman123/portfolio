"""Flask extensions — instantiated here to avoid circular imports."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
try:
    from flask_mail import Mail
except ImportError:
    class Mail:
        def __init__(self, app=None):
            pass
        def init_app(self, app):
            pass

try:
    from flask_migrate import Migrate
except ImportError:
    class Migrate:
        def __init__(self, app=None, db=None):
            pass
        def init_app(self, app, db):
            pass

try:
    from flask_bcrypt import Bcrypt
except ImportError:
    from werkzeug.security import generate_password_hash, check_password_hash
    class Bcrypt:
        def __init__(self, app=None):
            pass
        def init_app(self, app):
            pass
        def generate_password_hash(self, password: str):
            return generate_password_hash(password).encode('utf-8')
        def check_password_hash(self, pw_hash: str, password: str) -> bool:
            return check_password_hash(pw_hash, password)

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()
