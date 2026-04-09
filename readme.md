# GitHub Users Scraper + FastAPI CRUD Application

## 1. Project Overview
This project scrapes GitHub users data (using the GitHub API), stores it in SQLite database, and exposes a full CRUD FastAPI application.

## 2. Setup Instructions
- Python 3.10 or higher
- Create virtual environment: `python -m venv venv`
- Activate it: `.\venv\Scripts\activate`
- Install dependencies: `pip install fastapi uvicorn sqlalchemy pydantic python-dotenv requests`

## 3. Running the Project

1. **Run the Scraper** (to fetch and store data):
   ```bash
   python app/scraper.py

Start the FastAPI Server:Bashpython -m uvicorn app.main:app --reload
Access API Documentation:
Open in browser: http://127.0.0.1:8000/docs

4. Database Setup

SQLite database (github.db) is automatically created and initialized when scraper runs.
Uses SQLAlchemy ORM.

API Examples

GET /items → Get all users (with pagination)
GET /items/{id} → Get single user
GET /items/filter?name=octocat → Filter users
POST /items → Create new user
PUT /items/{id} → Update user
DELETE /items/{id} → Delete user