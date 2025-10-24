"""
Tests for authentication functionality.
"""
import pytest
import json
from app.models import User

class TestAuth:
    """Test authentication endpoints."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com'
            # Missing password
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_duplicate_username(self, client, sample_user):
        """Test registration with duplicate username."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.commit()
        
        response = client.post('/auth/register', json={
            'username': 'sampleuser',  # Duplicate username
            'email': 'different@example.com',
            'password': 'password'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Username already exists' in data['error']
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.commit()
        
        response = client.post('/auth/register', json={
            'username': 'differentuser',
            'email': 'sample@example.com',  # Duplicate email
            'password': 'password'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Email already exists' in data['error']
    
    def test_login_success(self, client, sample_user):
        """Test successful login."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.commit()
        
        response = client.post('/auth/login', json={
            'username_or_email': 'sampleuser',
            'password': 'samplepassword'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'sampleuser'
    
    def test_login_with_email(self, client, sample_user):
        """Test login with email instead of username."""
        db = sample_user._sa_instance_state.session
        db.add(sample_user)
        db.commit()
        
        response = client.post('/auth/login', json={
            'username_or_email': 'sample@example.com',
            'password': 'samplepassword'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/auth/login', json={
            'username_or_email': 'nonexistent',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid credentials' in data['error']
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get('/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication."""
        response = client.get('/auth/me')
        
        assert response.status_code == 401
    
    def test_change_password(self, client, auth_headers):
        """Test changing password."""
        response = client.post('/auth/change-password', 
                             headers=auth_headers,
                             json={
                                 'current_password': 'testpassword',
                                 'new_password': 'newpassword123'
                             })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
    
    def test_change_password_wrong_current(self, client, auth_headers):
        """Test changing password with wrong current password."""
        response = client.post('/auth/change-password',
                             headers=auth_headers,
                             json={
                                 'current_password': 'wrongpassword',
                                 'new_password': 'newpassword123'
                             })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Current password is incorrect' in data['error']
    
    def test_logout(self, client, auth_headers):
        """Test logout."""
        response = client.post('/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
