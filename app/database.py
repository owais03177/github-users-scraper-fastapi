from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Create the database engine (SQLite)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Function to get database session (we will use this in FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()