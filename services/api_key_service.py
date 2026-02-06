from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models import API_keys, Tenants
from datetime import datetime
import secrets

class APIKeyService:
    def __init__(self, db: Session):
        self.db = db

    def generate_key(self, tenant_id: int, scopes: str):
        key = secrets.token_urlsafe(32)

        api_key = API_keys(
            key=key,
            tenant_id=tenant_id,
            scopes=scopes,
            is_active=True,
            created_at=datetime.utcnow()
        )

        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)

        return api_key
    
    def get_key_by_value(self, key: str):
        api_key = self.db.query(API_keys).filter_by(key=key).first()
        return api_key
    
    def mark_as_used(self, key: str):
        api_key = self.db.query(API_keys).filter_by(key=key).first()

        if api_key:
            api_key.last_used_at = datetime.now(timezone.utc)

            self.sb.commit()
            return True
        
        return False
    
    def get_tenant_by_key(self, key: str):
        api_key = self.db.query(API_keys).filter_by(key=key).first()
        
        if not api_key:
            return None
        
        return api_key.tenant
    
    def validate_key(self, key:str):
        api_key = self.db.query(API_keys).filter_by(key=key).first()

        if not api_key:
            return False  
    
        if not api_key.is_active:
            return False
        
        api_key.last_used_at = datetime.now(timezone.utc)
        self.db.commit()

        return True
    
    def get_tenant_by_id(self, key:str):
        api_key = self.db.query(API_keys).filter_by(key=key).first()

        if not api_key:
            return None
        
        return api_key.tenant
    
