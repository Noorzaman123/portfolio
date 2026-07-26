# Noor Zaman – Personal Portfolio Website

A production-ready personal portfolio website built with **Python Flask**, featuring a premium dark-mode UI, full admin dashboard, blog system, and deployment-ready configuration.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/portfolio.git
cd portfolio
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Seed the database
```bash
python seed_db.py
```

### 6. Run the development server
```bash
python run.py
```

Visit: **http://localhost:5000**  
Admin: **http://localhost:5000/admin** → `admin` / `Admin@Portfolio2024`

---

## 📁 Project Structure

```
portfolio/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration classes
│   ├── extensions.py        # Flask extensions
│   ├── blueprints/
│   │   ├── main/            # Public pages
│   │   ├── blog/            # Blog system
│   │   ├── auth/            # Authentication
│   │   └── admin/           # Admin dashboard
│   ├── models/              # SQLAlchemy models
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript
│   │   └── assets/          # Images, favicon
│   └── templates/           # Jinja2 templates
├── instance/                # SQLite database (auto-created)
├── seed_db.py               # Database seeder
├── run.py                   # Development server entry point
├── requirements.txt
├── Procfile                 # Render / Heroku deployment
├── runtime.txt
├── gunicorn.conf.py
└── .env.example
```

---

## 🎨 Features

- **Premium Dark/Light Mode** with localStorage persistence
- **Glassmorphism** design with animated gradient backgrounds
- **Particle Background** with canvas-based animation
- **Typing Animation** cycling through roles
- **Animated Stats Counters**
- **Scroll Reveal** animations (AOS)
- **Custom Cursor** effect (desktop)
- **Full Blog System** with Markdown, categories, comments, search, pagination
- **Admin Dashboard** with analytics, visitor chart, and full CRUD
- **Contact Form** with database storage and optional email notification
- **SEO** meta tags, Open Graph, Twitter Cards, XML sitemap, robots.txt
- **CSRF Protection** on all forms
- **Responsive** mobile-first design

---

## 🔐 Admin Panel

| Feature | URL |
|---------|-----|
| Login | `/auth/login` |
| Dashboard | `/admin/` |
| Projects | `/admin/projects` |
| Blog | `/admin/blog` |
| Skills | `/admin/skills` |
| Messages | `/admin/messages` |
| Gallery | `/admin/gallery` |
| Settings | `/admin/settings` |

**Default credentials:** `admin` / `Admin@Portfolio2024`  
⚠️ Change the password after first login!

---

## 🚀 Deployment (Render)

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Set **Build Command:** `pip install -r requirements.txt && python seed_db.py`
4. Set **Start Command:** `gunicorn run:app --config gunicorn.conf.py`
5. Add environment variables from `.env.example`
6. For PostgreSQL: add a Render Postgres database and set `DATABASE_URL`

---

## 📧 Contact

**Noor Zaman**  
📧 noorzamanktk2@gmail.com  
📞 +92 333 4791760  
📍 Peshawar, Pakistan  
🔗 [LinkedIn](https://www.linkedin.com/in/noor-zaman-99b806291)

---

## 📄 License

MIT License — feel free to use this as a template for your own portfolio.
