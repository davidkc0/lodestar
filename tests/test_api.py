"""
Tests for API endpoints.
"""
import pytest
import json
from app.models import User, Post, Tag, Comment

class TestAPI:
    """Test API endpoints."""
    
    def test_get_posts(self, client):
        """Test getting all posts."""
        response = client.get('/api/v1/posts')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'posts' in data
        assert 'total' in data
        assert 'pages' in data
    
    def test_create_post(self, client, auth_headers):
        """Test creating a new post."""
        response = client.post('/api/v1/posts',
                             headers=auth_headers,
                             json={
                                 'title': 'Test Post',
                                 'content': 'This is test content.',
                                 'excerpt': 'Test excerpt',
                                 'is_published': True
                             })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'post' in data
        assert data['post']['title'] == 'Test Post'
        assert data['post']['is_published'] == True
    
    def test_create_post_unauthorized(self, client):
        """Test creating post without authentication."""
        response = client.post('/api/v1/posts',
                             json={
                                 'title': 'Test Post',
                                 'content': 'This is test content.'
                             })
        
        assert response.status_code == 401
    
    def test_get_specific_post(self, client, sample_user, sample_post):
        """Test getting a specific post."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        response = client.get(f'/api/v1/posts/{sample_post.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Test Post'
        assert data['content'] == 'This is a test post content.'
    
    def test_update_post(self, client, auth_headers, sample_user, sample_post):
        """Test updating a post."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        # Update the post to belong to the authenticated user
        sample_post.user_id = sample_user.id
        db.commit()
        
        response = client.put(f'/api/v1/posts/{sample_post.id}',
                            headers=auth_headers,
                            json={
                                'title': 'Updated Post Title',
                                'content': 'Updated content.'
                            })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['post']['title'] == 'Updated Post Title'
        assert data['post']['content'] == 'Updated content.'
    
    def test_delete_post(self, client, auth_headers, sample_user, sample_post):
        """Test deleting a post."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        # Update the post to belong to the authenticated user
        sample_post.user_id = sample_user.id
        db.commit()
        
        response = client.delete(f'/api/v1/posts/{sample_post.id}',
                               headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
    
    def test_get_tags(self, client):
        """Test getting all tags."""
        response = client.get('/api/v1/tags')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_create_tag(self, client, auth_headers):
        """Test creating a new tag."""
        response = client.post('/api/v1/tags',
                            headers=auth_headers,
                            json={
                                'name': 'Test Tag',
                                'description': 'A test tag'
                            })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'tag' in data
        assert data['tag']['name'] == 'Test Tag'
    
    def test_create_comment(self, client, sample_user, sample_post):
        """Test creating a comment."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        response = client.post(f'/api/v1/posts/{sample_post.id}/comments',
                             json={
                                 'content': 'This is a test comment.',
                                 'author_name': 'Test Author',
                                 'author_email': 'author@example.com'
                             })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'comment' in data
        assert data['comment']['content'] == 'This is a test comment.'
    
    def test_get_post_comments(self, client, sample_user, sample_post):
        """Test getting comments for a post."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        # Create a comment
        comment = Comment(
            content='Test comment',
            post_id=sample_post.id,
            author_name='Test Author',
            is_approved=True
        )
        db.add(comment)
        db.commit()
        
        response = client.get(f'/api/v1/posts/{sample_post.id}/comments')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['content'] == 'Test comment'
    
    def test_admin_get_users(self, client, admin_headers):
        """Test admin getting all users."""
        response = client.get('/api/v1/admin/users', headers=admin_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'users' in data
        assert 'total' in data
    
    def test_admin_get_users_unauthorized(self, client, auth_headers):
        """Test non-admin trying to get all users."""
        response = client.get('/api/v1/admin/users', headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_admin_approve_comment(self, client, admin_headers, sample_user, sample_post):
        """Test admin approving a comment."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.add(sample_post)
        db.commit()
        
        # Create a comment
        comment = Comment(
            content='Test comment',
            post_id=sample_post.id,
            author_name='Test Author',
            is_approved=False
        )
        db.add(comment)
        db.commit()
        
        response = client.post(f'/api/v1/admin/comments/{comment.id}/approve',
                            headers=admin_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        
        # Verify comment is approved
        updated_comment = Comment.query.get(comment.id)
        assert updated_comment.is_approved == True
