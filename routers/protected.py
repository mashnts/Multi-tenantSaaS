from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import verify_api_key
from models import Tenants
from services.rate_limiter import RateLimiter
import traceback

router = APIRouter(prefix="/api", tags=["Protected API"])

@router.get("/my-info")
def get_my_info(
    tenant: Tenants = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    try:
        return {
            "id": tenant.id,
            "company_name": tenant.company_name,
            "plan": {
                "name": tenant.plan.name,
                "type": tenant.plan.type.value
            },
            "is_active": tenant.is_active
        }
    except Exception as e:
        print(f"ERROR: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/protected-data")
def get_protected_data(
    tenant: Tenants = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    try:
        plan = tenant.plan
        rate_limiter = RateLimiter(db)
        result = rate_limiter.check_rate_limit(tenant.id, plan)
        
        if not result["allowed"]:
            raise HTTPException(status_code=429, detail=result["reason"])
        
        return {
            "message": "Success",
            "remaining": result["remaining_month"]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))