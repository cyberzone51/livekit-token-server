from fastapi import FastAPI, Query, HTTPException
import jwt
import uvicorn
import os
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LiveKit Token Server")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should restrict this to your app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API keys from environment variables
API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")

@app.get("/")
def read_root():
    return {"message": "LiveKit Token Server is running. Use /get_token endpoint to generate tokens."}

@app.get("/get_token")
def get_token(identity: str = Query(..., description="Participant identity"), 
              room: str = Query(..., description="Room name")):
    """
    Generate a LiveKit token for a participant to join a room.
    
    - **identity**: The unique identifier for the participant
    - **room**: The name of the room to join
    """
    if not API_KEY or not API_SECRET:
        raise HTTPException(status_code=500, detail="API_KEY or API_SECRET not configured on the server")
    
    # Create token with permissions
    now = int(time.time())
    exp = now + 86400  # Token expires in 24 hours
    
    # Create claims for the JWT token
    claims = {
        "iss": API_KEY,  # Issuer
        "nbf": now,      # Not Before
        "exp": exp,      # Expiration Time
        "sub": identity, # Subject (participant identity)
        "video": {
            "room": room,
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True
        }
    }
    
    # Generate the JWT token
    token = jwt.encode(claims, API_SECRET, algorithm="HS256")
    
    return {"token": token}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
