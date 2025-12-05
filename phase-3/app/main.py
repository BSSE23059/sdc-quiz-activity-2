from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from pathlib import Path
import time

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/registration_db")

# Retry logic for database connection
def get_db_url():
    max_retries = 5
    for i in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL, echo=False)
            with engine.connect() as conn:
                return DATABASE_URL
        except Exception as e:
            if i < max_retries - 1:
                print(f"Database connection attempt {i+1} failed, retrying in 2 seconds...")
                time.sleep(2)
            else:
                raise

DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy model
class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Registration API",
    description="FastAPI backend with PostgreSQL database",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRegistration(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "john.doe@example.com",
                "password": "secure_password123"
            }
        }

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mount static files (CSS, JS, etc.)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def get_index():
    """Serve the main registration page"""
    templates_dir = Path(__file__).parent / "templates"
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    raise HTTPException(status_code=404, detail="index.html not found")

@app.post("/api/register", response_model=dict, status_code=201)
async def register(user: UserRegistration, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **first_name**: User's first name (1-100 characters)
    - **last_name**: User's last name (1-100 characters)
    - **username**: User's username (3-100 characters)
    - **password**: User's password (6-100 characters)
    """
    try:
        # Check if username already exists
        existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Create new user in database
        db_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=user.password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "success": True,
            "message": "Registration successful!",
            "data": {
                "id": db_user.id,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "username": db_user.username,
                "password": db_user.password,
                "created_at": db_user.created_at.isoformat()
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data", response_model=List[dict])
async def get_data(db: Session = Depends(get_db)):
    """
    Retrieve all submitted user data
    
    Returns a list of all registered users from database
    """
    users = db.query(UserModel).all()
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Kubernetes liveness and readiness probes
    """
    return {
        "status": "healthy",
        "message": "Application is running"
    }

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get registration statistics
    """
    total_users = db.query(UserModel).count()
    return {
        "total_registrations": total_users,
        "status": "active"
    }

# Root redirect to index
@app.get("/index")
async def redirect_index():
    """Redirect to main page"""
    templates_dir = Path(__file__).parent / "templates"
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    raise HTTPException(status_code=404, detail="index.html not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info"
    )
