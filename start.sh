#!/bin/bash
# Startup script for AI Interview Service

# Get port from environment variable (Render sets this automatically)
PORT=${PORT:-8000}

echo "================================================"
echo "CodeOrbit AI Interview Service"
echo "================================================"
echo "Port: $PORT"
echo "Starting server..."
echo "================================================"

# Start uvicorn with proper host and port binding
exec uvicorn app:app \
    --host 0.0.0.0 \
    --port $PORT \
    --timeout-keep-alive 0 \
    --log-level info
