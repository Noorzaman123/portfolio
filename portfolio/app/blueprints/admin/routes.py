"""Admin routes — full CRUD for all content types."""
import os
import json
from datetime import datetime, timedelta
try:
    from slugify import slugify
except ImportError:
    import re
    def slugify(text):
        text = str(text).lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        return re.sub(r'[\s_-]+', '-', text)
from flask import (
    render_template, redirect, url_for, flash,
    request, current_app, jsonify
)
from flask_login import login_required, current_user
from . import admin_bp
from ...extensions import db
from ...models.user import User
from ...models.project import Project, ProjectTag
from ...models.skill import Skill
from ...models.experience import Experience
from ...models.education import Education
from ...models.certificate import Certificate
from ...models.message import Message
from ...models.blog import BlogPost, Category, Comment
from ...models.gallery import Gallery
from ...models.settings import SiteSettings, VisitorStat


def allowed_file(filename):
    allowed = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_upload(file_obj, subfolder=''):
    """Save an uploaded file and return its URL path."""
    import uuid
    from werkzeug.utils import secure_filename
    filename = secure_filename(file_obj.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(folder, exist_ok=True)
    file_obj.save(os.path.join(folder, unique_name))
    return f'/static/uploads/{subfolder}/{unique_name}' if subfolder else f'/static/uploads/{unique_name}'


# ─── Dashboard ───────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    stats = {
        'projects': Project.query.count(),
        'skills': Skill.query.count(),
        'messages': Message.query.count(),
        'unread_messages': Message.query.filter_by(is_read=False).count(),
        'blog_posts': BlogPost.query.count(),
        'published_posts': BlogPost.query.filter_by(is_published=True).count(),
        'gallery': Gallery.query.count(),
        'visitors_today': VisitorStat.query.filter(
            VisitorStat.visited_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
        ).count(),
        'visitors_week': VisitorStat.query.filter(
            VisitorStat.visited_at >= datetime.utcnow() - timedelta(days=7)
        ).count(),
        'visitors_total': VisitorStat.query.count(),
        'resume_downloads': SiteSettings.get('resume_downloads', '0'),
    }
    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()

    # Visitor data for chart (last 7 days)
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = VisitorStat.query.filter(
            VisitorStat.visited_at >= start,
            VisitorStat.visited_at <= end
        ).count()
        chart_labels.append(day.strftime('%b %d'))
        chart_data.append(count)

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_messages=recent_messages,
        recent_posts=recent_posts,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
    )


# ─── Projects ────────────────────────────────────────────────────────────────

@admin_bp.route('/projects')
@login_required
def projects():
    all_projects = Project.query.order_by(Project.order).all()
    return render_template('admin/projects.html', projects=all_projects)


@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def project_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = slugify(title)
        # Ensure unique slug
        existing = Project.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{datetime.utcnow().strftime('%f')[:4]}"

        tech_raw = request.form.get('tech_stack', '')
        features_raw = request.form.get('features', '')
        tech_list = [t.strip() for t in tech_raw.split(',') if t.strip()]
        features_list = [f.strip() for f in features_raw.split('\n') if f.strip()]

        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            f = request.files['image']
            if allowed_file(f.filename):
                image_url = save_upload(f, 'projects')

        project = Project(
            title=title, slug=slug,
            short_description=request.form.get('short_description', ''),
            long_description=request.form.get('long_description', ''),
            github_url=request.form.get('github_url', ''),
            live_url=request.form.get('live_url', ''),
            image_url=image_url or request.form.get('image_url', ''),
            category=request.form.get('category', ''),
            is_featured=bool(request.form.get('is_featured')),
            order=int(request.form.get('order', 0)),
        )
        project.tech_stack = tech_list
        project.features = features_list
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', project=None)


@admin_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def project_edit(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title', '').strip()
        project.slug = slugify(project.title)
        project.short_description = request.form.get('short_description', '')
        project.long_description = request.form.get('long_description', '')
        project.github_url = request.form.get('github_url', '')
        project.live_url = request.form.get('live_url', '')
        project.category = request.form.get('category', '')
        project.is_featured = bool(request.form.get('is_featured'))
        project.order = int(request.form.get('order', 0))

        tech_raw = request.form.get('tech_stack', '')
        features_raw = request.form.get('features', '')
        project.tech_stack = [t.strip() for t in tech_raw.split(',') if t.strip()]
        project.features = [f.strip() for f in features_raw.split('\n') if f.strip()]

        if 'image' in request.files and request.files['image'].filename:
            f = request.files['image']
            if allowed_file(f.filename):
                project.image_url = save_upload(f, 'projects')
        elif request.form.get('image_url'):
            project.image_url = request.form.get('image_url')

        project.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', project=project)


@admin_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('admin.projects'))


# ─── Skills ──────────────────────────────────────────────────────────────────

@admin_bp.route('/skills')
@login_required
def skills():
    all_skills = Skill.query.order_by(Skill.category, Skill.order).all()
    return render_template('admin/skills.html', skills=all_skills, categories=Skill.CATEGORIES)


@admin_bp.route('/skills/new', methods=['POST'])
@login_required
def skill_new():
    skill = Skill(
        name=request.form.get('name', ''),
        category=request.form.get('category', ''),
        level=int(request.form.get('level', 80)),
        icon=request.form.get('icon', ''),
        color=request.form.get('color', '#6366f1'),
        order=int(request.form.get('order', 0)),
        is_featured=bool(request.form.get('is_featured')),
    )
    db.session.add(skill)
    db.session.commit()
    flash('Skill added!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/<int:skill_id>/edit', methods=['POST'])
@login_required
def skill_edit(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    skill.name = request.form.get('name', skill.name)
    skill.category = request.form.get('category', skill.category)
    skill.level = int(request.form.get('level', skill.level))
    skill.icon = request.form.get('icon', skill.icon)
    skill.color = request.form.get('color', skill.color)
    skill.order = int(request.form.get('order', skill.order))
    skill.is_featured = bool(request.form.get('is_featured'))
    db.session.commit()
    flash('Skill updated!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def skill_delete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'info')
    return redirect(url_for('admin.skills'))


# ─── Blog ────────────────────────────────────────────────────────────────────

@admin_bp.route('/blog')
@login_required
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('admin/blog.html', posts=posts, categories=categories)


@admin_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blog_new():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = slugify(title)
        existing = BlogPost.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{datetime.utcnow().strftime('%f')[:4]}"

        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            f = request.files['image']
            if allowed_file(f.filename):
                image_url = save_upload(f, 'blog')

        content = request.form.get('content', '')
        word_count = len(content.split())
        read_time = max(1, word_count // 200)

        post = BlogPost(
            title=title, slug=slug,
            summary=request.form.get('summary', ''),
            content=content,
            image_url=image_url or request.form.get('image_url', ''),
            category_id=request.form.get('category_id') or None,
            is_published=bool(request.form.get('is_published')),
            is_featured=bool(request.form.get('is_featured')),
            meta_description=request.form.get('meta_description', ''),
            read_time=read_time,
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog post created!', 'success')
        return redirect(url_for('admin.blog'))

    return render_template('admin/blog_form.html', post=None, categories=categories)


@admin_bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def blog_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    categories = Category.query.all()

    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.summary = request.form.get('summary', '')
        post.content = request.form.get('content', '')
        post.category_id = request.form.get('category_id') or None
        post.is_published = bool(request.form.get('is_published'))
        post.is_featured = bool(request.form.get('is_featured'))
        post.meta_description = request.form.get('meta_description', '')
        word_count = len(post.content.split())
        post.read_time = max(1, word_count // 200)
        post.updated_at = datetime.utcnow()

        if 'image' in request.files and request.files['image'].filename:
            f = request.files['image']
            if allowed_file(f.filename):
                post.image_url = save_upload(f, 'blog')
        elif request.form.get('image_url'):
            post.image_url = request.form.get('image_url')

        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('admin.blog'))

    return render_template('admin/blog_form.html', post=post, categories=categories)


@admin_bp.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def blog_delete(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('admin.blog'))


@admin_bp.route('/blog/categories/new', methods=['POST'])
@login_required
def category_new():
    name = request.form.get('name', '').strip()
    if name:
        cat = Category(name=name, slug=slugify(name), description=request.form.get('description', ''))
        db.session.add(cat)
        db.session.commit()
        flash('Category created!', 'success')
    return redirect(url_for('admin.blog'))


@admin_bp.route('/blog/comments')
@login_required
def blog_comments():
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)


@admin_bp.route('/blog/comments/<int:comment_id>/approve', methods=['POST'])
@login_required
def comment_approve(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    flash('Comment approved.', 'success')
    return redirect(url_for('admin.blog_comments'))


@admin_bp.route('/blog/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def comment_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(url_for('admin.blog_comments'))


# ─── Messages ────────────────────────────────────────────────────────────────

@admin_bp.route('/messages')
@login_required
def messages():
    msgs = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=msgs)


@admin_bp.route('/messages/<int:msg_id>')
@login_required
def message_view(msg_id):
    msg = Message.query.get_or_404(msg_id)
    if not msg.is_read:
        msg.mark_read()
    return render_template('admin/message_view.html', message=msg)


@admin_bp.route('/messages/<int:msg_id>/delete', methods=['POST'])
@login_required
def message_delete(msg_id):
    msg = Message.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('admin.messages'))


# ─── Gallery ─────────────────────────────────────────────────────────────────

@admin_bp.route('/gallery')
@login_required
def gallery():
    items = Gallery.query.order_by(Gallery.order).all()
    return render_template('admin/gallery.html', items=items)


@admin_bp.route('/gallery/new', methods=['POST'])
@login_required
def gallery_new():
    image_url = None
    if 'image' in request.files and request.files['image'].filename:
        f = request.files['image']
        if allowed_file(f.filename):
            image_url = save_upload(f, 'gallery')

    item = Gallery(
        title=request.form.get('title', ''),
        description=request.form.get('description', ''),
        image_url=image_url or request.form.get('image_url', ''),
        category=request.form.get('category', ''),
        order=int(request.form.get('order', 0)),
    )
    db.session.add(item)
    db.session.commit()
    flash('Gallery item added!', 'success')
    return redirect(url_for('admin.gallery'))


@admin_bp.route('/gallery/<int:item_id>/delete', methods=['POST'])
@login_required
def gallery_delete(item_id):
    item = Gallery.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.', 'info')
    return redirect(url_for('admin.gallery'))


# ─── Settings ────────────────────────────────────────────────────────────────

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('_'):
                continue
            SiteSettings.set(key, request.form.get(key, ''))
        flash('Settings saved!', 'success')
        return redirect(url_for('admin.settings'))

    all_settings = {s.key: s.value for s in SiteSettings.query.all()}
    return render_template('admin/settings.html', settings=all_settings)


# ─── Resume Upload ────────────────────────────────────────────────────────────

@admin_bp.route('/resume/upload', methods=['POST'])
@login_required
def resume_upload():
    if 'resume' in request.files and request.files['resume'].filename:
        f = request.files['resume']
        if f.filename.endswith('.pdf'):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            f.save(os.path.join(upload_folder, 'Noor_Zaman_Resume.pdf'))
            flash('Resume uploaded successfully!', 'success')
        else:
            flash('Only PDF files are allowed for resume.', 'danger')
    return redirect(url_for('admin.settings'))


@admin_bp.route('/profile-photo/upload', methods=['POST'])
@login_required
def profile_photo_upload():
    if 'profile_photo' in request.files and request.files['profile_photo'].filename:
        f = request.files['profile_photo']
        ext = f.filename.rsplit('.', 1)[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'webp']:
            assets_folder = os.path.join(current_app.root_path, 'static', 'assets')
            os.makedirs(assets_folder, exist_ok=True)
            f.save(os.path.join(assets_folder, 'profile.jpg'))
            flash('Profile picture updated successfully!', 'success')
        else:
            flash('Only JPG, PNG, or WEBP images are allowed.', 'danger')
    return redirect(url_for('admin.settings'))

