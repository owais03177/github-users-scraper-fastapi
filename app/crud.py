from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import or_

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GithubUser).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.GithubUser).filter(models.GithubUser.id == user_id).first()

def filter_users(db: Session, name: str = None, date: str = None):
    query = db.query(models.GithubUser)
    if name:
        query = query.filter(models.GithubUser.login.ilike(f"%{name}%"))
    if date:
        query = query.filter(models.GithubUser.scraped_at.cast("date") == date)
    return query.all()

def create_user(db: Session, user: schemas.GithubUserCreate):
    db_user = models.GithubUser(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.GithubUserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user