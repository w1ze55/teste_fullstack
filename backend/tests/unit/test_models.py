
import pytest
from app.models.user import User
from app.models.charging_station import ChargingStation
from app.utils.database import db


class TestUser:
    
    
    def test_create_user(self, app):
        
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpass')
            
            assert user.username == 'testuser'
            assert user.password_hash is not None
            assert user.password_hash != 'testpass'
    
    def test_check_password(self, app):
        
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpass')
            
            assert user.check_password('testpass') is True
            assert user.check_password('wrongpass') is False
    
    def test_user_to_dict(self, app):
        
        with app.app_context():
            user = User(username='testuser', role='user')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert 'id' in user_dict
            assert user_dict['username'] == 'testuser'
            assert user_dict['role'] == 'user'
            assert 'password_hash' not in user_dict
            assert 'created_at' in user_dict
    
    def test_user_default_role(self, app):
        
        with app.app_context():
            user = User(username='testuser')
            assert user.role == 'user'
    
    def test_admin_permissions(self, app):
        
        with app.app_context():
            admin = User(username='admin', role='admin')
            
            assert admin.is_admin() is True
            assert admin.can_manage_stations() is True
            assert admin.can_view_stations() is True
    
    def test_user_permissions(self, app):
        
        with app.app_context():
            user = User(username='user', role='user')
            
            assert user.is_admin() is False
            assert user.can_manage_stations() is False
            assert user.can_view_stations() is True


class TestChargingStation:
    
    
    def test_create_station(self, app):
        
        with app.app_context():
            station = ChargingStation(
                name='Test Station',
                latitude=-23.5505,
                longitude=-46.6333,
                charger_type='AC',
                power_kw=22.0,
                num_spots=4,
                status='OPERATIONAL',
                state='SP',
                city='São Paulo'
            )
            
            assert station.name == 'Test Station'
            assert station.latitude == -23.5505
            assert station.longitude == -46.6333
            assert station.charger_type == 'AC'
            assert station.power_kw == 22.0
            assert station.num_spots == 4
            assert station.status == 'OPERATIONAL'
            assert station.state == 'SP'
            assert station.city == 'São Paulo'
    
    def test_station_to_dict(self, app):
        
        with app.app_context():
            station = ChargingStation(
                name='Test Station',
                latitude=-23.5505,
                longitude=-46.6333,
                charger_type='AC',
                power_kw=22.0,
                num_spots=4,
                status='OPERATIONAL',
                state='SP',
                city='São Paulo'
            )
            db.session.add(station)
            db.session.commit()
            
            station_dict = station.to_dict()
            
            assert 'id' in station_dict
            assert station_dict['name'] == 'Test Station'
            assert station_dict['latitude'] == -23.5505
            assert station_dict['longitude'] == -46.6333
            assert station_dict['charger_type'] == 'AC'
            assert station_dict['power_kw'] == 22.0
            assert station_dict['num_spots'] == 4
            assert station_dict['status'] == 'OPERATIONAL'
            assert station_dict['state'] == 'SP'
            assert station_dict['city'] == 'São Paulo'
    
    def test_get_by_location(self, app):
        
        with app.app_context():
            
            station1 = ChargingStation(
                name='SP Station', latitude=-23.5505, longitude=-46.6333,
                charger_type='AC', power_kw=22.0, num_spots=4,
                status='OPERATIONAL', state='SP', city='São Paulo'
            )
            station2 = ChargingStation(
                name='RJ Station', latitude=-22.9068, longitude=-43.1729,
                charger_type='DC', power_kw=50.0, num_spots=2,
                status='OPERATIONAL', state='RJ', city='Rio de Janeiro'
            )
            
            db.session.add_all([station1, station2])
            db.session.commit()
            
            
            sp_stations = ChargingStation.get_by_location(state='SP').all()
            assert len(sp_stations) == 1
            assert sp_stations[0].state == 'SP'
            
            
            sp_city_stations = ChargingStation.get_by_location(city='São Paulo').all()
            assert len(sp_city_stations) == 1
            assert sp_city_stations[0].city == 'São Paulo'

