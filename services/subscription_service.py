from sqlalchemy.orm import Session
from models import Subscriptions, SubscriptionStatus
from datetime import datetime, timezone, timedelta

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription(self, tenant_id:int, plan_id:int, duration_days: int):

        date_in = datetime.now(timezone.utc)

        subscription = Subscriptions(
            tenant_id=tenant_id,
            plan_id=plan_id,      
            date_in=date_in,
            date_out=date_in + timedelta(days=duration_days),  
            status=SubscriptionStatus.ACTIVE, 
            history="" 
        )

        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def get_active_subscription(self, tenant_id: int):

        active_subscription = self.db.query(Subscriptions).filter_by(tenant_id = tenant_id, status=SubscriptionStatus.ACTIVE).first()
        return active_subscription
    
    def cancel_subscription(self, subscription_id: int):

        subscription = self.db.query(Subscriptions).filter_by(id=subscription_id).first()

        if not subscription:
            return False
        
        subscription.status = SubscriptionStatus.CANCELED

        self.db.commit()
        return True
    
    def is_subscription_expired(self, subscription_id: int) -> bool:

        subscription = self.db.query(Subscriptions).filter_by(id=subscription_id).first()

        if not subscription:
            return False
        
        if subscription.date_out < datetime.now(timezone.utc):
            return True
    
        return False
        