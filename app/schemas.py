from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GithubUserBase(BaseModel):
    login: str
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None
    site_admin: bool = False

class GithubUserCreate(GithubUserBase):
    id: int

class GithubUserRead(GithubUserBase):
    id: int
    scraped_at: datetime

    class Config:
        from_attributes = True

class GithubUserUpdate(BaseModel):
    login: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None
    site_admin: Optional[bool] = None