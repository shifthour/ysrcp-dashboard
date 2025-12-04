"""
Vercel Serverless Function Entry Point
Exposes the FastAPI app for Vercel deployment
"""
import sys
import os

# Add backend folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import routes
from routes.api import router as api_router

# Create FastAPI app
app = FastAPI(
    title="YSRCP Political Dashboard API",
    description="Real-time political analytics API for YSRCP vs TDP comparison.",
    version="1.0.0"
)

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "YSRCP Political Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "dashboard": "/api/dashboard",
            "overall_stats": "/api/stats/overall",
            "platform_stats": "/api/stats/platforms",
            "google_trends": "/api/trends/google",
            "hashtags": "/api/hashtags",
            "news": "/api/news",
            "sentiment": "/api/sentiment",
            "health": "/api/health"
        }
    }


# Vercel handler
handler = Mangum(app)
