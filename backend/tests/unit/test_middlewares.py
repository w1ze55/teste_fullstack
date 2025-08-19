
import pytest
from unittest.mock import Mock, patch
from flask import Flask, jsonify
from app.middlewares.auth_middleware import token_required, admin_required, optional_auth
from app.models.user import User


class TestAuthMiddleware:
    
    
    def test_token_required_valid_token(self, app):
        
        with app.app_context():
            
            mock_user = User(username='testuser', role='user')
            
            
            @token_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = mock_user
                
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer valid_token'
                    
                    result = test_route()
                    
                    assert mock_verify.called
                    mock_verify.assert_called_with('Bearer valid_token')
    
    def test_token_required_missing_token(self, app):
        
        with app.app_context():
            @token_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            with patch('app.middlewares.auth_middleware.request') as mock_request:
                mock_request.headers.get.return_value = None
                
                result = test_route()
                
                assert result[1] == 401  
    
    def test_token_required_invalid_token(self, app):
        
        with app.app_context():
            @token_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = None
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer invalid_token'
                    
                    result = test_route()
                    
                    assert result[1] == 401  
    
    def test_admin_required_valid_admin(self, app):
        
        with app.app_context():
            
            mock_admin = User(username='admin', role='admin')
            
            @admin_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = mock_admin
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer admin_token'
                    
                    result = test_route()
                    
                    assert mock_verify.called
    
    def test_admin_required_regular_user(self, app):
        
        with app.app_context():
            
            mock_user = User(username='user', role='user')
            
            @admin_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = mock_user
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer user_token'
                    
                    result = test_route()
                    
                    assert result[1] == 403  
    
    def test_admin_required_missing_token(self, app):
        
        with app.app_context():
            @admin_required
            def test_route(current_user):
                return jsonify({'user': current_user.username})
            
            with patch('app.middlewares.auth_middleware.request') as mock_request:
                mock_request.headers.get.return_value = None
                
                result = test_route()
                
                assert result[1] == 401  
    
    def test_optional_auth_with_token(self, app):
        
        with app.app_context():
            mock_user = User(username='testuser', role='user')
            
            @optional_auth
            def test_route(current_user=None):
                if current_user:
                    return jsonify({'user': current_user.username})
                return jsonify({'user': None})
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = mock_user
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer valid_token'
                    
                    result = test_route()
                    
                    assert mock_verify.called
    
    def test_optional_auth_without_token(self, app):
        
        with app.app_context():
            @optional_auth
            def test_route(current_user=None):
                if current_user:
                    return jsonify({'user': current_user.username})
                return jsonify({'user': None})
            
            with patch('app.middlewares.auth_middleware.request') as mock_request:
                mock_request.headers.get.return_value = None
                
                result = test_route()
                
                
                assert result is not None
    
    def test_optional_auth_invalid_token(self, app):
        
        with app.app_context():
            @optional_auth
            def test_route(current_user=None):
                if current_user:
                    return jsonify({'user': current_user.username})
                return jsonify({'user': None})
            
            with patch('app.middlewares.auth_middleware.AuthService.verify_token') as mock_verify:
                mock_verify.return_value = None
                
                with patch('app.middlewares.auth_middleware.request') as mock_request:
                    mock_request.headers.get.return_value = 'Bearer invalid_token'
                    
                    result = test_route()
                    
                    
                    assert result is not None

