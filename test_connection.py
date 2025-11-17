from db import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database(), current_user();"))
    print(result.all())
