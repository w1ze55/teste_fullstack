
import pytest
from unittest.mock import Mock, patch
from app.services.auth_service import AuthService
from app.services.charging_station_service import ChargingStationService
from app.models.user import User
from app.models.charging_station import ChargingStation
from app.utils.database import db


class TestAuthService:
    
    
    def test_create_user_default_role(self, app):
        
        with app.app_context():
            user = AuthService.create_user('testuser', 'testpass')
            
            assert user.username == 'testuser'
            assert user.role == 'user'
            assert user.check_password('testpass') is True
    
    def test_create_user_admin_role(self, app):
        
        with app.app_context():
            admin = AuthService.create_user('admin', 'adminpass', 'admin')
            
            assert admin.username == 'admin'
            assert admin.role == 'admin'
            assert admin.is_admin() is True
    
    def test_create_user_invalid_role(self, app):
        
        with app.app_context():
            with pytest.raises(ValueError, match="Invalid role"):
                AuthService.create_user('user', 'pass', 'invalid_role')
    
    def test_create_duplicate_user(self, app):
        
        with app.app_context():
            AuthService.create_user('duplicate', 'pass')
            
            with pytest.raises(ValueError, match="Username already exists"):
                AuthService.create_user('duplicate', 'pass')
    
    def test_authenticate_user_success(self, app):
        
        with app.app_context():
            user = AuthService.create_user('testuser', 'testpass')
            db.session.commit()
            
            token, authenticated_user = AuthService.authenticate_user('testuser', 'testpass')
            
            assert token is not None
            assert authenticated_user.id == user.id
            assert authenticated_user.username == 'testuser'
    
    def test_authenticate_user_wrong_password(self, app):
        
        with app.app_context():
            AuthService.create_user('testuser', 'testpass')
            db.session.commit()
            
            token, user = AuthService.authenticate_user('testuser', 'wrongpass')
            
            assert token is None
            assert user is None
    
    def test_authenticate_nonexistent_user(self, app):
        
        with app.app_context():
            token, user = AuthService.authenticate_user('nonexistent', 'pass')
            
            assert token is None
            assert user is None
    
    @patch('app.services.auth_service.jwt')
    def test_generate_token(self, mock_jwt, app):
        
        with app.app_context():
            user = User(username='testuser', id=1)
            mock_jwt.encode.return_value = 'mocked_token'
            
            token = AuthService.generate_token(user)
            
            assert token == 'mocked_token'
            mock_jwt.encode.assert_called_once()
    
    @patch('app.services.auth_service.jwt')
    def test_verify_token_success(self, mock_jwt, app):
        
        with app.app_context():
            user = User(username='testuser', id=1)
            db.session.add(user)
            db.session.commit()
            
            mock_jwt.decode.return_value = {'user_id': 1, 'username': 'testuser'}
            
            verified_user = AuthService.verify_token('Bearer valid_token')
            
            assert verified_user is not None
            assert verified_user.id == 1
            assert verified_user.username == 'testuser'
    
    @patch('app.services.auth_service.jwt')
    def test_verify_token_invalid(self, mock_jwt, app):
        
        with app.app_context():
            mock_jwt.decode.side_effect = Exception("Invalid token")
            
            verified_user = AuthService.verify_token('Bearer invalid_token')
            
            assert verified_user is None


class TestChargingStationService:
    
    
    def test_create_station(self, app):
        
        with app.app_context():
            station_data = {
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
            
            station = ChargingStationService.create_station(station_data)
            
            assert station.name == 'Test Station'
            assert station.latitude == -23.5505
            assert station.longitude == -46.6333
            assert station.charger_type == 'AC'
            assert station.power_kw == 22.0
            assert station.status == 'OPERATIONAL'
    
    def test_get_stations_with_filters(self, app, sample_station):
        
        with app.app_context():
            
            station2 = ChargingStation(
                name='RJ Station',
                latitude=-22.9068,
                longitude=-43.1729,
                charger_type='DC',
                power_kw=50.0,
                num_spots=2,
                status='MAINTENANCE',
                state='RJ',
                city='Rio de Janeiro'
            )
            db.session.add(station2)
            db.session.commit()
            
            
            filters = {'state': 'SP'}
            stations, total = ChargingStationService.get_stations(filters=filters)
            
            assert total >= 1
            assert all(station.state == 'SP' for station in stations)
            
            
            filters = {'status': 'OPERATIONAL'}
            stations, total = ChargingStationService.get_stations(filters=filters)
            
            assert total >= 1
            assert all(station.status == 'OPERATIONAL' for station in stations)
    
    def test_get_stations_pagination(self, app):
        
        with app.app_context():
            
            for i in range(5):
                station = ChargingStation(
                    name=f'Station {i}',
                    latitude=-23.5505 + i * 0.01,
                    longitude=-46.6333 + i * 0.01,
                    charger_type='AC',
                    power_kw=22.0,
                    num_spots=4,
                    status='OPERATIONAL',
                    state='SP',
                    city='São Paulo'
                )
                db.session.add(station)
            db.session.commit()
            
            
            stations, total = ChargingStationService.get_stations(page=1, per_page=3)
            
            assert len(stations) == 3
            assert total >= 5
    
    def test_update_station(self, app, sample_station):
        
        with app.app_context():
            update_data = {
                'name': 'Updated Station',
                'status': 'MAINTENANCE'
            }
            
            updated_station = ChargingStationService.update_station(
                sample_station.id, 
                update_data
            )
            
            assert updated_station.name == 'Updated Station'
            assert updated_station.status == 'MAINTENANCE'
            assert updated_station.latitude == sample_station.latitude  
    
    def test_delete_station(self, app, sample_station):
        
        with app.app_context():
            station_id = sample_station.id
            
            result = ChargingStationService.delete_station(station_id)
            
            assert result is True
            
            
            deleted_station = ChargingStation.query.get(station_id)
            assert deleted_station is None
    
    def test_get_station_by_id(self, app, sample_station):
        
        with app.app_context():
            station = ChargingStationService.get_station_by_id(sample_station.id)
            
            assert station is not None
            assert station.id == sample_station.id
            assert station.name == sample_station.name
    
    def test_get_nonexistent_station(self, app):
        
        with app.app_context():
            station = ChargingStationService.get_station_by_id(99999)
            
            assert station is None

