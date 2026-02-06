from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.api_key_service import APIKeyService
from models import Tenants

async def verify_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> Tenants:
    api_key_service = APIKeyService(db)
    
    # Проверяем валидность ключа
    if not api_key_service.validate_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or inactive API key"
        )
    
    # Получаем tenant по ключу
    tenant = api_key_service.get_tenant_by_key(x_api_key)
    
    if not tenant:
        raise HTTPException(
            status_code=401,
            detail="Tenant not found"
        )
    
    return tenant