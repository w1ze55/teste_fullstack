import pytest
import json
from app import create_app
from models import db, ChargingStation, User

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app('testing')
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(username='testuser')
            test_user.set_password('testpass')
            db.session.add(test_user)
            db.session.commit()
            
            yield client
            
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers for a test user."""
    response = client.post('/auth/login', 
                          data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
                          content_type='application/json')
    token = json.loads(response.data)['token']
    return {'Authorization': f'Bearer {token}'}

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_user(self, client):
        """Test user registration."""
        response = client.post('/auth/register',
                              data=json.dumps({'username': 'newuser', 'password': 'newpass'}),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
    
    def test_register_duplicate_user(self, client):
        """Test registration with existing username."""
        response = client.post('/auth/register',
                              data=json.dumps({'username': 'testuser', 'password': 'newpass'}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['message']
    
    def test_login_valid_credentials(self, client):
        """Test login with valid credentials."""
        response = client.post('/auth/login',
                              data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert data['username'] == 'testuser'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/auth/login',
                              data=json.dumps({'username': 'testuser', 'password': 'wrongpass'}),
                              content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['message']

class TestChargingStations:
    """Test charging station endpoints."""
    
    def test_get_stations_empty(self, client):
        """Test getting stations when none exist."""
        response = client.get('/cargas')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['stations'] == []
        assert data['total'] == 0
    
    def test_create_station_unauthorized(self, client):
        """Test creating station without authentication."""
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
        response = client.post('/cargas',
                              data=json.dumps(station_data),
                              content_type='application/json')
        assert response.status_code == 401
    
    def test_create_station_valid(self, client, auth_headers):
        """Test creating a valid station."""
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
        response = client.post('/cargas',
                              data=json.dumps(station_data),
                              content_type='application/json',
                              headers=auth_headers)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Station'
        assert data['latitude'] == -23.5505
        assert data['charger_type'] == 'AC'
    
    def test_create_station_invalid_latitude(self, client, auth_headers):
        """Test creating station with invalid latitude."""
        station_data = {
            'name': 'Test Station',
            'latitude': 95.0,  # Invalid latitude
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': 22.0,
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        response = client.post('/cargas',
                              data=json.dumps(station_data),
                              content_type='application/json',
                              headers=auth_headers)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Latitude must be between -90 and 90' in data['message']
    
    def test_create_station_invalid_power(self, client, auth_headers):
        """Test creating station with invalid power."""
        station_data = {
            'name': 'Test Station',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'charger_type': 'AC',
            'power_kw': -10.0,  # Invalid power
            'num_spots': 4,
            'status': 'OPERATIONAL',
            'state': 'SP',
            'city': 'São Paulo'
        }
        response = client.post('/cargas',
                              data=json.dumps(station_data),
                              content_type='application/json',
                              headers=auth_headers)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Power must be a positive number' in data['message']
    
    def test_get_station_by_id(self, client, auth_headers):
        """Test getting a specific station by ID."""
        # First create a station
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
        create_response = client.post('/cargas',
                                     data=json.dumps(station_data),
                                     content_type='application/json',
                                     headers=auth_headers)
        station_id = json.loads(create_response.data)['id']
        
        # Then get it by ID
        response = client.get(f'/cargas/{station_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == station_id
        assert data['name'] == 'Test Station'
    
    def test_get_nonexistent_station(self, client):
        """Test getting a station that doesn't exist."""
        response = client.get('/cargas/999')
        assert response.status_code == 404
    
    def test_update_station(self, client, auth_headers):
        """Test updating a station."""
        # First create a station
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
        create_response = client.post('/cargas',
                                     data=json.dumps(station_data),
                                     content_type='application/json',
                                     headers=auth_headers)
        station_id = json.loads(create_response.data)['id']
        
        # Then update it
        update_data = {
            'name': 'Updated Station',
            'power_kw': 50.0
        }
        response = client.put(f'/cargas/{station_id}',
                             data=json.dumps(update_data),
                             content_type='application/json',
                             headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Station'
        assert data['power_kw'] == 50.0
    
    def test_delete_station(self, client, auth_headers):
        """Test deleting a station."""
        # First create a station
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
        create_response = client.post('/cargas',
                                     data=json.dumps(station_data),
                                     content_type='application/json',
                                     headers=auth_headers)
        station_id = json.loads(create_response.data)['id']
        
        # Then delete it
        response = client.delete(f'/cargas/{station_id}',
                               headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deleted successfully' in data['message']
        
        # Verify it's gone
        get_response = client.get(f'/cargas/{station_id}')
        assert get_response.status_code == 404
    
    def test_filter_stations_by_type(self, client, auth_headers):
        """Test filtering stations by charger type."""
        # Create stations with different types
        stations = [
            {
                'name': 'AC Station',
                'latitude': -23.5505,
                'longitude': -46.6333,
                'charger_type': 'AC',
                'power_kw': 22.0,
                'num_spots': 4,
                'status': 'OPERATIONAL',
                'state': 'SP',
                'city': 'São Paulo'
            },
            {
                'name': 'DC Station',
                'latitude': -23.5506,
                'longitude': -46.6334,
                'charger_type': 'DC',
                'power_kw': 50.0,
                'num_spots': 2,
                'status': 'OPERATIONAL',
                'state': 'SP',
                'city': 'São Paulo'
            }
        ]
        
        for station_data in stations:
            client.post('/cargas',
                       data=json.dumps(station_data),
                       content_type='application/json',
                       headers=auth_headers)
        
        # Filter by AC type
        response = client.get('/cargas?type=AC')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['stations']) == 1
        assert data['stations'][0]['charger_type'] == 'AC'

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

if __name__ == '__main__':
    pytest.main([__file__])