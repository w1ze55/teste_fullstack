from app.utils.database import db
from .base import BaseModel


class ChargingStation(BaseModel):
    __tablename__ = 'charging_stations'
    
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(2), nullable=False, index=True)
    city = db.Column(db.String(255), nullable=False, index=True)
    charger_type = db.Column(
        db.Enum('AC', 'DC', 'BOTH', name='charger_types'), 
        nullable=False,
        index=True
    )
    power_kw = db.Column(db.Float, nullable=False)
    num_spots = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum('OPERATIONAL', 'MAINTENANCE', 'INACTIVE', name='station_status'), 
        nullable=False,
        index=True
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'charger_type': self.charger_type,
            'power_kw': self.power_kw,
            'num_spots': self.num_spots,
            'status': self.status,
            'state': self.state,
            'city': self.city,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_location(cls, state=None, city=None):
        query = cls.query
        
        if state:
            query = query.filter(cls.state == state.upper())
        if city:
            query = query.filter(cls.city.ilike(f'%{city}%'))
            
        return query
    
    @classmethod
    def get_by_status(cls, status):
        return cls.query.filter(cls.status == status.upper())
    
    @classmethod
    def get_by_charger_type(cls, charger_type):
        return cls.query.filter(cls.charger_type == charger_type.upper())
    
    def __repr__(self):
        return f'<ChargingStation {self.name} - {self.city}/{self.state}>'
