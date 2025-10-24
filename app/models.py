"""
Database models for the application.
"""
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid

class User(db.Model):
    """User model for authentication and user management."""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """Post model for blog posts or content."""
    __tablename__ = 'posts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    slug = db.Column(db.String(200), unique=True, index=True)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    tags = db.relationship('Tag', secondary='post_tags', backref='posts', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert post to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'slug': self.slug,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': self.author.to_dict() if self.author else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'comment_count': self.comments.count()
        }
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Tag(db.Model):
    """Tag model for categorizing posts."""
    __tablename__ = 'tags'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert tag to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Comment(db.Model):
    """Comment model for post comments."""
    __tablename__ = 'comments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    author_name = db.Column(db.String(100))
    author_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    def to_dict(self):
        """Convert comment to dictionary."""
        return {
            'id': self.id,
            'content': self.content,
            'is_approved': self.is_approved,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'post_id': self.post_id,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<Comment {self.id}>'

# Association table for many-to-many relationship between posts and tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.String(36), db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.String(36), db.ForeignKey('tags.id'), primary_key=True)
)
