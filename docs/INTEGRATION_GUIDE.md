# CodeOrbit Integration Guide

Complete guide to integrate the AI Interview Service with CodeOrbit Node.js backend.

## Architecture

```
┌─────────────────────┐
│  React Frontend     │
│  (CodeOrbit UI)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Node.js Backend    │
│  (Express/FastAPI)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Service         │
│  (Python FastAPI)   │
│  Port: 8000         │
└─────────────────────┘
```

## Step 1: Add AI Service Routes to Node Backend

Create `Backend/codeorbit_backend/controllers/ai-interview.controller.js`:

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

// Start Interview
exports.startInterview = async (req, res) => {
  try {
    const { interview_type, difficulty, resume_path } = req.body;
    
    // Get user's coding profile from CodeOrbit
    const codingProfile = {
      leetcode_rating: req.user.leetcodeStats?.rating || null,
      codeforces_rating: req.user.codeforcesStats?.rating || null,
      codechef_rating: req.user.codechefStats?.rating || null,
      strong_topics: req.user.analytics?.strongTopics || [],
      weak_topics: req.user.analytics?.weakTopics || [],
      total_problems_solved: req.user.totalSolved || 0
    };
    
    // Call AI service
    const response = await axios.post(`${AI_SERVICE_URL}/interview/start`, {
      user_id: req.user._id.toString(),
      interview_type,
      difficulty,
      coding_profile: codingProfile
    }, {
      params: { resume_path }
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('AI Service Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to start interview',
      details: error.response?.data || error.message
    });
  }
};

// Upload Resume
exports.uploadResume = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path), req.file.originalname);
    
    const response = await axios.post(
      `${AI_SERVICE_URL}/interview/upload-resume`,
      formData,
      {
        headers: formData.getHeaders()
      }
    );
    
    // Clean up uploaded file
    fs.unlinkSync(req.file.path);
    
    res.json(response.data);
  } catch (error) {
    console.error('Resume Upload Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to upload resume',
      details: error.response?.data || error.message
    });
  }
};

// Submit Answer
exports.submitAnswer = async (req, res) => {
  try {
    const { session_id, answer } = req.body;
    
    const response = await axios.post(`${AI_SERVICE_URL}/interview/answer`, {
      session_id,
      answer
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Submit Answer Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to submit answer',
      details: error.response?.data || error.message
    });
  }
};

// Get Follow-up Question
exports.getFollowup = async (req, res) => {
  try {
    const { session_id } = req.body;
    
    const response = await axios.post(`${AI_SERVICE_URL}/interview/followup`, {
      session_id,
      should_followup: true
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Followup Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to get follow-up question',
      details: error.response?.data || error.message
    });
  }
};

// End Interview
exports.endInterview = async (req, res) => {
  try {
    const { session_id } = req.params;
    
    const response = await axios.post(`${AI_SERVICE_URL}/interview/end/${session_id}`);
    
    res.json(response.data);
  } catch (error) {
    console.error('End Interview Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to end interview',
      details: error.response?.data || error.message
    });
  }
};

// Get Session Status
exports.getSessionStatus = async (req, res) => {
  try {
    const { session_id } = req.params;
    
    const response = await axios.get(`${AI_SERVICE_URL}/interview/session/${session_id}`);
    
    res.json(response.data);
  } catch (error) {
    console.error('Session Status Error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Failed to get session status',
      details: error.response?.data || error.message
    });
  }
};
```

## Step 2: Add Routes

Create `Backend/codeorbit_backend/routes/ai-interview.routes.js`:

```javascript
const express = require('express');
const router = express.Router();
const multer = require('multer');
const authMiddleware = require('../middleware/auth.middleware');
const aiInterviewController = require('../controllers/ai-interview.controller');

// Configure multer for resume uploads
const upload = multer({ dest: 'uploads/' });

// All routes require authentication
router.use(authMiddleware);

// Routes
router.post('/start', aiInterviewController.startInterview);
router.post('/upload-resume', upload.single('resume'), aiInterviewController.uploadResume);
router.post('/answer', aiInterviewController.submitAnswer);
router.post('/followup', aiInterviewController.getFollowup);
router.post('/end/:session_id', aiInterviewController.endInterview);
router.get('/session/:session_id', aiInterviewController.getSessionStatus);

module.exports = router;
```

## Step 3: Register Routes in App

Add to `Backend/codeorbit_backend/app.js`:

```javascript
const aiInterviewRoutes = require('./routes/ai-interview.routes');

// ... other routes ...

app.use('/api/ai-interview', aiInterviewRoutes);
```

## Step 4: Environment Variables

Add to `Backend/codeorbit_backend/.env`:

```env
AI_SERVICE_URL=http://localhost:8000
```

## Step 5: Frontend Integration

Example React component:

```typescript
// Interview.tsx
import { useState } from 'react';
import axios from 'axios';

export default function Interview() {
  const [sessionId, setSessionId] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [report, setReport] = useState(null);

  const startInterview = async () => {
    const response = await axios.post('/api/ai-interview/start', {
      interview_type: 'technical',
      difficulty: 'intermediate'
    });
    
    setSessionId(response.data.session_id);
    setQuestion(response.data.question);
  };

  const submitAnswer = async () => {
    const response = await axios.post('/api/ai-interview/answer', {
      session_id: sessionId,
      answer
    });
    
    setQuestion(response.data.next_question);
    setAnswer('');
  };

  const endInterview = async () => {
    const response = await axios.post(`/api/ai-interview/end/${sessionId}`);
    setReport(response.data.report);
  };

  return (
    <div>
      <h1>AI Mock Interview</h1>
      
      {!sessionId && (
        <button onClick={startInterview}>Start Interview</button>
      )}
      
      {sessionId && !report && (
        <>
          <div>
            <h3>Question:</h3>
            <p>{question}</p>
          </div>
          
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Your answer..."
          />
          
          <button onClick={submitAnswer}>Submit Answer</button>
          <button onClick={endInterview}>End Interview</button>
        </>
      )}
      
      {report && (
        <div>
          <h2>Interview Report</h2>
          <p>Overall Score: {report.overall_score}/10</p>
          <p>Recommendation: {report.hiring_recommendation}</p>
          {/* Display full report */}
        </div>
      )}
    </div>
  );
}
```

## Step 6: Testing Integration

### Test AI Service is Running
```bash
curl http://localhost:8000/health
```

### Test Through Node Backend
```bash
# Start interview
curl -X POST http://localhost:5000/api/ai-interview/start \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "interview_type": "technical",
    "difficulty": "intermediate"
  }'
```

## API Flow Diagram

```
┌──────────┐         ┌───────────┐         ┌──────────┐
│ Frontend │         │   Node    │         │    AI    │
│  React   │────────▶│  Backend  │────────▶│  Service │
└──────────┘         └───────────┘         └──────────┘
     │                     │                      │
     │  Start Interview    │                      │
     │────────────────────▶│  Forward Request     │
     │                     │─────────────────────▶│
     │                     │                      │
     │                     │  Session + Question  │
     │   Session + Q       │◀─────────────────────│
     │◀────────────────────│                      │
     │                     │                      │
     │  Submit Answer      │                      │
     │────────────────────▶│  Forward Answer      │
     │                     │─────────────────────▶│
     │                     │                      │
     │                     │  Evaluation + Next Q │
     │   Evaluation + Q    │◀─────────────────────│
     │◀────────────────────│                      │
     │                     │                      │
     │  End Interview      │                      │
     │────────────────────▶│  End Request         │
     │                     │─────────────────────▶│
     │                     │                      │
     │                     │  Final Report        │
     │   Final Report      │◀─────────────────────│
     │◀────────────────────│                      │
```

## Data Flow Example

### 1. Start Interview Request (Frontend → Node)
```json
POST /api/ai-interview/start
{
  "interview_type": "technical",
  "difficulty": "intermediate"
}
```

### 2. Enhanced Request (Node → AI Service)
```json
POST http://localhost:8000/interview/start
{
  "user_id": "507f1f77bcf86cd799439011",
  "interview_type": "technical",
  "difficulty": "intermediate",
  "coding_profile": {
    "leetcode_rating": 1850,
    "strong_topics": ["DP", "Binary Search"],
    "weak_topics": ["Graphs", "Trie"]
  }
}
```

### 3. Response (AI Service → Node → Frontend)
```json
{
  "session_id": "uuid-here",
  "question": "Hello Arpit, I will be conducting your technical interview today...",
  "stage": "introduction",
  "difficulty": "intermediate"
}
```

## Production Considerations

1. **Session Persistence**: Use MongoDB/Redis instead of in-memory storage
2. **Error Handling**: Implement retry logic and fallbacks
3. **Rate Limiting**: Add rate limits to prevent abuse
4. **Authentication**: Verify tokens at AI service level
5. **Monitoring**: Log all interactions for debugging
6. **Caching**: Cache frequently used data
7. **Scaling**: Run multiple AI service instances behind load balancer

## Environment Setup

### Development
```bash
# Terminal 1: Start AI Service
cd ai-service
python -m uvicorn app:app --reload --port 8000

# Terminal 2: Start Node Backend
cd Backend/codeorbit_backend
npm run dev

# Terminal 3: Start Frontend
cd codolio
npm run dev
```

### Production
Use Docker Compose or Kubernetes to orchestrate all services.

## Troubleshooting

**AI Service not reachable:**
- Check if AI service is running: `curl http://localhost:8000/health`
- Verify AI_SERVICE_URL in Node backend env

**CORS errors:**
- Ensure CORS is configured in AI service `app.py`
- Add Node backend domain to allowed origins

**Session not found:**
- Sessions are in-memory, restart clears them
- Implement persistent storage for production

## Next Steps

1. Deploy AI service to cloud (AWS/GCP/Azure)
2. Add authentication to AI service
3. Implement WebSocket for real-time interview
4. Add voice support on frontend
5. Create interview scheduling system
