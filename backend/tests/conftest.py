
import pytest
from app import create_app
from app.utils.database import db
from app.models.user import User
from app.models.charging_station import ChargingStation


@pytest.fixture
def app():

    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def runner(app):

    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):

    user_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    client.post('/auth/register', json=user_data)
    response = client.post('/auth/login', json=user_data)
    token = response.get_json()['token']
    
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client):

    from app.services.auth_service import AuthService
    from app.utils.database import db
    

    admin_user = AuthService.create_user('testadmin', 'adminpass123', 'admin')
    db.session.commit()
    

    user_data = {'username': 'testadmin', 'password': 'adminpass123'}
    response = client.post('/auth/login', json=user_data)
    token = response.get_json()['token']
    
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_user():

    user = User(username='sampleuser', role='user')
    user.set_password('samplepass123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_admin():

    admin = User(username='sampleadmin', role='admin')
    admin.set_password('adminpass123')
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture
def sample_station():

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
    return station

