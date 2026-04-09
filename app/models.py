from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

# Import Base correctly

class GithubUser():
    __tablename__ = "github_users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    avatar_url = Column(String)
    html_url = Column(String)
    type = Column(String)
    site_admin = Column(Boolean, default=False)
    scraped_at = Column(DateTime, server_default=func.now())