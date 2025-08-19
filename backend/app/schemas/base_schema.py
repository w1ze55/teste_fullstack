from typing import Dict, List, Any


class BaseSchema:
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.errors = []
    
    def is_valid(self) -> bool:
        self.errors = []
        self.validate()
        return len(self.errors) == 0
    
    def validate(self):
        pass
    
    def add_error(self, field: str, message: str):
        self.errors.append({'field': field, 'message': message})
    
    def get_errors(self) -> List[Dict[str, str]]:
        return self.errors
    
    def require_field(self, field: str, field_type: type = None):
        if field not in self.data or self.data[field] is None:
            self.add_error(field, f'{field} is required')
            return False
        
        if field_type and not isinstance(self.data[field], field_type):
            self.add_error(field, f'{field} must be of type {field_type.__name__}')
            return False
            
        return True
    
    def validate_string_length(self, field: str, min_length: int = None, max_length: int = None):
        if field not in self.data:
            return
            
        value = self.data[field]
        if not isinstance(value, str):
            return
            
        if min_length and len(value) < min_length:
            self.add_error(field, f'{field} must be at least {min_length} characters long')
        
        if max_length and len(value) > max_length:
            self.add_error(field, f'{field} must be at most {max_length} characters long')
    
    def validate_numeric_range(self, field: str, min_val: float = None, max_val: float = None):
        if field not in self.data:
            return
            
        value = self.data[field]
        if not isinstance(value, (int, float)):
            return
            
        if min_val is not None and value < min_val:
            self.add_error(field, f'{field} must be at least {min_val}')
        
        if max_val is not None and value > max_val:
            self.add_error(field, f'{field} must be at most {max_val}')
    
    def validate_choice(self, field: str, choices: List[str], case_insensitive: bool = True):
        if field not in self.data:
            return
            
        value = self.data[field]
        if not isinstance(value, str):
            return
        
        comparison_value = value.upper() if case_insensitive else value
        comparison_choices = [c.upper() for c in choices] if case_insensitive else choices
        
        if comparison_value not in comparison_choices:
            self.add_error(field, f'{field} must be one of: {", ".join(choices)}')