
import pytest
import json
from app.models.user import User
from app.models.charging_station import ChargingStation
from app.utils.database import db


class TestEndToEndWorkflows:
    
    
    def test_complete_user_workflow(self, client):
        
        
        user_data = {
            'username': 'e2euser',
            'password': 'e2epass123'
        }
        
        register_response = client.post('/auth/register',
                                      data=json.dumps(user_data),
                                      content_type='application/json')
        
        assert register_response.status_code == 201
        
        
        login_response = client.post('/auth/login',
                                   data=json.dumps(user_data),
                                   content_type='application/json')
        
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        token = login_data['token']
        
        
        headers = {'Authorization': f'Bearer {token}'}
        permissions_response = client.get('/auth/permissions', headers=headers)
        
        assert permissions_response.status_code == 200
        permissions_data = permissions_response.get_json()
        
        assert permissions_data['permissions']['can_view_stations'] is True
        assert permissions_data['permissions']['can_manage_stations'] is False
        assert permissions_data['role'] == 'user'
        
        
        stations_response = client.get('/api/cargas')
        
        assert stations_response.status_code == 200
        stations_data = stations_response.get_json()
        assert 'stations' in stations_data
        
        
        station_data = {
            'name': 'User Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        create_response = client.post('/api/cargas',
                                    data=json.dumps(station_data),
                                    content_type='application/json',
                                    headers=headers)
        
        assert create_response.status_code == 403
    
    def test_complete_admin_workflow(self, client):
        
        
        with client.application.app_context():
            admin = User(username='e2eadmin', role='admin')
            admin.set_password('adminpass123')
            db.session.add(admin)
            db.session.commit()
        
        
        admin_data = {
            'username': 'e2eadmin',
            'password': 'adminpass123'
        }
        
        login_response = client.post('/auth/login',
                                   data=json.dumps(admin_data),
                                   content_type='application/json')
        
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        admin_token = login_data['token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        
        permissions_response = client.get('/auth/permissions', headers=admin_headers)
        
        assert permissions_response.status_code == 200
        permissions_data = permissions_response.get_json()
        
        assert permissions_data['permissions']['can_view_stations'] is True
        assert permissions_data['permissions']['can_manage_stations'] is True
        assert permissions_data['permissions']['is_admin'] is True
        assert permissions_data['role'] == 'admin'
        
        
        station_data = {
            'name': 'Admin Created Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'DC',
            'power_kw': 50.0,
            'num_spots': 2,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        create_response = client.post('/api/cargas',
                                    data=json.dumps(station_data),
                                    content_type='application/json',
                                    headers=admin_headers)
        
        assert create_response.status_code == 201
        create_data = create_response.get_json()
        station_id = create_data['station']['id']
        
        
        read_response = client.get(f'/api/cargas/{station_id}')
        
        assert read_response.status_code == 200
        read_data = read_response.get_json()
        assert read_data['name'] == 'Admin Created Station'
        assert read_data['charger_type'] == 'DC'
        
        
        update_data = {
            'name': 'Updated Admin Station',
            'status': 'MAINTENANCE'
        }
        
        update_response = client.put(f'/api/cargas/{station_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json',
                                   headers=admin_headers)
        
        assert update_response.status_code == 200
        update_response_data = update_response.get_json()
        assert update_response_data['station']['name'] == 'Updated Admin Station'
        assert update_response_data['station']['status'] == 'MAINTENANCE'
        
        
        verify_response = client.get(f'/api/cargas/{station_id}')
        
        assert verify_response.status_code == 200
        verify_data = verify_response.get_json()
        assert verify_data['name'] == 'Updated Admin Station'
        assert verify_data['status'] == 'MAINTENANCE'
        
        
        delete_response = client.delete(f'/api/cargas/{station_id}',
                                      headers=admin_headers)
        
        assert delete_response.status_code == 200
        
        
        verify_delete_response = client.get(f'/api/cargas/{station_id}')
        assert verify_delete_response.status_code == 404
    
    def test_rbac_enforcement_workflow(self, client):
        
        
        with client.application.app_context():
            
            user = User(username='rbacuser', role='user')
            user.set_password('userpass123')
            db.session.add(user)
            
            
            admin = User(username='rbacadmin', role='admin')
            admin.set_password('adminpass123')
            db.session.add(admin)
            
            
            station = ChargingStation(
                name='RBAC Test Station',
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
            station_id = station.id
        
        
        user_login_data = {'username': 'rbacuser', 'password': 'userpass123'}
        user_login_response = client.post('/auth/login',
                                        data=json.dumps(user_login_data),
                                        content_type='application/json')
        
        user_token = user_login_response.get_json()['token']
        user_headers = {'Authorization': f'Bearer {user_token}'}
        
        
        admin_login_data = {'username': 'rbacadmin', 'password': 'adminpass123'}
        admin_login_response = client.post('/auth/login',
                                         data=json.dumps(admin_login_data),
                                         content_type='application/json')
        
        admin_token = admin_login_response.get_json()['token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        
        user_view_response = client.get('/api/cargas', headers=user_headers)
        admin_view_response = client.get('/api/cargas', headers=admin_headers)
        
        assert user_view_response.status_code == 200
        assert admin_view_response.status_code == 200
        
        
        new_station_data = {
            'name': 'RBAC New Station',
            'latitude': -23.5506,
            'longitude': -46.6334,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        
        user_create_response = client.post('/api/cargas',
                                         data=json.dumps(new_station_data),
                                         content_type='application/json',
                                         headers=user_headers)
        
        admin_create_response = client.post('/api/cargas',
                                          data=json.dumps(new_station_data),
                                          content_type='application/json',
                                          headers=admin_headers)
        
        assert user_create_response.status_code == 403  
        assert admin_create_response.status_code == 201  
        
        
        update_data = {'name': 'RBAC Updated Station'}
        
        user_update_response = client.put(f'/api/cargas/{station_id}',
                                        data=json.dumps(update_data),
                                        content_type='application/json',
                                        headers=user_headers)
        
        admin_update_response = client.put(f'/api/cargas/{station_id}',
                                         data=json.dumps(update_data),
                                         content_type='application/json',
                                         headers=admin_headers)
        
        assert user_update_response.status_code == 403  
        assert admin_update_response.status_code == 200  
        
        
        user_delete_response = client.delete(f'/api/cargas/{station_id}',
                                           headers=user_headers)
        
        assert user_delete_response.status_code == 403  
        
        
        
        
        
    
    def test_error_handling_workflow(self, client):
        
        
        invalid_json_response = client.post('/auth/register',
                                           data='invalid json',
                                           content_type='application/json')
        
        assert invalid_json_response.status_code == 400
        
        
        incomplete_user = {'username': 'incomplete'}
        
        incomplete_response = client.post('/auth/register',
                                        data=json.dumps(incomplete_user),
                                        content_type='application/json')
        
        assert incomplete_response.status_code == 400
        
        
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        
        invalid_auth_response = client.get('/auth/profile',
                                         headers=invalid_headers)
        
        assert invalid_auth_response.status_code == 401
        
        
        not_found_response = client.get('/api/cargas/99999')
        
        assert not_found_response.status_code == 404
        
        
        invalid_route_response = client.get('/api/nonexistent')
        
        assert invalid_route_response.status_code == 404

