# Quick Start Guide - CodeOrbit AI Interview Service

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ (for CodeOrbit backend)
- Groq API Key ([Get one free](https://console.groq.com/))

---

## Step 1: Setup AI Service

### Windows
```bash
cd ai-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac
```bash
cd ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2: Configure Environment

Create `ai-service/.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Step 3: Start AI Service

### Windows
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
uvicorn app:app --reload --port 8000
```

Service will be available at: **http://localhost:8000**

---

## Step 4: Test the Service

```bash
# Terminal 1 - AI Service running

# Terminal 2 - Run test
python test_api.py
```

Or use curl:
```bash
curl http://localhost:8000/health
```

---

## Step 5: Integrate with CodeOrbit Backend

### Add to Backend .env
```env
AI_SERVICE_URL=http://localhost:8000
```

### Start Node Backend
```bash
cd Backend/codeorbit_backend
npm install
npm run dev
```

---

## Step 6: Test Full Integration

```bash
# Start an interview
curl -X POST http://localhost:5000/api/ai-interview/start \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "interview_type": "technical",
    "difficulty": "intermediate"
  }'
```

---

## API Endpoints Summary

### AI Service (Port 8000)
- `GET /health` - Health check
- `POST /interview/start` - Start interview
- `POST /interview/answer` - Submit answer
- `POST /interview/end/{id}` - End interview

### Node Backend (Port 5000)
- `POST /api/ai-interview/start`
- `POST /api/ai-interview/upload-resume`
- `POST /api/ai-interview/answer`
- `POST /api/ai-interview/end/:session_id`

---

## Interview Types

- `hr` - HR/Behavioral
- `technical` - Frontend/Backend/Full Stack
- `dsa` - Data Structures & Algorithms
- `competitive` - Competitive Programming
- `mixed` - All combined

## Difficulty Levels

- `beginner`
- `intermediate`
- `advanced`

---

## Troubleshooting

**Import Error:**
```bash
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Change port
uvicorn app:app --reload --port 8001
```

**AI Service Not Reachable:**
- Check if service is running: `curl http://localhost:8000/health`
- Check firewall settings
- Verify AI_SERVICE_URL in backend .env

---

## Next Steps

1. ✅ Service running
2. ✅ Test basic endpoints
3. 📱 Build frontend UI
4. 🎤 Add voice support (optional)
5. 📊 View interview reports

See **INTEGRATION_GUIDE.md** for detailed integration steps.
See **README.md** for complete documentation.
