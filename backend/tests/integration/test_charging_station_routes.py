
import pytest
import json
from app.models.charging_station import ChargingStation
from app.utils.database import db


class TestChargingStationRoutes:
    
    
    def test_get_stations_success(self, client):
        
        response = client.get('/api/cargas')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'stations' in data
        assert 'total' in data
        assert 'pages' in data
        assert 'current_page' in data
        assert isinstance(data['stations'], list)
    
    def test_get_stations_with_filters(self, client, sample_station):
        
        
        response = client.get('/api/cargas?state=SP')
        
        assert response.status_code == 200
        data = response.get_json()
        
        
        for station in data['stations']:
            assert station['state'] == 'SP'
    
    def test_get_stations_with_pagination(self, client):
        
        
        with client.application.app_context():
            for i in range(5):
                station = ChargingStation(
                    name=f'Test Station {i}',
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
        
        
        response = client.get('/api/cargas?page=1&per_page=3')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert len(data['stations']) <= 3
        assert data['current_page'] == 1
    
    def test_get_station_by_id_success(self, client, sample_station):
        
        response = client.get(f'/api/cargas/{sample_station.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['id'] == sample_station.id
        assert data['name'] == sample_station.name
        assert data['state'] == sample_station.state
    
    def test_get_station_by_id_not_found(self, client):
        
        response = client.get('/api/cargas/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Station not found' in data['message']
    
    def test_create_station_success_admin(self, client, admin_headers):
        
        station_data = {
            'name': 'New Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        response = client.post('/api/cargas',
                             data=json.dumps(station_data),
                             content_type='application/json',
                             headers=admin_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['message'] == 'Charging station created successfully'
        assert 'station' in data
        assert data['station']['name'] == 'New Test Station'
        assert data['station']['state'] == 'SP'
    
    def test_create_station_forbidden_user(self, client, auth_headers):
        
        station_data = {
            'name': 'New Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        response = client.post('/api/cargas',
                             data=json.dumps(station_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'Only administrators can perform this action' in data['message']
    
    def test_create_station_no_auth(self, client):
        
        station_data = {
            'name': 'New Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        response = client.post('/api/cargas',
                             data=json.dumps(station_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authentication required' in data['message']
    
    def test_create_station_invalid_data(self, client, admin_headers):
        
        invalid_data = {
            'name': 'Test Station',
            'latitude': 91.0,  
            'longitude': -46.6333,
            'charger_type': 'INVALID',  
            'power_kw': -5.0,  
            'num_spots': 0,  
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        response = client.post('/api/cargas',
                             data=json.dumps(invalid_data),
                             content_type='application/json',
                             headers=admin_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'Validation error' in data['message']
    
    def test_update_station_success_admin(self, client, admin_headers, sample_station):
        
        update_data = {
            'name': 'Updated Station Name',
            'status': 'MAINTENANCE'
        }
        
        response = client.put(f'/api/cargas/{sample_station.id}',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=admin_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['message'] == 'Charging station updated successfully'
        assert data['station']['name'] == 'Updated Station Name'
        assert data['station']['status'] == 'MAINTENANCE'
    
    def test_update_station_forbidden_user(self, client, auth_headers, sample_station):
        
        update_data = {
            'name': 'Updated Station Name'
        }
        
        response = client.put(f'/api/cargas/{sample_station.id}',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=auth_headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'Only administrators can perform this action' in data['message']
    
    def test_update_station_not_found(self, client, admin_headers):
        
        update_data = {
            'name': 'Updated Station Name'
        }
        
        response = client.put('/api/cargas/99999',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=admin_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Station not found' in data['message']
    
    def test_update_station_no_auth(self, client, sample_station):
        
        update_data = {
            'name': 'Updated Station Name'
        }
        
        response = client.put(f'/api/cargas/{sample_station.id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authentication required' in data['message']
    
    def test_delete_station_success_admin(self, client, admin_headers, sample_station):
        
        station_id = sample_station.id
        
        response = client.delete(f'/api/cargas/{station_id}',
                               headers=admin_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['message'] == 'Charging station deleted successfully'
        
        
        get_response = client.get(f'/api/cargas/{station_id}')
        assert get_response.status_code == 404
    
    def test_delete_station_forbidden_user(self, client, auth_headers, sample_station):
        
        response = client.delete(f'/api/cargas/{sample_station.id}',
                               headers=auth_headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'Only administrators can perform this action' in data['message']
    
    def test_delete_station_not_found(self, client, admin_headers):
        
        response = client.delete('/api/cargas/99999',
                               headers=admin_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'Station not found' in data['message']
    
    def test_delete_station_no_auth(self, client, sample_station):
        
        response = client.delete(f'/api/cargas/{sample_station.id}')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Authentication required' in data['message']
    
    def test_get_stations_complex_filters(self, client):
        
        
        with client.application.app_context():
            stations_data = [
                {'name': 'SP AC Station', 'state': 'SP', 'charger_type': 'AC', 'status': 'OPERATIONAL'},
                {'name': 'SP DC Station', 'state': 'SP', 'charger_type': 'DC', 'status': 'OPERATIONAL'},
                {'name': 'RJ AC Station', 'state': 'RJ', 'charger_type': 'AC', 'status': 'MAINTENANCE'},
                {'name': 'RJ DC Station', 'state': 'RJ', 'charger_type': 'DC', 'status': 'OPERATIONAL'},
            ]
            
            for i, station_data in enumerate(stations_data):
                station = ChargingStation(
                    name=station_data['name'],
                    latitude=-23.5505 + i * 0.01,
                    longitude=-46.6333 + i * 0.01,
                    charger_type=station_data['charger_type'],
                    power_kw=22.0,
                    num_spots=4,
                    status=station_data['status'],
                    state=station_data['state'],
                    city='Test City'
                )
                db.session.add(station)
            db.session.commit()
        
        
        response = client.get('/api/cargas?state=SP&type=AC&status=OPERATIONAL')
        
        assert response.status_code == 200
        data = response.get_json()
        
        
        for station in data['stations']:
            assert station['state'] == 'SP'
            assert station['charger_type'] == 'AC'
            assert station['status'] == 'OPERATIONAL'

