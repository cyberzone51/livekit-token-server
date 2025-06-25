from fastapi import FastAPI, Query
from livekit.jwt import AccessToken


import uvicorn
import os
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
        return {"error": "API_KEY or API_SECRET not configured on the server"}, 500
    
    # Create token with permissions
    token = AccessToken(API_KEY, API_SECRET, identity=identity)
    
    # Add grants for the token
    token.add_grant({
        "roomJoin": True,  # Allow joining the room
        "room": room,      # Specify the room
        "canPublish": True,  # Allow publishing audio/video
        "canSubscribe": True,  # Allow subscribing to other participants
        "canPublishData": True  # Allow publishing data
    })
    
    # Generate the JWT token
    jwt_token = token.to_jwt()
    
    return {"token": jwt_token}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
