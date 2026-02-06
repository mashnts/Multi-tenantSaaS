from sqlalchemy.orm import Session
from models import Tenants
from datetime import datetime, timezone

class TenantService:
    def __init__(self, db: Session):
        self.db = db

    def create_tenant(self, company_name:str, plan_id:int):

        tenant = Tenants(
            company_name = company_name,
            plan_id = plan_id,
            created_at = datetime.now(timezone.utc),
            is_active = True
        )

        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def get_tenant(self, tenant_id:int):
        tenant = self.db.query(Tenants).filter_by(id=tenant_id).first()
        return tenant

    def is_active(self, tenant_id: int) -> bool:
        tenant = self.db.query(Tenants).filter_by(id=tenant_id).first()

        if not tenant:
            return False
        
        return tenant.is_active
    

        

    

