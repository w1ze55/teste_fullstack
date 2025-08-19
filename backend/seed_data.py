from app import create_app
from app.models.user import User
from app.models.charging_station import ChargingStation
from app.utils.database import db

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ Admin user created (username: admin, password: admin123, role: admin)")
        else:
            print("ℹ️  Admin user already exists")
        
        if ChargingStation.query.count() == 0:
            stations = [
                ChargingStation(
                    name='Estação Shopping Ibirapuera',
                    latitude=-23.5875,
                    longitude=-46.6564,
                    charger_type='AC',
                    power_kw=22.0,
                    num_spots=6,
                    status='OPERATIONAL',
                    state='SP',
                    city='São Paulo'
                ),
                ChargingStation(
                    name='Estação Copacabana Beach',
                    latitude=-22.9711,
                    longitude=-43.1822,
                    charger_type='DC',
                    power_kw=50.0,
                    num_spots=4,
                    status='OPERATIONAL',
                    state='RJ',
                    city='Rio de Janeiro'
                ),
                ChargingStation(
                    name='Estação Centro Histórico BH',
                    latitude=-19.9245,
                    longitude=-43.9352,
                    charger_type='BOTH',
                    power_kw=75.0,
                    num_spots=8,
                    status='OPERATIONAL',
                    state='MG',
                    city='Belo Horizonte'
                ),
                ChargingStation(
                    name='Estação Aeroporto Brasília',
                    latitude=-15.8697,
                    longitude=-47.9208,
                    charger_type='DC',
                    power_kw=150.0,
                    num_spots=12,
                    status='OPERATIONAL',
                    state='DF',
                    city='Brasília'
                ),
                ChargingStation(
                    name='Estação Porto Alegre Centro',
                    latitude=-30.0346,
                    longitude=-51.2177,
                    charger_type='AC',
                    power_kw=11.0,
                    num_spots=3,
                    status='MAINTENANCE',
                    state='RS',
                    city='Porto Alegre'
                ),
                ChargingStation(
                    name='Estação Recife Antigo',
                    latitude=-8.0631,
                    longitude=-34.8711,
                    charger_type='DC',
                    power_kw=60.0,
                    num_spots=5,
                    status='OPERATIONAL',
                    state='PE',
                    city='Recife'
                ),
                ChargingStation(
                    name='Estação Salvador Pelourinho',
                    latitude=-12.9714,
                    longitude=-38.5014,
                    charger_type='AC',
                    power_kw=22.0,
                    num_spots=4,
                    status='OPERATIONAL',
                    state='BA',
                    city='Salvador'
                ),
                ChargingStation(
                    name='Estação Fortaleza Beira Mar',
                    latitude=-3.7319,
                    longitude=-38.5267,
                    charger_type='BOTH',
                    power_kw=100.0,
                    num_spots=10,
                    status='OPERATIONAL',
                    state='CE',
                    city='Fortaleza'
                ),
                ChargingStation(
                    name='Estação Curitiba Centro',
                    latitude=-25.4284,
                    longitude=-49.2733,
                    charger_type='AC',
                    power_kw=22.0,
                    num_spots=6,
                    status='INACTIVE',
                    state='PR',
                    city='Curitiba'
                ),
                ChargingStation(
                    name='Estação Manaus Centro',
                    latitude=-3.1190,
                    longitude=-60.0217,
                    charger_type='DC',
                    power_kw=50.0,
                    num_spots=3,
                    status='OPERATIONAL',
                    state='AM',
                    city='Manaus'
                ),
                ChargingStation(
                    name='Estação Campinas Unicamp',
                    latitude=-22.8186,
                    longitude=-47.0647,
                    charger_type='BOTH',
                    power_kw=43.0,
                    num_spots=8,
                    status='OPERATIONAL',
                    state='SP',
                    city='Campinas'
                ),
                ChargingStation(
                    name='Estação Florianópolis Centro',
                    latitude=-27.5954,
                    longitude=-48.5480,
                    charger_type='AC',
                    power_kw=11.0,
                    num_spots=4,
                    status='OPERATIONAL',
                    state='SC',
                    city='Florianópolis'
                ),
                ChargingStation(
                    name='Estação Goiânia Setor Bueno',
                    latitude=-16.7011,
                    longitude=-49.2539,
                    charger_type='DC',
                    power_kw=75.0,
                    num_spots=6,
                    status='MAINTENANCE',
                    state='GO',
                    city='Goiânia'
                ),
                ChargingStation(
                    name='Estação Vitória Centro',
                    latitude=-20.3155,
                    longitude=-40.3128,
                    charger_type='AC',
                    power_kw=22.0,
                    num_spots=5,
                    status='OPERATIONAL',
                    state='ES',
                    city='Vitória'
                ),
                ChargingStation(
                    name='Estação Campo Grande Centro',
                    latitude=-20.4697,
                    longitude=-54.6201,
                    charger_type='BOTH',
                    power_kw=50.0,
                    num_spots=7,
                    status='OPERATIONAL',
                    state='MS',
                    city='Campo Grande'
                )
            ]
            
            for station in stations:
                db.session.add(station)
            
            print(f"✅ {len(stations)} charging stations created")
        else:
            print(f"ℹ️  Database already has {ChargingStation.query.count()} charging stations")
        
        db.session.commit()
        print("🎉 Database seeded successfully!")
        
        print(f"\n📊 Database Summary:")
        print(f"   👥 Users: {User.query.count()}")
        print(f"   ⚡ Charging Stations: {ChargingStation.query.count()}")
        print(f"   🟢 Operational: {ChargingStation.query.filter_by(status='OPERATIONAL').count()}")
        print(f"   🟡 Maintenance: {ChargingStation.query.filter_by(status='MAINTENANCE').count()}")
        print(f"   🔴 Inactive: {ChargingStation.query.filter_by(status='INACTIVE').count()}")

if __name__ == '__main__':
    seed_database()
