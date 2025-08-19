
from typing import Dict, Any, Optional
from app.utils.database import db


class BaseService:
    
    model = None
    
    @classmethod
    def create(cls, data: Dict[str, Any]):
        if not cls.model:
            raise NotImplementedError("Model not specified")
        
        instance = cls.model(**data)
        return instance.save()
    
    @classmethod
    def get_by_id(cls, instance_id: int):
        if not cls.model:
            raise NotImplementedError("Model not specified")
        
        return cls.model.query.get(instance_id)
    
    @classmethod
    def get_by_id_or_404(cls, instance_id: int):
        if not cls.model:
            raise NotImplementedError("Model not specified")
        
        return cls.model.query.get_or_404(instance_id)
    
    @classmethod
    def update(cls, instance_id: int, data: Dict[str, Any]):
        instance = cls.get_by_id_or_404(instance_id)
        
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return instance.save()
    
    @classmethod
    def delete(cls, instance_id: int):
        instance = cls.get_by_id_or_404(instance_id)
        return instance.delete()
    
    @classmethod
    def get_all(cls, page: int = 1, per_page: int = 50):
        if not cls.model:
            raise NotImplementedError("Model not specified")
        
        paginated = cls.model.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'items': [item.to_dict() for item in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
