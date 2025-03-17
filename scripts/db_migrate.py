import asyncio
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

async def run_migrations():
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    # Create engine
    engine = create_engine(database_url)
    
    try:
        # Read and execute initialization SQL
        with open('init/init.sql', 'r') as f:
            sql = f.read()
            
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
            
        print("Database migrations completed successfully")
    except Exception as e:
        print(f"Error running migrations: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_migrations()) 