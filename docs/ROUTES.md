# API Routes Documentation

## 🛣️ routes/ - API Endpoints

### `routes/interview_api.py` - Main Interview APIs

**Purpose**: RESTful endpoints for interview operations

**Prefix**: `/interview`

---

#### **POST /interview/upload-resume**

**Purpose**: Upload and analyze resume PDF

**Request**:
```python
Content-Type: multipart/form-data
file: resume.pdf
```

**Process**:
1. Validate PDF format
2. Save to `uploads/` directory
3. Parse with resumeParser
4. Analyze with resume_analyzer
5. Return path + analysis

**Response**:
```json
{
  "success": true,
  "data": {
    "message": "Resume uploaded successfully",
    "path": "uploads/resume.pdf",
    "analysis": {
      "name": "Arpit",
      "skills": ["React", "Node.js"],
      "projects": [...]
    }
  }
}
```

**Error Codes**:
- 400: Not a PDF file
- 500: Upload/parsing failed

---

#### **POST /interview/start**

**Purpose**: Start new interview session

**Request Body**:
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "interview_type": "react",
  "difficulty": "intermediate",
  "coding_profile": {
    "leetcode_rating": 1850,
    "strong_topics": ["DP"],
    "weak_topics": ["Graphs"]
  }
}
```

**Query Params**:
```
?resume_path=uploads/resume.pdf (optional)
```

**Process**:
1. Create session (session_manager)
2. If resume_path: analyze resume
3. Generate introduction question
4. Store in session
5. Return session_id + first question

**Response**:
```json
{
  "success": true,
  "data": {
    "session_id": "abc-123-xyz",
    "message": "Interview started successfully",
    "question": "Hello Arpit, introduce yourself...",
    "stage": "introduction",
    "difficulty": "intermediate"
  }
}
```

**Error Codes**:
- 400: Missing required fields
- 500: Session creation failed

---

#### **POST /interview/answer**

**Purpose**: Submit answer and get next question

**Request Body**:
```json
{
  "session_id": "abc-123-xyz",
  "answer": "I'm a full-stack developer..."
}
```

**Process**:
1. Get session
2. Evaluate answer (answer_evaluator)
3. Store Q&A in conversation_history
4. Check difficulty adjustment
5. Generate next question
6. Update session scores
7. Return evaluation + next question

**Response**:
```json
{
  "success": true,
  "data": {
    "evaluation": {
      "overall_score": 8.4,
      "technical_accuracy": 8.0,
      "depth": 7.5,
      "clarity": 9.0,
      "completeness": 8.5,
      "communication": 9.0,
      "strengths": ["Clear communication"],
      "weaknesses": ["Could elaborate more"],
      "feedback": "Good introduction...",
      "confidence_level": "high"
    },
    "next_question": "Tell me about CodeOrbit...",
    "stage": "resume_discussion",
    "difficulty": "intermediate",
    "overall_score": 8.4,
    "questions_answered": 1
  }
}
```

**Error Codes**:
- 400: Missing session_id or answer
- 404: Session not found
- 500: Processing failed

---

#### **POST /interview/followup**

**Purpose**: Generate follow-up question on last answer

**Request Body**:
```json
{
  "session_id": "abc-123-xyz",
  "should_followup": true
}
```

**Process**:
1. Get session
2. Get last answer from conversation_history
3. Generate contextual follow-up
4. Update session
5. Return follow-up question

**Response**:
```json
{
  "success": true,
  "data": {
    "followup_question": "Can you elaborate on the diffing algorithm?"
  }
}
```

**Use Case**: Probe deeper into candidate's answer

---

#### **POST /interview/end/:session_id**

**Purpose**: End interview and get final report

**URL Params**:
```
session_id: abc-123-xyz
```

**Process**:
1. Get session
2. Set end_time
3. Generate report (report_generator)
4. Return comprehensive report

**Response**:
```json
{
  "success": true,
  "data": {
    "message": "Interview ended successfully",
    "report": {
      "overall_score": 8.3,
      "technical_score": 8.5,
      "communication_score": 8.7,
      "confidence_score": 8.0,
      "strengths": [...],
      "weaknesses": [...],
      "topics_to_improve": [...],
      "missed_concepts": [...],
      "recommended_topics": [...],
      "recommended_leetcode_problems": [...],
      "recommended_resources": [...],
      "hiring_recommendation": "Hire",
      "detailed_feedback": "...",
      "session_id": "abc-123-xyz",
      "duration_minutes": 35,
      "questions_answered": 12
    }
  }
}
```

---

#### **GET /interview/session/:session_id**

**Purpose**: Get current session status

**URL Params**:
```
session_id: abc-123-xyz
```

**Response**:
```json
{
  "success": true,
  "data": {
    "session_id": "abc-123-xyz",
    "user_id": "507f...",
    "interview_type": "react",
    "stage": "technical_round",
    "difficulty": "intermediate",
    "questions_answered": 5,
    "overall_score": 8.2,
    "current_question": "Explain React hooks..."
  }
}
```

**Use Case**: Check interview progress

---

#### **POST /interview/advance-stage/:session_id**

**Purpose**: Manually move to next interview stage

**URL Params**:
```
session_id: abc-123-xyz
```

**Process**:
1. Advance stage (session_manager)
2. Generate question for new stage
3. Update session
4. Return new stage + question

**Response**:
```json
{
  "success": true,
  "data": {
    "stage": "technical_round",
    "question": "Let's discuss React concepts..."
  }
}
```

**Use Case**: Manual stage control (usually automatic)

---

### `routes/voice_api.py` - Voice Interview APIs

**Purpose**: Speech-to-speech interview endpoints

**Prefix**: `/voice`

---

#### **POST /voice/speech-to-text**

**Purpose**: Convert audio answer to text

**Request**:
```python
Content-Type: multipart/form-data
audio: answer.wav
```

**Process**:
1. Save uploaded audio
2. Use Whisper to transcribe
3. Return text
4. Cleanup temp file

**Response**:
```json
{
  "transcription": "React reconciliation is the process..."
}
```

**Requires**: `openai-whisper` installed

---

#### **POST /voice/text-to-speech**

**Purpose**: Convert question text to audio

**Request Body**:
```json
{
  "text": "What is React reconciliation?"
}
```

**Process**:
1. Use gTTS to generate audio
2. Save to temp file
3. Return file

**Response**: Audio file (MP3)
```
Content-Type: audio/mpeg
[Audio binary data]
```

**Requires**: `gtts` installed

---

#### **POST /voice/voice-answer/:session_id**

**Purpose**: Complete voice flow (audio in → audio out)

**Request**:
```python
Content-Type: multipart/form-data
audio: answer.wav
```

**Process**:
1. Speech to text (transcribe answer)
2. Evaluate answer
3. Generate next question
4. Text to speech (convert question)
5. Return everything

**Response**:
```json
{
  "transcription": "React uses...",
  "evaluation": {
    "overall_score": 8.5,
    "feedback": "..."
  },
  "next_question": "Can you explain...",
  "audio_url": "/voice/audio/question_xyz.mp3",
  "stage": "technical_round",
  "difficulty": "intermediate"
}
```

**Use Case**: Hands-free voice interview

---

#### **GET /voice/audio/:filename**

**Purpose**: Serve generated audio files

**URL Params**:
```
filename: question_xyz.mp3
```

**Response**: Audio file stream

---

### `routes/resume.py` - Legacy Resume Upload

**Note**: Superseded by `/interview/upload-resume`

**Endpoint**: `POST /upload-resume`

Simple resume upload without full analysis.

---

## 🔐 Authentication

All routes expect authentication to be handled by Node.js backend proxy.

Direct calls to AI service should include proper validation in production.

---

## 🚨 Error Handling

All endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Error message",
  "details": "Detailed error information"
}
```

**HTTP Status Codes**:
- 200: Success
- 400: Bad Request (validation error)
- 404: Not Found (session doesn't exist)
- 500: Internal Server Error

---

See DATASETS.md for information about question bank files.
