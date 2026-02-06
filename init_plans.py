from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Plan, PlanType

def create_plans():
    db = SessionLocal()
    
    # Проверяем есть ли уже планы
    existing = db.query(Plan).first()
    if existing:
        print("Планы уже существуют!")
        return
    
    plans = [
        Plan(
            name="Free",
            type=PlanType.FREE,
            price=0.0,
            requests_per_month=1000,
            requests_per_minute=10,
            max_api_keys=1
        ),
        Plan(
            name="Pro",
            type=PlanType.PRO,
            price=29.99,
            requests_per_month=100000,
            requests_per_minute=100,
            max_api_keys=5
        ),
        Plan(
            name="Max",
            type=PlanType.MAX,
            price=99.99,
            requests_per_month=1000000,
            requests_per_minute=1000,
            max_api_keys=20
        )
    ]
    
    for plan in plans:
        db.add(plan)
    
    db.commit()
    print("✅ Планы созданы!")
    db.close()

if __name__ == "__main__":
    init_db()
    create_plans()