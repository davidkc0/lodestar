"""
Pytest configuration and fixtures.
"""
import pytest
import os
import tempfile
from app import create_app, db
from app.models import User, Post, Tag, Comment

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers for testing."""
    # Create a test user
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('testpassword')
    
    db.session.add(user)
    db.session.commit()
    
    # Login to get token
    response = client.post('/auth/login', json={
        'username_or_email': 'testuser',
        'password': 'testpassword'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(client):
    """Get admin authentication headers for testing."""
    # Create an admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    admin.set_password('adminpassword')
    
    db.session.add(admin)
    db.session.commit()
    
    # Login to get token
    response = client.post('/auth/login', json={
        'username_or_email': 'admin',
        'password': 'adminpassword'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    user = User(
        username='sampleuser',
        email='sample@example.com',
        first_name='Sample',
        last_name='User'
    )
    user.set_password('samplepassword')
    return user

@pytest.fixture
def sample_post(sample_user):
    """Create a sample post for testing."""
    post = Post(
        title='Test Post',
        content='This is a test post content.',
        excerpt='Test excerpt',
        slug='test-post',
        is_published=True,
        user_id=sample_user.id
    )
    return post

@pytest.fixture
def sample_tag():
    """Create a sample tag for testing."""
    tag = Tag(
        name='Test Tag',
        slug='test-tag',
        description='A test tag'
    )
    return tag
