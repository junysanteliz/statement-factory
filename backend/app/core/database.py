# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

# Database URLs
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/bank_statements")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/bank_statements")

# For SQLite (development/testing)
SQLITE_URL = "sqlite:///./bank_statements.db"
ASYNC_SQLITE_URL = "sqlite+aiosqlite:///./bank_statements.db"

# Choose database based on environment
USE_POSTGRESQL = os.getenv("USE_POSTGRESQL", "true").lower() == "true"

if USE_POSTGRESQL:
    engine = create_engine(DATABASE_URL)
    async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
else:
    # SQLite for development
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    async_engine = create_async_engine(ASYNC_SQLITE_URL, echo=True)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async dependency
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables function
def create_tables():
    Base.metadata.create_all(bind=engine)

async def create_tables_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)