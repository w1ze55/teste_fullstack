import re
from typing import Dict, Any, Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_coordinates(latitude: float, longitude: float) -> bool:
    return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    if not isinstance(value, str):
        return str(value)
    
    sanitized = ' '.join(value.split())
    
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].strip()
    
    return sanitized


def format_datetime(dt: datetime, format_string: str = '%Y-%m-%d %H:%M:%S') -> str:
    if not isinstance(dt, datetime):
        return str(dt)
    
    return dt.strftime(format_string)


def parse_filters(request_args: Dict[str, Any]) -> Dict[str, Any]:
    filters = {}
    
    filter_mappings = {
        'type': 'charger_type',
        'status': 'status',
        'state': 'state',
        'city': 'city',
        'min_power': 'min_power',
        'max_power': 'max_power'
    }
    
    for param, filter_key in filter_mappings.items():
        value = request_args.get(param)
        if value:
            if isinstance(value, str):
                value = sanitize_string(value)
                if value:
                    filters[filter_key] = value
            else:
                filters[filter_key] = value
    
    return filters


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    import math
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    r = 6371
    
    return c * r


def paginate_query(query, page: int = 1, per_page: int = 50, max_per_page: int = 100):
    per_page = min(per_page, max_per_page)
    page = max(page, 1)
    
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def create_response_dict(data: Any, message: str = None, status: str = 'success') -> Dict[str, Any]:
    response = {
        'status': status,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    response['timestamp'] = datetime.utcnow().isoformat()
    
    return response