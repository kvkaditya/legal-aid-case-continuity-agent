from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import cases
from app.database import Base, engine, SessionLocal
from app.database.seed import seed_demo_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed demo data
try:
    with SessionLocal() as db:
        seed_demo_data(db)
except Exception as e:
    print(f"Seed data already exists or error occurred: {e}")

app = FastAPI(
    title="Legal Aid Case Continuity Agent API",
    description="Backend API for Legal Aid Case Continuity",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cases.router)


@app.get("/")
async def root():
    return {
        "message": "Legal Aid Case Continuity Agent API",
        "version": "0.1.0",
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

