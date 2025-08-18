from models import db, User, ChargingStation
from datetime import datetime
import jwt
from flask import current_app

class AuthService:
    @staticmethod
    def create_user(username, password):
        """Create a new user."""
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user and return JWT token."""
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            return token, user
        
        return None, None
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user."""
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(data['user_id'])
        except:
            return None

class StationService:
    @staticmethod
    def validate_station_data(data, partial=False):
        """Validate station data."""
        errors = []
        
        if not partial:
            required_fields = ['name', 'latitude', 'longitude', 'charger_type', 'power_kw', 'num_spots', 'status', 'state', 'city']
            for field in required_fields:
                if field not in data:
                    errors.append(f'{field} is required')
            
            if errors:
                return errors
        
        if 'latitude' in data and not (-90 <= data['latitude'] <= 90):
            errors.append('Latitude must be between -90 and 90')
        
        if 'longitude' in data and not (-180 <= data['longitude'] <= 180):
            errors.append('Longitude must be between -180 and 180')
        
        if 'power_kw' in data and data['power_kw'] <= 0:
            errors.append('Power must be a positive number')
        
        if 'num_spots' in data and (data['num_spots'] <= 0 or not isinstance(data['num_spots'], int)):
            errors.append('Number of spots must be a positive integer')
        
        if 'charger_type' in data and data['charger_type'].upper() not in ['AC', 'DC', 'BOTH']:
            errors.append('Charger type must be AC, DC, or BOTH')
        
        if 'status' in data and data['status'].upper() not in ['OPERATIONAL', 'MAINTENANCE', 'INACTIVE']:
            errors.append('Status must be OPERATIONAL, MAINTENANCE, or INACTIVE')
        
        return errors
    
    @staticmethod
    def get_stations(page=1, per_page=50, filters=None):
        """Get paginated list of stations with optional filters."""
        query = ChargingStation.query
        
        if filters:
            if filters.get('type'):
                query = query.filter(ChargingStation.charger_type == filters['type'].upper())
            if filters.get('status'):
                query = query.filter(ChargingStation.status == filters['status'].upper())
            if filters.get('state'):
                query = query.filter(ChargingStation.state == filters['state'].upper())
        
        stations = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'stations': [station.to_dict() for station in stations.items],
            'total': stations.total,
            'pages': stations.pages,
            'current_page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_station_by_id(station_id):
        """Get station by ID."""
        return ChargingStation.query.get_or_404(station_id)
    
    @staticmethod
    def create_station(data):
        """Create a new charging station."""
        errors = StationService.validate_station_data(data, partial=False)
        if errors:
            raise ValueError('; '.join(errors))
        
        station = ChargingStation(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            charger_type=data['charger_type'].upper(),
            power_kw=data['power_kw'],
            num_spots=data['num_spots'],
            status=data['status'].upper(),
            state=data['state'].upper(),
            city=data['city']
        )
        
        db.session.add(station)
        db.session.commit()
        return station
    
    @staticmethod
    def update_station(station_id, data):
        """Update an existing charging station."""
        station = ChargingStation.query.get_or_404(station_id)
        
        errors = StationService.validate_station_data(data, partial=True)
        if errors:
            raise ValueError('; '.join(errors))
        
        for field in ['name', 'latitude', 'longitude', 'power_kw', 'num_spots', 'state', 'city']:
            if field in data:
                setattr(station, field, data[field])
        
        for field in ['charger_type', 'status']:
            if field in data:
                setattr(station, field, data[field].upper())
        
        station.updated_at = datetime.utcnow()
        db.session.commit()
        return station
    
    @staticmethod
    def delete_station(station_id):
        """Delete a charging station."""
        station = ChargingStation.query.get_or_404(station_id)
        db.session.delete(station)
        db.session.commit()
        return True