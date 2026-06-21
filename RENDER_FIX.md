# 🔧 Render Port Binding Fix

## Problem
Render shows "No open ports detected" and times out because heavy imports (embeddings, ChromaDB) delay server startup.

## Solution Applied

### 1. **app.py Changes** ✅
- Health endpoints defined BEFORE route imports
- Routes imported AFTER basic endpoints
- This ensures `/health` is available immediately
- Heavy imports happen after server binding

### 2. **Start Command** ✅
Use directly in Render dashboard:
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 0
```

### 3. **Render Configuration** ✅

In Render dashboard, set:

**Start Command**:
```
uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 0
```

**Health Check Path**:
```
/health
```

**Environment Variables**:
- `GROQ_API_KEY` = your_key
- `PYTHON_VERSION` = 3.11

## Why This Works

1. **Immediate Port Binding**: Server binds to port immediately
2. **Health Check First**: `/health` endpoint available before heavy imports
3. **Timeout Prevention**: `--timeout-keep-alive 0` prevents connection timeouts
4. **Import Order**: Heavy dependencies load AFTER server starts

## Render Dashboard Settings

### Service Configuration

```yaml
Build Command:
  bash build.sh

Start Command:
  uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 0

Health Check Path:
  /health

Instance Type:
  Starter ($7/month) or higher
```

### Environment Variables

| Key | Value |
|-----|-------|
| GROQ_API_KEY | your_groq_api_key |
| PYTHON_VERSION | 3.11 |

### Disk (Persistent Storage)

| Setting | Value |
|---------|-------|
| Name | vector-db |
| Mount Path | /opt/render/project/src/vector_db |
| Size | 1 GB |

## Deployment Steps

1. **Commit Changes**:
```bash
git add .
git commit -m "Fix Render port binding"
git push
```

2. **In Render Dashboard**:
   - Go to your service
   - Click "Manual Deploy" → "Clear build cache & deploy"
   - OR wait for auto-deploy from GitHub

3. **Watch Logs**:
   - Check for "✅ Server started successfully on port..."
   - Health check should respond within seconds
   - Full app loads in background

4. **Verify Deployment**:
```bash
curl https://your-service.onrender.com/health
```

Should return immediately:
```json
{"status":"healthy","service":"ai-interview-service"}
```

## Expected Startup Sequence

```
[1/3] Binding to port $PORT ✓ (immediate)
[2/3] Starting health endpoint ✓ (1-2 seconds)
[3/3] Loading ML models & routes ⏳ (30-60 seconds)
```

Render detects port is open at step 2, deployment succeeds!

## Troubleshooting

### Still Timing Out?

**Check Start Command**:
```bash
# ✅ CORRECT
uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 0

# ❌ WRONG
bash start.sh  # Adds extra layer
python app.py  # Wrong way to start FastAPI
```

### Check Logs Show Port Binding

Look for:
```
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

If missing, start command is wrong.

### Increase Health Check Timeout

In Render dashboard → Settings:
- Health Check Path: `/health`
- Health Check Timeout: 30 seconds (default is 10)

### Use Smaller Model (Optional)

If loading takes too long, in `services/embeddings.py`:
```python
# Faster alternative
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Already smallest!
)
```

## Testing Locally

```bash
# Simulate Render environment
PORT=10000 uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 0

# In another terminal
curl http://localhost:10000/health
```

Should respond immediately even while models load!

## Success Indicators

✅ Render shows "Live" status
✅ `/health` endpoint responds < 5 seconds
✅ No "port scan timeout" in logs
✅ API docs available at `/docs`

---

**Fixed**: June 21, 2026  
**Issue**: Port binding timeout on Render  
**Solution**: Import routes after health endpoints
