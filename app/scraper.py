import requests
import time
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import our modules
from database import engine, Base, SessionLocal
from models import GithubUser
from crud import create_user
from schemas import GithubUserCreate

# Create database tables
Base.metadata.create_all(bind=engine)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

print("🚀 Starting GitHub Scraper + Saving to Database...")
print("Creating database tables if not exist...")

db = SessionLocal()

try:
    for page in range(1, 51):   # Reduced to 50 pages for testing (you can increase later)
        url = f"https://api.github.com/users?per_page=10&page={page}"
        print(f"📄 Fetching page {page}...")

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            users = response.json()

            for user in users:
                # Avoid duplicates
                existing = db.query(GithubUser).filter(GithubUser.id == user["id"]).first()
                if existing:
                    continue

                user_data = GithubUserCreate(
                    id=user["id"],
                    login=user["login"],
                    avatar_url=user.get("avatar_url"),
                    html_url=user.get("html_url"),
                    type=user.get("type", "User"),
                    site_admin=user.get("site_admin", False)
                )

                create_user(db, user_data)
                print(f"   ✅ Saved to DB: {user['login']}")

        elif response.status_code in [403, 429]:
            print(f"   ⚠️ Rate limit reached. Stopping.")
            break
        else:
            print(f"   ❌ Error {response.status_code} on page {page}")
            break

        time.sleep(1.0)

    print("\n✅ Scraping finished and data saved to github.db!")

except Exception as e:
    print(f"❌ Error occurred: {e}")
finally:
    db.close()