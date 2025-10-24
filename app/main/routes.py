"""
Main routes for the application.
"""
from flask import render_template, jsonify, request
from app.main import main_bp
from app.models import Post, Tag, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

@main_bp.route('/')
def index():
    """Home page route."""
    return jsonify({
        'message': 'Welcome to Flask API',
        'version': '1.0.0',
        'status': 'running'
    })

@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': 'connected'
    })

@main_bp.route('/posts')
def get_posts():
    """Get all published posts."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.filter_by(is_published=True)\
        .order_by(Post.published_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })

@main_bp.route('/posts/<slug>')
def get_post(slug):
    """Get a specific post by slug."""
    post = Post.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(post.to_dict())

@main_bp.route('/tags')
def get_tags():
    """Get all tags."""
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])

@main_bp.route('/tags/<slug>')
def get_posts_by_tag(slug):
    """Get posts by tag."""
    tag = Tag.query.filter_by(slug=slug).first()
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = tag.posts.filter_by(is_published=True)\
        .order_by(Post.published_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'tag': tag.to_dict(),
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })
