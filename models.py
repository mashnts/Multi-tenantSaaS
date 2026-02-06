from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum, Date, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()

class PlanType(Enum):
    FREE = "free"
    PRO = "pro"
    MAX = "max"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    CANCELED = 'canceled'
    PAST_DUE = "past_due"
    TRIALING = "trialing"

class InvoiceStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float, nullable=False)
    type = Column(SQLEnum(PlanType), nullable=False)
    requests_per_month = Column(Integer)
    requests_per_minute = Column(Integer)
    max_api_keys = Column(Integer)
    
    tenants = relationship("Tenants", back_populates="plan")

class Tenants(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    created_at = Column(Date, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    is_active = Column(Boolean, nullable=False)
    
    plan = relationship("Plan", back_populates="tenants")
    subscriptions = relationship("Subscriptions", back_populates="tenant")
    api_keys = relationship("API_keys", back_populates="tenant")
    invoices = relationship("Invoices", back_populates="tenant")
    usage = relationship("Usage", back_populates="tenant")

class Subscriptions(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    date_in = Column(Date, nullable=False)
    date_out = Column(Date, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), nullable=False)
    history = Column(String, nullable=False)
    
    tenant = relationship("Tenants", back_populates="subscriptions")
    invoices = relationship("Invoices", back_populates="subscription")

class API_keys(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime)
    last_used_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False)
    scopes = Column(String, nullable=False)
    
    tenant = relationship("Tenants", back_populates="api_keys")

class Usage(Base):
    __tablename__ = "usage"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    requests_count = Column(Integer, default=0)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    
    tenant = relationship("Tenants", back_populates="usage")

class Invoices(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False)
    paid_at = Column(Date)
    history = Column(String, nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    status = Column(SQLEnum(InvoiceStatus), nullable=False)
    
    tenant = relationship("Tenants", back_populates="invoices")
    subscription = relationship("Subscriptions", back_populates="invoices")