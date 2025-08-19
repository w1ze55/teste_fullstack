from typing import Dict, Any, Optional

from app.models.charging_station import ChargingStation
from app.schemas.charging_station_schema import ChargingStationCreateSchema, ChargingStationUpdateSchema
from .base_service import BaseService


class ChargingStationService(BaseService):
    
    model = ChargingStation
    
    @classmethod
    def create_station(cls, data: Dict[str, Any]) -> ChargingStation:
        schema = ChargingStationCreateSchema(data)
        
        if not schema.is_valid():
            error_messages = [error['message'] for error in schema.get_errors()]
            raise ValueError('; '.join(error_messages))
        
        normalized_data = cls._normalize_station_data(data)
        
        return cls.create(normalized_data)
    
    @classmethod
    def update_station(cls, station_id: int, data: Dict[str, Any]) -> ChargingStation:
        schema = ChargingStationUpdateSchema(data)
        
        if not schema.is_valid():
            error_messages = [error['message'] for error in schema.get_errors()]
            raise ValueError('; '.join(error_messages))
        
        normalized_data = cls._normalize_station_data(data)
        
        return cls.update(station_id, normalized_data)
    
    @classmethod
    def get_stations_with_filters(cls, page: int = 1, per_page: int = 50, 
                                filters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        query = ChargingStation.query
        
        if filters:
            if filters.get('type'):
                query = query.filter(
                    ChargingStation.charger_type == filters['type'].upper()
                )
            
            if filters.get('status'):
                query = query.filter(
                    ChargingStation.status == filters['status'].upper()
                )
            
            if filters.get('state'):
                query = query.filter(
                    ChargingStation.state == filters['state'].upper()
                )
            
            if filters.get('city'):
                query = query.filter(
                    ChargingStation.city.ilike(f"%{filters['city']}%")
                )
            
            if filters.get('min_power'):
                try:
                    min_power = float(filters['min_power'])
                    query = query.filter(ChargingStation.power_kw >= min_power)
                except ValueError:
                    pass
            
            if filters.get('max_power'):
                try:
                    max_power = float(filters['max_power'])
                    query = query.filter(ChargingStation.power_kw <= max_power)
                except ValueError:
                    pass
        
        paginated = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'stations': [station.to_dict() for station in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    
    @classmethod
    def get_stations_by_location(cls, state: Optional[str] = None, 
                               city: Optional[str] = None) -> list:
        query = ChargingStation.get_by_location(state=state, city=city)
        return [station.to_dict() for station in query.all()]
    
    @classmethod
    def get_stations_by_status(cls, status: str) -> list:
        query = ChargingStation.get_by_status(status)
        return [station.to_dict() for station in query.all()]
    
    @classmethod
    def get_stations_by_charger_type(cls, charger_type: str) -> list:
        query = ChargingStation.get_by_charger_type(charger_type)
        return [station.to_dict() for station in query.all()]
    
    @classmethod
    def get_station_stats(cls) -> Dict[str, Any]:
        total_stations = ChargingStation.query.count()
        
        operational = ChargingStation.query.filter_by(status='OPERATIONAL').count()
        maintenance = ChargingStation.query.filter_by(status='MAINTENANCE').count()
        inactive = ChargingStation.query.filter_by(status='INACTIVE').count()
        
        ac_stations = ChargingStation.query.filter_by(charger_type='AC').count()
        dc_stations = ChargingStation.query.filter_by(charger_type='DC').count()
        both_stations = ChargingStation.query.filter_by(charger_type='BOTH').count()
        
        from sqlalchemy import func
        top_states = ChargingStation.query.with_entities(
            ChargingStation.state,
            func.count(ChargingStation.id).label('count')
        ).group_by(ChargingStation.state).order_by(
            func.count(ChargingStation.id).desc()
        ).limit(5).all()
        
        return {
            'total_stations': total_stations,
            'status_distribution': {
                'operational': operational,
                'maintenance': maintenance,
                'inactive': inactive
            },
            'charger_type_distribution': {
                'ac': ac_stations,
                'dc': dc_stations,
                'both': both_stations
            },
            'top_states': [
                {'state': state, 'count': count} 
                for state, count in top_states
            ]
        }
    
    @classmethod
    def _normalize_station_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = data.copy()
        
        enum_fields = ['charger_type', 'status', 'state']
        for field in enum_fields:
            if field in normalized and isinstance(normalized[field], str):
                normalized[field] = normalized[field].upper()
        
        return normalized