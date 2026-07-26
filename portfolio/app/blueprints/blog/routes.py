try:
    import markdown as md
    def render_md(content):
        return md.markdown(content, extensions=['fenced_code', 'tables', 'toc', 'nl2br'])
except ImportError:
    import html
    def render_md(content):
        safe_content = html.escape(content or '')
        return ''.join(f'<p>{p}</p>' for p in safe_content.split('\n\n'))

from flask import render_template, request, redirect, url_for, flash, current_app
from . import blog_bp
from ...extensions import db
from ...models.blog import BlogPost, Category, Comment


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_slug = request.args.get('category', '')

    query = BlogPost.query.filter_by(is_published=True)

    if search:
        query = query.filter(
            BlogPost.title.ilike(f'%{search}%') |
            BlogPost.summary.ilike(f'%{search}%')
        )
    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    posts = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    categories = Category.query.all()
    featured_posts = BlogPost.query.filter_by(is_published=True, is_featured=True).limit(3).all()

    return render_template(
        'blog/index.html',
        posts=posts,
        categories=categories,
        featured_posts=featured_posts,
        search=search,
        selected_category=category_slug,
    )


@blog_bp.route('/<slug>', methods=['GET', 'POST'])
def post(slug):
    blog_post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    blog_post.increment_views()

    # Render Markdown content
    rendered_content = render_md(blog_post.content)

    # Handle comment submission
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        content = request.form.get('content', '').strip()

        if not name or not email or not content:
            flash('Please fill all comment fields.', 'danger')
        else:
            comment = Comment(
                post_id=blog_post.id,
                name=name, email=email, content=content,
                ip_address=request.remote_addr,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been submitted for review. Thank you!', 'success')
            return redirect(url_for('blog.post', slug=slug))

    approved_comments = blog_post.approved_comments()
    related = BlogPost.query.filter(
        BlogPost.category_id == blog_post.category_id,
        BlogPost.id != blog_post.id,
        BlogPost.is_published == True
    ).limit(3).all()

    return render_template(
        'blog/post.html',
        post=blog_post,
        content=rendered_content,
        comments=approved_comments,
        related=related,
    )


@blog_bp.route('/category/<slug>')
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(
        category_id=cat.id, is_published=True
    ).order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    categories = Category.query.all()
    return render_template(
        'blog/index.html',
        posts=posts,
        categories=categories,
        featured_posts=[],
        search='',
        selected_category=slug,
        current_category=cat,
    )
