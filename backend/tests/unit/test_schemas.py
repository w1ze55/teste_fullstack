
import pytest
from app.schemas.charging_station_schema import ChargingStationSchema
from app.schemas.user_schema import UserSchema
from app.utils.validators import validate_coordinates, validate_power_kw, validate_num_spots


class TestChargingStationSchema:
    
    
    def test_valid_station_data(self):
        
        valid_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(valid_data)
        
        assert result == {}  
    
    def test_missing_required_fields(self):
        
        incomplete_data = {
            'name': 'Test Station',
            'latitude': -23.5505
            
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(incomplete_data)
        
        assert 'longitude' in result
        assert 'charger_type' in result
        assert 'power_kw' in result
    
    def test_invalid_charger_type(self):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'INVALID',  
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(invalid_data)
        
        assert 'charger_type' in result
    
    def test_invalid_status(self):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'INVALID_STATUS',  
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(invalid_data)
        
        assert 'status' in result
    
    def test_invalid_coordinates(self):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': 91.0,  
            'longitude': 181.0,  
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(invalid_data)
        
        assert 'latitude' in result
        assert 'longitude' in result
    
    def test_invalid_power_kw(self):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': -5.0,  
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(invalid_data)
        
        assert 'power_kw' in result
    
    def test_invalid_num_spots(self):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 0,  
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        schema = ChargingStationSchema()
        result = schema.validate(invalid_data)
        
        assert 'num_spots' in result


class TestUserSchema:
    
    
    def test_valid_user_data(self):
        
        valid_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'role': 'user'
        }
        
        schema = UserSchema()
        result = schema.validate(valid_data)
        
        assert result == {}  
    
    def test_missing_required_fields(self):
        
        incomplete_data = {
            'username': 'testuser'
            
        }
        
        schema = UserSchema()
        result = schema.validate(incomplete_data)
        
        assert 'password' in result
    
    def test_invalid_role(self):
        
        invalid_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'role': 'invalid_role'
        }
        
        schema = UserSchema()
        result = schema.validate(invalid_data)
        
        assert 'role' in result
    
    def test_short_password(self):
        
        invalid_data = {
            'username': 'testuser',
            'password': '123',  
            'role': 'user'
        }
        
        schema = UserSchema()
        result = schema.validate(invalid_data)
        
        assert 'password' in result
    
    def test_short_username(self):
        
        invalid_data = {
            'username': 'ab',  
            'password': 'testpass123',
            'role': 'user'
        }
        
        schema = UserSchema()
        result = schema.validate(invalid_data)
        
        assert 'username' in result


class TestValidators:
    
    
    def test_validate_coordinates_valid(self):
        
        assert validate_coordinates(-23.5505, -46.6333) is True
        assert validate_coordinates(0, 0) is True
        assert validate_coordinates(90, 180) is True
        assert validate_coordinates(-90, -180) is True
    
    def test_validate_coordinates_invalid_latitude(self):
        
        assert validate_coordinates(91, 0) is False
        assert validate_coordinates(-91, 0) is False
    
    def test_validate_coordinates_invalid_longitude(self):
        
        assert validate_coordinates(0, 181) is False
        assert validate_coordinates(0, -181) is False
    
    def test_validate_power_kw_valid(self):
        
        assert validate_power_kw(22.0) is True
        assert validate_power_kw(50.0) is True
        assert validate_power_kw(150.0) is True
        assert validate_power_kw(0.1) is True
    
    def test_validate_power_kw_invalid(self):
        
        assert validate_power_kw(0) is False
        assert validate_power_kw(-5.0) is False
        assert validate_power_kw(500.0) is False  
    
    def test_validate_num_spots_valid(self):
        
        assert validate_num_spots(1) is True
        assert validate_num_spots(4) is True
        assert validate_num_spots(10) is True
    
    def test_validate_num_spots_invalid(self):
        
        assert validate_num_spots(0) is False
        assert validate_num_spots(-1) is False
        assert validate_num_spots(51) is False  

