"""
Database module for SQLAlchemy ORM
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

# Use SQLite for development if no PostgreSQL URL is set
database_url = settings.database_url or "sqlite:///./test.db"

engine = create_engine(
    database_url,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

