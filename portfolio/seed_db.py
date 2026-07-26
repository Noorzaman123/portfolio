"""
Seed the database with Noor Zaman's portfolio data.

Usage:
    python seed_db.py

This script is idempotent — running it multiple times will not duplicate data.
"""
import os
import sys

# Ensure the app package is importable
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.project import Project
from app.models.skill import Skill
from app.models.experience import Experience
from app.models.education import Education
from app.models.certificate import Certificate
from app.models.blog import BlogPost, Category
from app.models.settings import SiteSettings


def seed():
    app = create_app('development')

    with app.app_context():
        db.create_all()
        print("✅ Tables created.")

        # ─── Admin User ────────────────────────────────────────────────
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='noorzamanktk2@gmail.com',
                is_admin=True,
            )
            admin.set_password('Admin@Portfolio2024')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin / Admin@Portfolio2024")
        else:
            print("ℹ️  Admin user already exists.")

        # ─── Site Settings ──────────────────────────────────────────────
        settings_data = [
            ('site_tagline', 'Python Backend Developer | Full Stack Developer | Cybersecurity Enthusiast'),
            ('meta_description', 'Computer Science graduate passionate about backend development, scalable web applications, cybersecurity, and Python development.'),
            ('linkedin_url', 'https://www.linkedin.com/in/noor-zaman-99b806291'),
            ('github_url', 'https://github.com'),
            ('resume_downloads', '0'),
            ('footer_text', 'Built with ❤️ using Python Flask'),
        ]
        for key, value in settings_data:
            if not SiteSettings.query.filter_by(key=key).first():
                db.session.add(SiteSettings(key=key, value=value))
        db.session.commit()
        print("✅ Site settings seeded.")

        # ─── Skills ────────────────────────────────────────────────────
        skills_data = [
            # (name, category, level, icon, color, order, is_featured)
            # Programming Languages
            ('Python',       'programming', 92, 'fab fa-python',     '#3776AB', 1,  True),
            ('JavaScript',   'programming', 70, 'fab fa-js-square',  '#F7DF1E', 2,  False),
            ('SQL',          'programming', 80, 'fas fa-database',   '#336791', 3,  False),
            ('HTML5',        'programming', 85, 'fab fa-html5',      '#E34F26', 4,  False),
            ('CSS3',         'programming', 80, 'fab fa-css3-alt',   '#1572B6', 5,  False),
            # Backend
            ('Flask',        'backend',     90, 'fas fa-flask',      '#6366f1', 1,  True),
            ('Django',       'backend',     80, 'fas fa-leaf',       '#092E20', 2,  True),
            ('FastAPI',      'backend',     75, 'fas fa-bolt',       '#009688', 3,  False),
            ('REST API',     'backend',     88, 'fas fa-exchange-alt','#06b6d4', 4,  False),
            # Frontend
            ('React',        'frontend',    65, 'fab fa-react',      '#61DAFB', 1,  False),
            ('Bootstrap 5',  'frontend',    85, 'fab fa-bootstrap',  '#7952B3', 2,  False),
            # Database
            ('SQLite',       'database',    90, 'fas fa-database',   '#003B57', 1,  False),
            ('PostgreSQL',   'database',    78, 'fas fa-database',   '#336791', 2,  True),
            ('MySQL',        'database',    75, 'fas fa-database',   '#4479A1', 3,  False),
            ('SQLAlchemy',   'database',    85, 'fas fa-layer-group','#8b5cf6', 4,  False),
            # Tools
            ('Git',          'tools',       88, 'fab fa-git-alt',    '#F05032', 1,  False),
            ('GitHub',       'tools',       88, 'fab fa-github',     '#f0f6fc', 2,  False),
            ('VS Code',      'tools',       90, 'fas fa-code',       '#007ACC', 3,  False),
            ('Postman',      'tools',       80, 'fas fa-paper-plane','#FF6C37', 4,  False),
            ('Linux',        'tools',       72, 'fab fa-linux',      '#FCC624', 5,  False),
            # Cybersecurity
            ('Networking',         'cybersecurity', 72, 'fas fa-network-wired','#06b6d4', 1, False),
            ('Security Basics',    'cybersecurity', 70, 'fas fa-shield-alt',   '#ef4444',  2, False),
            ('Vulnerability Assessment', 'cybersecurity', 65, 'fas fa-bug', '#f59e0b', 3, False),
            # Machine Learning
            ('Pandas',       'ml', 75, 'fas fa-table',       '#150458', 1, False),
            ('NumPy',        'ml', 72, 'fas fa-calculator',  '#4DABCF', 2, False),
            ('Scikit-learn', 'ml', 65, 'fas fa-robot',       '#f97316', 3, False),
        ]
        for name, cat, level, icon, color, order, featured in skills_data:
            if not Skill.query.filter_by(name=name).first():
                db.session.add(Skill(
                    name=name, category=cat, level=level,
                    icon=icon, color=color, order=order, is_featured=featured,
                ))
        db.session.commit()
        print(f"✅ {len(skills_data)} skills seeded.")

        # ─── Experiences ───────────────────────────────────────────────
        experiences_data = [
            {
                'title': 'Python Developer Intern',
                'company': 'Arch Technologies',
                'location': 'Peshawar, Pakistan',
                'start_date': 'Jan 2023',
                'end_date': 'Jun 2023',
                'is_current': False,
                'description': 'Worked as a Python Developer Intern, contributing to backend development, API design, and automation projects using Flask and Python.',
                'achievements': [
                    'Developed and maintained Python backend services and RESTful APIs using Flask',
                    'Built automation scripts that reduced manual workflow time by 40%',
                    'Collaborated on Flask web applications with senior developers',
                    'Participated in code reviews and followed agile/Scrum practices',
                    'Integrated third-party APIs and handled data processing pipelines',
                ],
                'order': 1,
            },
            {
                'title': 'Cyber Security & Web Development Intern',
                'company': 'National Telecommunication Corporation (NTC)',
                'location': 'Peshawar, Pakistan',
                'start_date': 'Jul 2023',
                'end_date': 'Dec 2023',
                'is_current': False,
                'description': 'Interned at NTC focusing on cybersecurity assessments and web development for internal systems.',
                'achievements': [
                    'Assisted in vulnerability assessments and security audits of web applications',
                    'Developed and maintained web pages for the organization\'s internal systems',
                    'Studied and applied network security principles and protocols',
                    'Documented security findings and provided actionable recommendations',
                    'Gained hands-on experience with network monitoring and intrusion detection tools',
                ],
                'order': 2,
            },
        ]
        for exp_data in experiences_data:
            if not Experience.query.filter_by(title=exp_data['title'], company=exp_data['company']).first():
                exp = Experience(**{k: v for k, v in exp_data.items() if k != 'achievements'})
                exp.achievements = exp_data['achievements']
                db.session.add(exp)
        db.session.commit()
        print("✅ Experiences seeded.")

        # ─── Education ─────────────────────────────────────────────────
        if not Education.query.first():
            edu = Education(
                degree='Bachelor of Science',
                field='Computer Science',
                institution='University / Institute of Information Technology',
                location='Peshawar, Pakistan',
                start_year='2020',
                end_year='2024',
                is_current=False,
                description='Focused on software engineering, algorithms, databases, networking, and cybersecurity. Built multiple projects applying theoretical concepts to real-world solutions.',
                order=1,
            )
            db.session.add(edu)
            db.session.commit()
            print("✅ Education seeded.")

        # ─── Projects ──────────────────────────────────────────────────
        projects_data = [
            {
                'title': 'Explore PK – AI Tourism & Booking Platform',
                'slug': 'explore-pk-ai-tourism-booking-platform',
                'short_description': 'An intelligent tourism booking platform for Pakistan featuring AI recommendations, live weather, chatbot, and admin dashboard.',
                'long_description': '''<p>Explore PK is a comprehensive AI-powered tourism and booking platform designed to help travelers discover and book experiences across Pakistan. The platform integrates multiple intelligent systems to provide a seamless travel planning experience.</p>

<h3>Core Features</h3>
<p>The platform includes a robust recommendation system that analyzes user preferences and travel history to suggest personalized destinations and activities. An integrated chatbot handles user queries 24/7, while live weather API integration ensures travelers have real-time weather information for their destinations.</p>

<p>The admin dashboard provides complete control over bookings, user management, and content moderation. The invoice generation system automatically creates professional PDF invoices for completed bookings.</p>

<h3>Technical Architecture</h3>
<p>Built with Python and Streamlit for the frontend, with SQLite handling data persistence. BeautifulSoup handles web scraping for live tourism data, while a custom JSON-based recommendation engine provides AI-powered suggestions.</p>''',
                'tech_stack': ['Python', 'Streamlit', 'SQLite', 'BeautifulSoup', 'JSON', 'Weather API'],
                'features': [
                    'Live weather integration via external API',
                    'AI-powered destination recommendation system',
                    'Integrated chatbot for 24/7 user support',
                    'Hotel and tour booking with confirmation',
                    'Admin dashboard for full platform management',
                    'PDF invoice generation for bookings',
                    'Image gallery with destination photos',
                    'User authentication and profile management',
                    'Web scraping for live tourism data',
                ],
                'github_url': '#github-placeholder',
                'live_url': '',
                'category': 'AI & Python',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'IoT Resource Analytics Dashboard',
                'slug': 'iot-resource-analytics-dashboard',
                'short_description': 'A scalable IoT analytics platform with Django REST Framework backend, PostgreSQL database, and React-based real-time dashboard.',
                'long_description': '''<p>The IoT Resource Analytics Dashboard is a production-ready platform for monitoring and analyzing IoT device data in real-time. Designed for scalability, it handles thousands of data points per minute with minimal latency.</p>

<h3>Backend Architecture</h3>
<p>The backend is built with Django REST Framework, providing a clean, well-documented API layer. PostgreSQL serves as the primary database, optimized with proper indexing for time-series IoT data. JWT authentication secures all API endpoints.</p>

<h3>Dashboard</h3>
<p>The React-based frontend dashboard provides real-time visualization of resource utilization metrics. Interactive charts display CPU usage, memory consumption, network throughput, and custom IoT sensor data with configurable time ranges.</p>

<h3>Key Technical Decisions</h3>
<p>Django channels handle WebSocket connections for real-time updates without polling. The REST API follows HATEOAS principles and is fully documented with OpenAPI/Swagger. Celery handles background data aggregation tasks.</p>''',
                'tech_stack': ['Python', 'Django', 'Django REST Framework', 'React', 'PostgreSQL', 'REST API', 'JWT'],
                'features': [
                    'Real-time IoT device monitoring',
                    'Scalable Django REST Framework backend',
                    'PostgreSQL with optimized time-series queries',
                    'React dashboard with interactive charts',
                    'JWT-based API authentication',
                    'WebSocket support for live updates',
                    'Celery background task processing',
                    'OpenAPI/Swagger API documentation',
                ],
                'github_url': '#github-placeholder',
                'live_url': '',
                'category': 'Backend & IoT',
                'is_featured': True,
                'order': 2,
            },
        ]
        for p_data in projects_data:
            if not Project.query.filter_by(slug=p_data['slug']).first():
                project = Project(
                    title=p_data['title'],
                    slug=p_data['slug'],
                    short_description=p_data['short_description'],
                    long_description=p_data['long_description'],
                    github_url=p_data.get('github_url', ''),
                    live_url=p_data.get('live_url', ''),
                    category=p_data['category'],
                    is_featured=p_data['is_featured'],
                    order=p_data['order'],
                )
                project.tech_stack = p_data['tech_stack']
                project.features = p_data['features']
                db.session.add(project)
        db.session.commit()
        print("✅ Projects seeded.")

        # ─── Blog Category & Sample Post ───────────────────────────────
        if not Category.query.first():
            categories = [
                Category(name='Python',       slug='python',       description='Python programming tutorials and tips'),
                Category(name='Flask',        slug='flask',        description='Flask web development guides'),
                Category(name='Backend',      slug='backend',      description='Backend development best practices'),
                Category(name='Cybersecurity',slug='cybersecurity',description='Security tips and practices'),
                Category(name='Career',       slug='career',       description='Career advice for developers'),
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("✅ Blog categories seeded.")

        if not BlogPost.query.first():
            py_cat = Category.query.filter_by(slug='python').first()
            sample_post = BlogPost(
                title='Getting Started with Flask: Build Your First REST API',
                slug='getting-started-flask-rest-api',
                summary='Learn how to build a production-ready REST API using Flask, SQLAlchemy, and Flask-Login in under 30 minutes.',
                content='''# Getting Started with Flask: Build Your First REST API

Flask is a lightweight, flexible Python web framework that's perfect for building REST APIs. In this article, we'll build a complete REST API from scratch.

## Why Flask?

Flask is minimal by design, giving you the freedom to structure your application exactly as you need. Unlike Django, Flask doesn't impose conventions, making it ideal for microservices and APIs.

## Prerequisites

- Python 3.8+
- pip package manager
- Basic Python knowledge

## Installation

```bash
pip install flask flask-sqlalchemy flask-jwt-extended
```

## Creating Your First Flask App

```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db = SQLAlchemy(app)

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'message': 'API is running!'})

if __name__ == '__main__':
    app.run(debug=True)
```

## Defining Your Model

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
```

## Creating CRUD Endpoints

```python
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

## Conclusion

Flask makes building APIs elegant and efficient. The framework's simplicity allows you to focus on business logic rather than framework conventions.

Stay tuned for more Flask tutorials covering authentication, pagination, and deployment!
''',
                category_id=py_cat.id if py_cat else None,
                is_published=True,
                is_featured=True,
                read_time=5,
                meta_description='Learn how to build a production-ready REST API using Flask, SQLAlchemy, and JWT authentication.',
            )
            db.session.add(sample_post)
            db.session.commit()
            print("✅ Sample blog post seeded.")

        print("\n🎉 Database seeded successfully!")
        print("─" * 50)
        print("Admin URL:      http://localhost:5000/admin")
        print("Admin User:     admin")
        print("Admin Password: Admin@Portfolio2024")
        print("─" * 50)
        print("⚠️  IMPORTANT: Change the admin password after first login!")


if __name__ == '__main__':
    seed()
