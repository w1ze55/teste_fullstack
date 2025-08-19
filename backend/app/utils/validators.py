import re
from typing import List, Any, Optional


class ValidationError(Exception):
    pass


def validate_required_fields(data: dict, required_fields: List[str]) -> None:
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")


def validate_string_field(value: Any, field_name: str, min_length: int = 1, 
                         max_length: Optional[int] = None, pattern: Optional[str] = None) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    
    if len(value) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters long")
    
    if max_length and len(value) > max_length:
        raise ValidationError(f"{field_name} must be at most {max_length} characters long")
    
    if pattern and not re.match(pattern, value):
        raise ValidationError(f"{field_name} format is invalid")


def validate_numeric_field(value: Any, field_name: str, min_value: Optional[float] = None,
                          max_value: Optional[float] = None, allow_int_only: bool = False) -> None:
    if allow_int_only:
        if not isinstance(value, int):
            raise ValidationError(f"{field_name} must be an integer")
    else:
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field_name} must be a number")
    
    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")
    
    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}")


def validate_choice_field(value: Any, field_name: str, choices: List[str], 
                         case_insensitive: bool = True) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    
    if case_insensitive:
        normalized_value = value.upper()
        normalized_choices = [choice.upper() for choice in choices]
        
        if normalized_value not in normalized_choices:
            raise ValidationError(f"{field_name} must be one of: {', '.join(choices)}")
        
        return normalized_value
    else:
        if value not in choices:
            raise ValidationError(f"{field_name} must be one of: {', '.join(choices)}")
        
        return value


def validate_coordinates_strict(latitude: Any, longitude: Any) -> tuple:
    if not isinstance(latitude, (int, float)):
        raise ValidationError("Latitude must be a number")
    
    if not isinstance(longitude, (int, float)):
        raise ValidationError("Longitude must be a number")
    
    if not (-90 <= latitude <= 90):
        raise ValidationError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= longitude <= 180):
        raise ValidationError("Longitude must be between -180 and 180 degrees")
    
    return float(latitude), float(longitude)


def validate_brazilian_state(state: Any) -> str:
    if not isinstance(state, str):
        raise ValidationError("State must be a string")
    
    state = state.upper().strip()
    
    if len(state) != 2:
        raise ValidationError("State must be a 2-character code")
    
    valid_states = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    if state not in valid_states:
        raise ValidationError(f"Invalid Brazilian state code: {state}")
    
    return state


def validate_username(username: Any) -> str:
    if not isinstance(username, str):
        raise ValidationError("Username must be a string")
    
    username = username.strip()
    
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long")
    
    if len(username) > 80:
        raise ValidationError("Username must be at most 80 characters long")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Username can only contain letters, numbers, and underscores")
    
    return username


def validate_password(password: Any) -> str:
    if not isinstance(password, str):
        raise ValidationError("Password must be a string")
    
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long")
    
    if len(password) > 128:
        raise ValidationError("Password must be at most 128 characters long")
    
    return password


def validate_coordinates(latitude, longitude):
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (-90 <= lat <= 90):
            return False
        if not (-180 <= lon <= 180):
            return False
        
        return True
    except (ValueError, TypeError):
        return False


def validate_power_kw(power):
    try:
        power_val = float(power)
        return 0 < power_val <= 400
    except (ValueError, TypeError):
        return False


def validate_num_spots(spots):
    try:
        spots_val = int(spots)
        return 1 <= spots_val <= 50
    except (ValueError, TypeError):
        return False