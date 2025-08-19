from .base_schema import BaseSchema


class ChargingStationCreateSchema(BaseSchema):
    
    def validate(self):
        self.require_field('name', str)
        self.require_field('latitude', (int, float))
        self.require_field('longitude', (int, float))
        self.require_field('charger_type', str)
        self.require_field('power_kw', (int, float))
        self.require_field('num_spots', int)
        self.require_field('status', str)
        self.require_field('state', str)
        self.require_field('city', str)
        
        if 'name' in self.data:
            self.validate_string_length('name', min_length=1, max_length=255)
        
        if 'latitude' in self.data:
            self.validate_numeric_range('latitude', min_val=-90, max_val=90)
        
        if 'longitude' in self.data:
            self.validate_numeric_range('longitude', min_val=-180, max_val=180)
        
        if 'state' in self.data:
            self.validate_string_length('state', min_length=2, max_length=2)
        
        if 'city' in self.data:
            self.validate_string_length('city', min_length=1, max_length=255)
        
        if 'charger_type' in self.data:
            self.validate_choice('charger_type', ['AC', 'DC', 'BOTH'])
        
        if 'power_kw' in self.data:
            self.validate_numeric_range('power_kw', min_val=0.1)
        
        if 'num_spots' in self.data:
            self.validate_numeric_range('num_spots', min_val=1)
            if not isinstance(self.data['num_spots'], int):
                self.add_error('num_spots', 'Number of spots must be an integer')
        
        if 'status' in self.data:
            self.validate_choice('status', ['OPERATIONAL', 'MAINTENANCE', 'INACTIVE'])


class ChargingStationUpdateSchema(BaseSchema):
    
    def validate(self):
        if 'name' in self.data:
            self.require_field('name', str)
            self.validate_string_length('name', min_length=1, max_length=255)
        
        if 'latitude' in self.data:
            self.require_field('latitude', (int, float))
            self.validate_numeric_range('latitude', min_val=-90, max_val=90)
        
        if 'longitude' in self.data:
            self.require_field('longitude', (int, float))
            self.validate_numeric_range('longitude', min_val=-180, max_val=180)
        
        if 'state' in self.data:
            self.require_field('state', str)
            self.validate_string_length('state', min_length=2, max_length=2)
        
        if 'city' in self.data:
            self.require_field('city', str)
            self.validate_string_length('city', min_length=1, max_length=255)
        
        if 'charger_type' in self.data:
            self.require_field('charger_type', str)
            self.validate_choice('charger_type', ['AC', 'DC', 'BOTH'])
        
        if 'power_kw' in self.data:
            self.require_field('power_kw', (int, float))
            self.validate_numeric_range('power_kw', min_val=0.1)
        
        if 'num_spots' in self.data:
            self.require_field('num_spots', int)
            self.validate_numeric_range('num_spots', min_val=1)
            if not isinstance(self.data['num_spots'], int):
                self.add_error('num_spots', 'Number of spots must be an integer')
        
        if 'status' in self.data:
            self.require_field('status', str)
            self.validate_choice('status', ['OPERATIONAL', 'MAINTENANCE', 'INACTIVE'])


ChargingStationSchema = ChargingStationCreateSchema