"""
YSRCP Political Dashboard - Backend API
FastAPI server providing real-time political analytics

Run with: uvicorn main:app --reload --port 8000
"""

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

# Import Mangum for Vercel serverless deployment
try:
    from mangum import Mangum
    SERVERLESS = True
except ImportError:
    SERVERLESS = False

from routes.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting YSRCP Dashboard API...")
    print("📊 Services: Google Trends, News, Sentiment, Social Media")
    print("🌐 API Documentation: http://localhost:8000/docs")
    yield
    # Shutdown
    print("👋 Shutting down API server...")


# Create FastAPI app
app = FastAPI(
    title="YSRCP Political Dashboard API",
    description="""
    Real-time political analytics API for YSRCP vs TDP comparison.

    ## Features
    - **Google Trends**: Search interest data from Google
    - **News Monitoring**: Real-time news from multiple sources
    - **Sentiment Analysis**: AI-powered sentiment classification
    - **Social Media Stats**: Aggregated metrics from all platforms

    ## Data Sources
    - Google Trends (via pytrends)
    - Google News RSS
    - NewsAPI.org (with API key)
    - Estimated social media metrics

    ## Note
    For production use with real-time social media data,
    consider integrating Brand24 or similar paid services.
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Determine if running in production/Vercel
IS_PRODUCTION = os.getenv('VERCEL', '') or os.getenv('VERCEL_ENV', '')

# Configure CORS - allow all origins in production for Vercel
if IS_PRODUCTION:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # Alternative React port
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ],
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Vercel serverless handler
if SERVERLESS:
    handler = Mangum(app, lifespan="off")
