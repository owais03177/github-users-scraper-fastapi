from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

# Correct relative imports (this is the fix)
from .database import get_db
from .models import GithubUser
from .schemas import GithubUserRead, GithubUserCreate, GithubUserUpdate
from .crud import get_users, get_user, create_user, update_user, delete_user, filter_users

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub Users Scraper & CRUD API",
    description="Intern Assignment Project - Web Scraping + FastAPI CRUD",
    version="1.0.0"
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# ====================== CRUD ENDPOINTS ======================

@app.get("/items", response_model=List[GithubUserRead])
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all records with pagination"""
    return get_users(db, skip=skip, limit=limit)

@app.get("/items/{item_id}", response_model=GithubUserRead)
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    """Get single record by ID"""
    user = get_user(db, item_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/items/filter", response_model=List[GithubUserRead])
def filter_items(
    name: Optional[str] = Query(None, description="Filter by login name"),
    date: Optional[str] = Query(None, description="Filter by scraped date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Filter records"""
    return filter_users(db, name=name, date=date)

@app.post("/items", response_model=GithubUserRead, status_code=201)
def create_item(user: GithubUserCreate, db: Session = Depends(get_db)):
    """Create new record"""
    return create_user(db, user)

@app.put("/items/{item_id}", response_model=GithubUserRead)
def update_item(item_id: int, user: GithubUserUpdate, db: Session = Depends(get_db)):
    """Update existing record"""
    updated = update_user(db, item_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a record"""
    deleted = delete_user(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "GitHub Users Scraper & FastAPI CRUD API is running!", 
            "docs": "/docs"}