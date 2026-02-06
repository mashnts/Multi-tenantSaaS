from sqlalchemy.orm import Session
from models import Usage
from datetime import datetime, timezone, timedelta

class RateLimiter:
    def __init__(self, db:Session):
        self.db = db

    def check_minute_limit(self, tenant_id: int, max_per_minute: int) -> bool:

        one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

        count = self.db.query(Usage).filter(
            Usage.tenant_id == tenant_id,
            Usage.created_at >= one_minute_ago
        ).count()

        return count < max_per_minute
        
    def record_request(self, tenant_id: int):
        now = datetime.now(timezone.utc)
        
        usage = Usage(
            tenant_id = tenant_id,
            requests_count = 1,
            created_at = datetime.now(timezone.utc),
            period_start = now,
            period_end = now
        )

        self.db.add(usage)
        self.db.commit()
        self.db.refresh(usage)
        return usage
    
    def check_month_limit(self, tenant_id: int, max_per_month: int) -> bool:

        month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0)

        count = self.db.query(Usage).filter(
            Usage.tenant_id == tenant_id,
            Usage.created_at >= month_start
        ).count()

        return count < max_per_month
    
    def check_rate_limit(self, tenant_id: int, plan) -> dict:

        if not self.check_minute_limit(tenant_id, plan.requests_per_minute):
            return {
                "allowed": False,
                "reason": "Rate limit exceeded (per minute)"
            }
        
        if not self.check_month_limit(tenant_id, plan.requests_per_month):
            return {
                "allowed": False,
                "reason": "Rate limit exceeded (per month)"
            }
        
        self.record_request(tenant_id)
    
        month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0)
        current_month_usage = self.db.query(Usage).filter(
            Usage.tenant_id == tenant_id,
            Usage.created_at >= month_start
        ).count()
        
        remaining = plan.requests_per_month - current_month_usage
        
        return {
            "allowed": True,
            "remaining_month": remaining
        }