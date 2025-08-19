import jwt
from flask import current_app
from typing import Tuple, Optional

from app.models.user import User
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema
from .base_service import BaseService


class AuthService(BaseService):
    
    model = User
    
    @classmethod
    def create_user(cls, username: str, password: str, role: str = 'user') -> User:
        data = {'username': username, 'password': password}
        schema = UserCreateSchema(data)
        
        if not schema.is_valid():
            error_messages = [error['message'] for error in schema.get_errors()]
            raise ValueError('; '.join(error_messages))
        
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        
        if role not in ['admin', 'user']:
            raise ValueError('Invalid role. Must be admin or user')
        
        user = User(username=username, role=role)
        user.set_password(password)
        return user.save()
    
    @classmethod
    def authenticate_user(cls, username: str, password: str) -> Tuple[Optional[str], Optional[User]]:
        data = {'username': username, 'password': password}
        schema = UserLoginSchema(data)
        
        if not schema.is_valid():
            return None, None
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            token = cls._generate_token(user)
            return token, user
        
        return None, None
    
    @classmethod
    def verify_token(cls, token: str) -> Optional[User]:
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            return User.query.get(data['user_id'])
            
        except (jwt.InvalidTokenError, KeyError):
            return None
    
    @classmethod
    def _generate_token(cls, user: User) -> str:
        payload = {
            'user_id': user.id,
            'username': user.username
        }
        
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()