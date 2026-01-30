# backend/app/models/customer.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), default="USA")
    date_of_birth = Column(DateTime)
    ssn_last_4 = Column(String(4))  # For verification, store only last 4
    customer_since = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="active")  # active, inactive, suspended
    risk_category = Column(String(20), default="standard")
    notes = Column(Text)
    
    # Relationships
    loans = relationship("Loan", back_populates="customer", cascade="all, delete-orphan")
    statements = relationship("Statement", back_populates="customer")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.full_name}, customer_id={self.customer_id})>"