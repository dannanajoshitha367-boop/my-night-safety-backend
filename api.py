from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import generate_guidance

# Initialize FastAPI app
app = FastAPI(
    title="AI Night-Safety Companion API",
    description="REST API for night-time safety guidance",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for guidance endpoint
class GuidanceRequest(BaseModel):
    situation: str

# Response model for guidance
class GuidanceResponse(BaseModel):
    status: str
    guidance: str
    alert_level: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Night-Safety Companion API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Check API health"""
    return {
        "status": "healthy",
        "service": "AI Night-Safety Companion API"
    }

@app.post("/api/guidance")
async def get_guidance(request: GuidanceRequest):
    """Get safety guidance for a situation"""
    try:
        guidance = generate_guidance(request.situation)
        return {
            "status": "success",
            "guidance": guidance,
            "alert_level": "info"
        }
    except Exception as e:
        return {
            "status": "error",
            "guidance": "Unable to generate guidance.",
            "error": str(e)
        }

@app.get("/api/emergency-numbers")
async def get_emergency_numbers():
    """Get emergency contact numbers"""
    return {
        "emergency_numbers": {
            "police": "100",
            "ambulance": "108",
            "fire": "101",
            "women_helpline": "1091",
            "disaster_management": "1070"
        }
    }

@app.get("/api/safety-tips")
async def get_safety_tips():
    """Get general safety tips"""
    return {
        "safety_tips": [
            "Always stay aware of your surroundings",
            "Walk in well-lit areas",
            "Trust your instincts",
            "Keep your phone charged",
            "Let someone know your location",
            "Avoid isolated areas at night",
            "Keep emergency contacts ready",
            "Use buddy system when possible"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
