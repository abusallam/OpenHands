from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Create directories if they don't exist
Path("static").mkdir(exist_ok=True)
Path("static/css").mkdir(exist_ok=True)
Path("static/js").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

app = FastAPI(
    title="AI Agent Coder",
    description="AI Code Generation and Analysis API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files only if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"status": "online", "message": "AI Agent Coder API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8529))
    uvicorn.run(app, host="0.0.0.0", port=port) 