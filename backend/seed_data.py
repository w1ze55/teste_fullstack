from app import create_app
from models import db, ChargingStation, User

# Sample Brazilian cities with real coordinates
SAMPLE_STATIONS = [
    {
        'name': 'Estação São Paulo - Centro',
        'latitude': -23.5505,
        'longitude': -46.6333,
        'charger_type': 'BOTH',
        'power_kw': 150.0,
        'num_spots': 8,
        'status': 'OPERATIONAL',
        'state': 'SP',
        'city': 'São Paulo'
    },
    {
        'name': 'Carregador Rio de Janeiro - Copacabana',
        'latitude': -22.9068,
        'longitude': -43.1729,
        'charger_type': 'AC',
        'power_kw': 22.0,
        'num_spots': 4,
        'status': 'OPERATIONAL',
        'state': 'RJ',
        'city': 'Rio de Janeiro'
    },
    {
        'name': 'Super Carregador Brasília - Asa Norte',
        'latitude': -15.7801,
        'longitude': -47.9292,
        'charger_type': 'DC',
        'power_kw': 350.0,
        'num_spots': 12,
        'status': 'OPERATIONAL',
        'state': 'DF',
        'city': 'Brasília'
    },
    {
        'name': 'Estação Belo Horizonte - Savassi',
        'latitude': -19.9167,
        'longitude': -43.9345,
        'charger_type': 'BOTH',
        'power_kw': 75.0,
        'num_spots': 6,
        'status': 'MAINTENANCE',
        'state': 'MG',
        'city': 'Belo Horizonte'
    },
    {
        'name': 'Carregador Salvador - Pelourinho',
        'latitude': -12.9714,
        'longitude': -38.5014,
        'charger_type': 'AC',
        'power_kw': 11.0,
        'num_spots': 3,
        'status': 'OPERATIONAL',
        'state': 'BA',
        'city': 'Salvador'
    },
    {
        'name': 'Estação Fortaleza - Aldeota',
        'latitude': -3.7319,
        'longitude': -38.5267,
        'charger_type': 'DC',
        'power_kw': 120.0,
        'num_spots': 5,
        'status': 'OPERATIONAL',
        'state': 'CE',
        'city': 'Fortaleza'
    },
    {
        'name': 'Carregador Recife - Boa Viagem',
        'latitude': -8.1137,
        'longitude': -34.9058,
        'charger_type': 'BOTH',
        'power_kw': 100.0,
        'num_spots': 7,
        'status': 'INACTIVE',
        'state': 'PE',
        'city': 'Recife'
    },
    {
        'name': 'Super Carregador Porto Alegre - Centro',
        'latitude': -30.0346,
        'longitude': -51.2177,
        'charger_type': 'DC',
        'power_kw': 250.0,
        'num_spots': 10,
        'status': 'OPERATIONAL',
        'state': 'RS',
        'city': 'Porto Alegre'
    },
    {
        'name': 'Estação Curitiba - Batel',
        'latitude': -25.4284,
        'longitude': -49.2733,
        'charger_type': 'AC',
        'power_kw': 22.0,
        'num_spots': 4,
        'status': 'OPERATIONAL',
        'state': 'PR',
        'city': 'Curitiba'
    },
    {
        'name': 'Carregador Goiânia - Setor Oeste',
        'latitude': -16.6869,
        'longitude': -49.2648,
        'charger_type': 'BOTH',
        'power_kw': 180.0,
        'num_spots': 9,
        'status': 'MAINTENANCE',
        'state': 'GO',
        'city': 'Goiânia'
    },
    {
        'name': 'Estação Manaus - Centro',
        'latitude': -3.1190,
        'longitude': -60.0217,
        'charger_type': 'DC',
        'power_kw': 80.0,
        'num_spots': 6,
        'status': 'OPERATIONAL',
        'state': 'AM',
        'city': 'Manaus'
    },
    {
        'name': 'Carregador Belém - Nazaré',
        'latitude': -1.4558,
        'longitude': -48.5044,
        'charger_type': 'AC',
        'power_kw': 11.0,
        'num_spots': 3,
        'status': 'OPERATIONAL',
        'state': 'PA',
        'city': 'Belém'
    }
]

def seed_database():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default users
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
        
        if not User.query.filter_by(username='user').first():
            regular_user = User(username='user')
            regular_user.set_password('user123')
            db.session.add(regular_user)
        
        # Add sample charging stations
        for station_data in SAMPLE_STATIONS:
            existing_station = ChargingStation.query.filter_by(
                name=station_data['name']
            ).first()
            
            if not existing_station:
                station = ChargingStation(**station_data)
                db.session.add(station)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()

