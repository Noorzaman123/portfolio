"""Main public-facing routes."""
import os
from datetime import datetime
from flask import (
    render_template, redirect, url_for, flash,
    request, send_from_directory, current_app, abort, make_response
)
from . import main_bp
from ...extensions import db, mail
from ...models.project import Project
from ...models.skill import Skill
from ...models.experience import Experience
from ...models.education import Education
from ...models.certificate import Certificate
from ...models.message import Message
from ...models.blog import BlogPost, Category
from ...models.gallery import Gallery
from ...models.settings import VisitorStat


def _track_visit(page):
    """Record a page visit."""
    try:
        stat = VisitorStat(
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:300] if request.user_agent else None,
            referrer=request.referrer[:300] if request.referrer else None,
        )
        db.session.add(stat)
        db.session.commit()
    except Exception:
        db.session.rollback()


# ─── Home ────────────────────────────────────────────────────────────────────

@main_bp.route('/')
def index():
    _track_visit('home')
    featured_projects = Project.query.filter_by(is_featured=True).order_by(Project.order).limit(3).all()
    latest_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    skills_featured = Skill.query.filter_by(is_featured=True).order_by(Skill.order).all()
    total_projects = Project.query.count()
    total_skills = Skill.query.count()
    return render_template(
        'main/index.html',
        featured_projects=featured_projects,
        latest_posts=latest_posts,
        skills_featured=skills_featured,
        total_projects=total_projects,
        total_skills=total_skills,
    )


# ─── About ───────────────────────────────────────────────────────────────────

@main_bp.route('/about')
def about():
    _track_visit('about')
    experiences = Experience.query.order_by(Experience.order).all()
    education = Education.query.order_by(Education.order).all()
    return render_template('main/about.html', experiences=experiences, education=education)


# ─── Skills ──────────────────────────────────────────────────────────────────

@main_bp.route('/skills')
def skills():
    _track_visit('skills')
    all_skills = Skill.query.order_by(Skill.category, Skill.order).all()
    categories = {}
    for skill in all_skills:
        categories.setdefault(skill.category, []).append(skill)
    return render_template('main/skills.html', skills_by_category=categories)


# ─── Projects ────────────────────────────────────────────────────────────────

@main_bp.route('/projects')
def projects():
    _track_visit('projects')
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = Project.query
    if category:
        query = query.filter(Project.category.ilike(f'%{category}%'))
    if search:
        query = query.filter(
            Project.title.ilike(f'%{search}%') |
            Project.short_description.ilike(f'%{search}%')
        )
    projects_pag = query.order_by(Project.order).paginate(
        page=page, per_page=current_app.config['PROJECTS_PER_PAGE'], error_out=False
    )
    categories = db.session.query(Project.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    return render_template(
        'main/projects.html',
        projects=projects_pag,
        categories=categories,
        selected_category=category,
        search=search,
    )


@main_bp.route('/projects/<slug>')
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    project.increment_views()
    related = Project.query.filter(
        Project.category == project.category, Project.id != project.id
    ).limit(3).all()
    return render_template('main/project_detail.html', project=project, related=related)


# ─── Services ────────────────────────────────────────────────────────────────

@main_bp.route('/services')
def services():
    _track_visit('services')
    return render_template('main/services.html')


# ─── Experience ──────────────────────────────────────────────────────────────

@main_bp.route('/experience')
def experience():
    _track_visit('experience')
    experiences = Experience.query.order_by(Experience.order).all()
    return render_template('main/experience.html', experiences=experiences)


# ─── Education ───────────────────────────────────────────────────────────────

@main_bp.route('/education')
def education():
    _track_visit('education')
    education_list = Education.query.order_by(Education.order).all()
    return render_template('main/education.html', education_list=education_list)


# ─── Certificates ────────────────────────────────────────────────────────────

@main_bp.route('/certificates')
def certificates():
    _track_visit('certificates')
    certs = Certificate.query.order_by(Certificate.order).all()
    categories = list(set(c.category for c in certs if c.category))
    return render_template('main/certificates.html', certificates=certs, categories=categories)


# ─── Resume ──────────────────────────────────────────────────────────────────

@main_bp.route('/resume')
def resume():
    _track_visit('resume')
    return render_template('main/resume.html')


@main_bp.route('/resume/download')
def download_resume():
    """Download the resume PDF. Increment download counter."""
    from ...models.settings import SiteSettings
    try:
        count = int(SiteSettings.get('resume_downloads', '0'))
        SiteSettings.set('resume_downloads', str(count + 1))
    except Exception:
        pass

    upload_folder = current_app.config['UPLOAD_FOLDER']
    resume_path = os.path.join(upload_folder, 'Noor_Zaman_Resume.pdf')
    if os.path.exists(resume_path):
        return send_from_directory(upload_folder, 'Noor_Zaman_Resume.pdf', as_attachment=True)

    # Fallback if PDF not yet uploaded
    flash('Resume PDF not yet uploaded. Please check back soon!', 'info')
    return redirect(url_for('main.resume'))


# ─── Contact ─────────────────────────────────────────────────────────────────

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    _track_visit('contact')
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message_text = request.form.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not email or '@' not in email:
            errors.append('A valid email is required.')
        if not subject:
            errors.append('Subject is required.')
        if not message_text or len(message_text) < 10:
            errors.append('Message must be at least 10 characters.')

        if errors:
            for e in errors:
                flash(e, 'danger')
        else:
            msg = Message(
                name=name, email=email, phone=phone,
                subject=subject, message=message_text,
                ip_address=request.remote_addr,
            )
            db.session.add(msg)
            db.session.commit()

            # Optional email notification
            try:
                notify = current_app.config.get('CONTACT_NOTIFY_EMAIL')
                if notify and current_app.config.get('MAIL_USERNAME'):
                    from flask_mail import Message as MailMsg
                    mail_msg = MailMsg(
                        subject=f'[Portfolio] New message: {subject}',
                        recipients=[notify],
                        body=f'From: {name} <{email}>\nPhone: {phone}\n\n{message_text}',
                    )
                    mail.send(mail_msg)
            except Exception:
                pass  # Don't break on mail failure

            flash('Thank you! Your message has been sent. I will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))

    return render_template('main/contact.html')


# ─── Privacy ─────────────────────────────────────────────────────────────────

@main_bp.route('/privacy')
def privacy():
    return render_template('main/privacy.html')


# ─── SEO ─────────────────────────────────────────────────────────────────────

@main_bp.route('/sitemap.xml')
def sitemap():
    pages = []
    base = current_app.config.get('SITE_URL', request.url_root.rstrip('/'))

    static_routes = [
        ('main.index', {}, '1.0', 'daily'),
        ('main.about', {}, '0.9', 'weekly'),
        ('main.skills', {}, '0.8', 'weekly'),
        ('main.projects', {}, '0.9', 'weekly'),
        ('main.services', {}, '0.8', 'monthly'),
        ('main.experience', {}, '0.8', 'monthly'),
        ('main.education', {}, '0.7', 'monthly'),
        ('main.certificates', {}, '0.7', 'monthly'),
        ('main.resume', {}, '0.8', 'monthly'),
        ('main.contact', {}, '0.6', 'monthly'),
        ('blog.index', {}, '0.9', 'daily'),
    ]
    for route, kwargs, priority, freq in static_routes:
        pages.append((url_for(route, _external=True, **kwargs), priority, freq))

    for post in BlogPost.query.filter_by(is_published=True).all():
        pages.append((url_for('blog.post', slug=post.slug, _external=True), '0.8', 'weekly'))

    for project in Project.query.all():
        pages.append((url_for('main.project_detail', slug=project.slug, _external=True), '0.8', 'monthly'))

    xml = render_template('sitemap.xml', pages=pages)
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@main_bp.route('/robots.txt')
def robots():
    base = current_app.config.get('SITE_URL', request.url_root.rstrip('/'))
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /auth/

Sitemap: {base}/sitemap.xml
"""
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    return response
