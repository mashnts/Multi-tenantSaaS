from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.tenant_service import TenantService
from services.api_key_service import APIKeyService
from services.subscription_service import SubscriptionService
from pydantic import BaseModel

router = APIRouter(prefix="/tenants", tags=["Tenants"])

# Pydantic модели для валидации входных данных
class TenantCreate(BaseModel):
    company_name: str
    plan_id: int

class TenantResponse(BaseModel):
    id: int
    company_name: str
    plan_id: int
    is_active: bool
    api_key: str  # Вернем сгенерированный ключ

@router.post("/register", response_model=TenantResponse)
def register_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):
    # 1. Создаем tenant
    tenant_service = TenantService(db)
    tenant = tenant_service.create_tenant(
        company_name=tenant_data.company_name,
        plan_id=tenant_data.plan_id
    )
    
    # 2. Создаем подписку на 30 дней
    subscription_service = SubscriptionService(db)
    subscription_service.create_subscription(
        tenant_id=tenant.id,
        plan_id=tenant_data.plan_id,
        duration_days=30
    )
    
    # 3. Генерируем API ключ
    api_key_service = APIKeyService(db)
    api_key_obj = api_key_service.generate_key(
        tenant_id=tenant.id,
        scopes="read,write"
    )
    
    # 4. Возвращаем данные
    return {
        "id": tenant.id,
        "company_name": tenant.company_name,
        "plan_id": tenant.plan_id,
        "is_active": tenant.is_active,
        "api_key": api_key_obj.key  # Возвращаем строку ключа, а не объект
    }