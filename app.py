from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes.interview_api import router as interview_router
from routes.voice_api import router as voice_router
import os

app = FastAPI(
    title="CodeOrbit AI Interview Service",
    description="AI-powered mock interview platform",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "service": "CodeOrbit AI Interview Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-interview-service"
    }

# Include routers
# app.include_router(interview_router)
app.include_router(voice_router)