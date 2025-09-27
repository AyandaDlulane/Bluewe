from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from auth import router as auth_router
import config

app = FastAPI(
    title="PhishGuard Login",
    description="International login system for browser extension",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include auth routes
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
async def serve_login_page():
    return FileResponse("static/login.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "phishguard-auth"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PhishGuard Login Server...")
    print("📍 Local URL: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)