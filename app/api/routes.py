"""
API routes for CRUD operations.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import Post, Tag, Comment, User
from app import db
from datetime import datetime
import uuid

def admin_required(f):
    """Decorator to require admin privileges."""
    from functools import wraps
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Post management routes
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    published_only = request.args.get('published_only', 'true').lower() == 'true'
    tag_slug = request.args.get('tag')
    
    query = Post.query
    
    if published_only:
        query = query.filter_by(is_published=True)
    
    if tag_slug:
        tag = Tag.query.filter_by(slug=tag_slug).first()
        if tag:
            query = query.filter(Post.tags.contains(tag))
    
    posts = query.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })

@api_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Generate slug from title
    slug = data.get('slug') or data['title'].lower().replace(' ', '-').replace('_', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c in '-').strip('-')
    
    # Ensure slug is unique
    original_slug = slug
    counter = 1
    while Post.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    post = Post(
        title=data['title'],
        content=data['content'],
        excerpt=data.get('excerpt', ''),
        slug=slug,
        is_published=data.get('is_published', False),
        user_id=current_user_id
    )
    
    if post.is_published:
        post.published_at = datetime.utcnow()
    
    try:
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create post'}), 500

@api_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post."""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@api_bp.route('/posts/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update a post."""
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Check if user owns the post or is admin
    user = User.query.get(current_user_id)
    if post.user_id != current_user_id and not user.is_admin:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'excerpt' in data:
        post.excerpt = data['excerpt']
    if 'is_published' in data:
        post.is_published = data['is_published']
        if data['is_published'] and not post.published_at:
            post.published_at = datetime.utcnow()
    
    post.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update post'}), 500

@api_bp.route('/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a post."""
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    
    # Check if user owns the post or is admin
    user = User.query.get(current_user_id)
    if post.user_id != current_user_id and not user.is_admin:
        return jsonify({'error': 'Permission denied'}), 403
    
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post'}), 500

# Tag management routes
@api_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags."""
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])

@api_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    """Create a new tag."""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Tag name is required'}), 400
    
    # Check if tag already exists
    if Tag.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Tag already exists'}), 400
    
    # Generate slug from name
    slug = data.get('slug') or data['name'].lower().replace(' ', '-').replace('_', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c in '-').strip('-')
    
    tag = Tag(
        name=data['name'],
        slug=slug,
        description=data.get('description', '')
    )
    
    try:
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'message': 'Tag created successfully',
            'tag': tag.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create tag'}), 500

# Comment management routes
@api_bp.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get comments for a post."""
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id, is_approved=True).all()
    return jsonify([comment.to_dict() for comment in comments])

@api_bp.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Create a comment for a post."""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Comment content is required'}), 400
    
    comment = Comment(
        content=data['content'],
        post_id=post_id,
        author_name=data.get('author_name', ''),
        author_email=data.get('author_email', '')
    )
    
    # If user is logged in, associate with user
    try:
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if current_user_id:
            comment.user_id = current_user_id
    except:
        pass  # User not logged in, anonymous comment
    
    try:
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment'}), 500

# Admin routes
@api_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    })

@api_bp.route('/admin/comments', methods=['GET'])
@admin_required
def get_all_comments():
    """Get all comments for moderation (admin only)."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    approved_only = request.args.get('approved_only', 'false').lower() == 'true'
    
    query = Comment.query
    if approved_only:
        query = query.filter_by(is_approved=True)
    
    comments = query.order_by(Comment.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'comments': [comment.to_dict() for comment in comments.items],
        'total': comments.total,
        'pages': comments.pages,
        'current_page': page
    })

@api_bp.route('/admin/comments/<comment_id>/approve', methods=['POST'])
@admin_required
def approve_comment(comment_id):
    """Approve a comment (admin only)."""
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    
    try:
        db.session.commit()
        return jsonify({'message': 'Comment approved successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to approve comment'}), 500
