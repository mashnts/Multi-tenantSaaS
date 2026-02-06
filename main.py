from fastapi import FastAPI
from database import init_db
from routers import tenants, protected

app = FastAPI(title="Multi-tenant SaaS API")

app.include_router(tenants.router)
app.include_router(protected.router)

@app.on_event("startup")
def on_startup():
    init_db()
    print("Database initialized!")

@app.get("/")
def read_root():
    return {"message": "Multi-tenant SaaS API is running"}