from .base_schema import BaseSchema


class UserCreateSchema(BaseSchema):
    
    def validate(self):
        self.require_field('username', str)
        self.require_field('password', str)
        
        if 'username' in self.data:
            self.validate_string_length('username', min_length=3, max_length=80)
            
            username = self.data['username']
            if not username.replace('_', '').isalnum():
                self.add_error('username', 'Username can only contain letters, numbers, and underscores')
        
        if 'password' in self.data:
            self.validate_string_length('password', min_length=6, max_length=128)


class UserLoginSchema(BaseSchema):
    
    def validate(self):
        self.require_field('username', str)
        self.require_field('password', str)
        
        if 'username' in self.data:
            self.validate_string_length('username', min_length=1, max_length=80)
        
        if 'password' in self.data:
            self.validate_string_length('password', min_length=1, max_length=128)


UserSchema = UserCreateSchema