# LiveKit Token Server

A simple FastAPI server that generates LiveKit tokens for your Android application. This server allows your Android app to work stably regardless of whether your computer is turned on or not.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A LiveKit Cloud account (https://cloud.livekit.io)

### Local Development

1. Clone this repository
2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
3. Edit the `.env` file and add your LiveKit API keys:
   ```
   LIVEKIT_API_KEY=your_api_key_here
   LIVEKIT_API_SECRET=your_api_secret_here
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the server:
   ```
   python main.py
   ```
6. The server will be available at http://localhost:8000

## Deploying to Railway.app

Railway.app is a platform that makes it easy to deploy your applications. Here's how to deploy this token server:

1. Create an account on [Railway.app](https://railway.app)

2. Install the Railway CLI (optional):
   ```
   npm i -g @railway/cli
   ```

3. Login to Railway:
   ```
   railway login
   ```

4. Create a new project:
   ```
   railway init
   ```

5. Add your environment variables:
   ```
   railway variables set LIVEKIT_API_KEY=your_api_key_here LIVEKIT_API_SECRET=your_api_secret_here
   ```

6. Deploy your application:
   ```
   railway up
   ```

Alternatively, you can deploy directly from the Railway dashboard:

1. Go to [Railway.app](https://railway.app) and log in
2. Click "New Project" > "Deploy from GitHub"
3. Select your repository
4. Add the environment variables:
   - `LIVEKIT_API_KEY`: Your LiveKit API key
   - `LIVEKIT_API_SECRET`: Your LiveKit API secret
5. Deploy the application

Once deployed, Railway will provide you with a URL for your token server (e.g., https://livekit-token-server-production.up.railway.app).

## API Endpoints

### GET /get_token

Generates a LiveKit token for a participant to join a room.

**Query Parameters:**
- `identity`: The unique identifier for the participant
- `room`: The name of the room to join

**Example Request:**
```
GET https://your-server-url.railway.app/get_token?identity=user123&room=my-room
```

**Example Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### GET /health

Health check endpoint for monitoring.

**Example Request:**
```
GET https://your-server-url.railway.app/health
```

**Example Response:**
```json
{
  "status": "healthy"
}
```

## Integrating with Android App

Update your Android app to use this token server instead of the LiveKit Sandbox. In your `TokenExt.kt` file, replace the token generation code with a request to your deployed token server.

## Security Considerations

- In production, you should restrict CORS to only allow requests from your app's domain
- Consider adding authentication to your token server to prevent unauthorized access
- Keep your LiveKit API keys secure and never expose them in client-side code
