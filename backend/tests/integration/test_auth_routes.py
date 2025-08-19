
import pytest
import json
from app.models.user import User
from app.utils.database import db


class TestAuthRoutes:
    
    
    def test_register_success(self, client):
        
        user_data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        
        response = client.post('/auth/register', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['message'] == 'User created successfully'
        assert 'user' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['role'] == 'user'  
        assert 'password_hash' not in data['user']
    
    def test_register_duplicate_username(self, client):
        
        user_data = {
            'username': 'duplicate',
            'password': 'pass123'
        }
        
        
        client.post('/auth/register', 
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        
        response = client.post('/auth/register', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Username already exists' in data['message']
    
    def test_register_missing_fields(self, client):
        
        incomplete_data = {
            'username': 'testuser'
            
        }
        
        response = client.post('/auth/register', 
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Username and password are required' in data['message']
    
    def test_register_invalid_json(self, client):
        
        response = client.post('/auth/register', 
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_login_success(self, client):
        
        
        user_data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        client.post('/auth/register', 
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        
        response = client.post('/auth/login', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['message'] == 'Login successful'
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == 'loginuser'
        assert data['user']['role'] == 'user'
    
    def test_login_admin_user(self, client):
        
        
        with client.application.app_context():
            admin = User(username='testadmin', role='admin')
            admin.set_password('adminpass123')
            db.session.add(admin)
            db.session.commit()
        
        login_data = {
            'username': 'testadmin',
            'password': 'adminpass123'
        }
        
        response = client.post('/auth/login', 
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['user']['role'] == 'admin'
    
    def test_login_wrong_password(self, client):
        
        
        user_data = {
            'username': 'wrongpassuser',
            'password': 'correctpass123'
        }
        client.post('/auth/register', 
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        
        wrong_data = {
            'username': 'wrongpassuser',
            'password': 'wrongpass123'
        }
        
        response = client.post('/auth/login', 
                             data=json.dumps(wrong_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid username or password' in data['message']
    
    def test_login_nonexistent_user(self, client):
        
        nonexistent_data = {
            'username': 'nonexistent',
            'password': 'somepass123'
        }
        
        response = client.post('/auth/login', 
                             data=json.dumps(nonexistent_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid username or password' in data['message']
    
    def test_login_missing_fields(self, client):
        
        incomplete_data = {
            'username': 'testuser'
            
        }
        
        response = client.post('/auth/login', 
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Username and password are required' in data['message']
    
    def test_verify_token_valid(self, client, auth_headers):
        
        response = client.get('/auth/verify', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['message'] == 'Token is valid'
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_verify_token_missing(self, client):
        
        response = client.get('/auth/verify')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authorization token is required' in data['message']
    
    def test_verify_token_invalid(self, client):
        
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/auth/verify', headers=headers)
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'invalid or has expired' in data['message']
    
    def test_get_profile_success(self, client, auth_headers):
        
        response = client.get('/auth/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        assert data['user']['role'] == 'user'
    
    def test_get_profile_missing_token(self, client):
        
        response = client.get('/auth/profile')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authorization token is required' in data['message']
    
    def test_get_permissions_user(self, client, auth_headers):
        
        response = client.get('/auth/permissions', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'permissions' in data
        assert data['permissions']['can_view_stations'] is True
        assert data['permissions']['can_manage_stations'] is False
        assert data['permissions']['is_admin'] is False
        assert data['role'] == 'user'
    
    def test_get_permissions_admin(self, client, admin_headers):
        
        response = client.get('/auth/permissions', headers=admin_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'permissions' in data
        assert data['permissions']['can_view_stations'] is True
        assert data['permissions']['can_manage_stations'] is True
        assert data['permissions']['is_admin'] is True
        assert data['role'] == 'admin'
    
    def test_get_permissions_missing_token(self, client):
        
        response = client.get('/auth/permissions')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authorization token is required' in data['message']

