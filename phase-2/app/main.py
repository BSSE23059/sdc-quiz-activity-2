from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import os
from pathlib import Path

app = FastAPI(
    title="User Registration API",
    description="FastAPI backend for user registration",
    version="1.0.0"
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
    first_name: str
    last_name: str
    username: str
    password: str

# In-memory storage for submissions
submitted_data: List[UserResponse] = []

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
async def register(user: UserRegistration):
    """
    Register a new user
    
    - **first_name**: User's first name (1-100 characters)
    - **last_name**: User's last name (1-100 characters)
    - **username**: User's username (3-100 characters)
    - **password**: User's password (6-100 characters)
    """
    try:
        # Create user response
        user_response = UserResponse(**user.dict())
        
        # Store the data
        submitted_data.append(user_response)
        
        return {
            "success": True,
            "message": "Registration successful!",
            "data": user_response.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data", response_model=List[UserResponse])
async def get_data():
    """
    Retrieve all submitted user data
    
    Returns a list of all registered users
    """
    return submitted_data

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
async def get_stats():
    """
    Get registration statistics
    """
    return {
        "total_registrations": len(submitted_data),
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
