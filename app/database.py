import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from google.cloud.sql.connector import Connector, IPTypes
import pg8000.dbapi

# Cloud SQL connection details
# Replace with your actual Cloud SQL instance connection name
# Example: your-project-id:your-region:your-instance-name
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME", "your-project-id:your-region:your-instance-name")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "your-db-password") # Consider using Secret Manager
DB_NAME = os.environ.get("DB_NAME", "panaderia")

# For local development or if running outside Cloud Run/App Engine
# Set to 'True' if you are testing locally and need direct connection
# Set to 'False' for Cloud Run/App Engine where the Cloud SQL Proxy is used
USE_CLOUD_SQL_CONNECTOR = os.environ.get("USE_CLOUD_SQL_CONNECTOR", "True").lower() == "true"

Base = declarative_base()

if USE_CLOUD_SQL_CONNECTOR:
    # Use Cloud SQL Python Connector for secure connections
    connector = Connector()

    def getconn():
        conn = connector.connect(
            CLOUD_SQL_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type=IPTypes.PUBLIC,
        )
        return conn

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
else:
    # Fallback for direct connection (e.g., local PostgreSQL)
    # Be cautious with exposing credentials directly in production
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
