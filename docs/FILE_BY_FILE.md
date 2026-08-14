# Complete File-by-File Documentation

## 📄 Root Level Files

### `app.py` - Main Application Entry Point

**Purpose**: FastAPI application initialization and configuration

**What it does**:
- Creates FastAPI app instance
- Configures CORS middleware (allows frontend connections)
- Registers all API routes (interview, voice)
- Defines health check endpoint

**Key Code**:
```python
app = FastAPI(title="CodeOrbit AI Interview Service")

# Allow cross-origin requests from frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Mount routes
app.include_router(interview_router)  # /interview/*
app.include_router(voice_router)      # /voice/*

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**When it runs**: On server startup (`uvicorn app:app`)

---

### `requirements.txt` - Python Dependencies

**Purpose**: Lists all required Python packages

**Key Dependencies**:
```
fastapi==0.109.0          # Web framework
uvicorn[standard]         # ASGI server
pydantic==2.5.0          # Data validation
langchain==0.1.0         # LLM framework
langchain-groq           # Groq integration
chromadb==0.4.22         # Vector database
sentence-transformers    # Text embeddings
pypdf==4.0.1            # PDF parsing
python-dotenv           # Environment vars
python-multipart        # File uploads
```

**Usage**: `pip install -r requirements.txt`

---

### `.env` - Environment Variables

**Purpose**: Stores sensitive configuration

**Content**:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Security**: Never commit to git (in .gitignore)

---

### `test_api.py` - API Testing Script

**Purpose**: Test all endpoints without frontend

**What it does**:
1. Tests health check
2. Starts interview → gets session_id
3. Submits answers
4. Checks session status
5. Ends interview → gets report

**Usage**:
```bash
python test_api.py
```

**Output**: Shows API responses for debugging

---

## 📦 models/ - Data Models

### `models/interview_session.py` - Core Data Structures

**Purpose**: Define all data types used across the system

**Contains**:

#### 1. **InterviewType** (Enum)
```python
class InterviewType(str, Enum):
    HR = "hr"
    DSA = "dsa"
    REACT = "react"
    NODE = "node"
    CPP_JAVA = "cpp_java"
    DBMS = "dbms"
    OS = "os"
    CN = "cn"
    OOPS = "oops"
    SYSTEM_DESIGN = "system_design"
    COMPETITIVE = "competitive"
    MIXED = "mixed"
```
**Usage**: Specifies what kind of interview

#### 2. **DifficultyLevel** (Enum)
```python
class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
```
**Usage**: Current difficulty (can change dynamically)

#### 3. **InterviewStage** (Enum)
```python
class InterviewStage(str, Enum):
    INTRODUCTION = "introduction"
    RESUME_DISCUSSION = "resume_discussion"
    TECHNICAL_ROUND = "technical_round"
    BEHAVIORAL_ROUND = "behavioral_round"
    CLOSING = "closing"
```
**Usage**: Tracks current phase of interview

#### 4. **CodingProfile** (Model)
```python
class CodingProfile(BaseModel):
    leetcode_rating: Optional[int] = None
    codeforces_rating: Optional[int] = None
    codechef_rating: Optional[int] = None
    strong_topics: List[str] = []
    weak_topics: List[str] = []
    total_problems_solved: int = 0
    contest_participation: int = 0
```
**Usage**: Stores user's competitive programming stats
**Source**: Comes from CodeOrbit backend (LeetCode/CF/CC data)

#### 5. **QuestionAnswer** (Model)
```python
class QuestionAnswer(BaseModel):
    question: str          # Question asked
    answer: str           # User's answer
    score: float          # Score 0-10
    feedback: str         # AI feedback
    timestamp: datetime   # When answered
```
**Usage**: Single Q&A record in conversation history

#### 6. **InterviewSession** (Model)
```python
class InterviewSession(BaseModel):
    session_id: str                          # UUID
    user_id: str                            # From CodeOrbit
    interview_type: InterviewType           # e.g., "react"
    difficulty: DifficultyLevel             # Current level
    stage: InterviewStage                   # Current stage
    resume_path: Optional[str] = None       # PDF path
    resume_context: Dict = {}               # Parsed data
    coding_profile: Optional[CodingProfile] # Stats
    conversation_history: List[QuestionAnswer] = []  # All Q&A
    current_question: Optional[str] = None  # Active question
    questions_asked: List[str] = []         # All questions
    start_time: datetime                    # Interview start
    end_time: Optional[datetime] = None     # Interview end
    overall_score: float = 0.0              # Aggregate score
    technical_score: float = 0.0
    communication_score: float = 0.0
    confidence_score: float = 0.0
```
**Usage**: Complete state of an interview session
**Lifecycle**: Created → Updated per answer → Final report

---

## 🔧 services/ - Business Logic

### `services/llm.py` - Groq LLM Client

**Purpose**: Initialize and configure the language model

**What it does**:
```python
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv('GROQ_API_KEY')
)
```

**Usage**: Imported everywhere that needs LLM
```python
response = llm.invoke("Your prompt here")
```

**Model**: Llama 3.1 8B (fast, cost-effective)

---

### `services/embeddings.py` - Text Embeddings

**Purpose**: Convert text to vector embeddings for semantic search

**What it does**:
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

**Usage**: 
- Question bank search (find similar questions)
- Vector database operations
- Semantic matching

**How it works**:
```python
text = "What is React reconciliation?"
vector = embedding_model.embed_query(text)
# Returns: [0.123, -0.456, 0.789, ...]  (384 dimensions)
```

---

### `services/session_manager.py` - Session Lifecycle

**Purpose**: Manage interview sessions (CRUD operations)

**Class**: `SessionManager`

**Methods**:

#### 1. `create_session()`
```python
def create_session(user_id, interview_type, difficulty, 
                   resume_path=None, coding_profile=None) -> str:
    """
    Creates new interview session
    
    Returns: session_id (UUID)
    """
    session_id = str(uuid.uuid4())  # Generate unique ID
    session = InterviewSession(...)  # Create session object
    self.sessions[session_id] = session  # Store in memory
    return session_id
```

**When called**: User clicks "Start Interview"

#### 2. `get_session(session_id)`
```python
def get_session(session_id: str) -> InterviewSession:
    """Retrieve existing session"""
    return self.sessions.get(session_id)
```

**When called**: Every API request with session_id

#### 3. `update_session(session_id, session)`
```python
def update_session(session_id, session):
    """Save session changes"""
    self.sessions[session_id] = session
```

**When called**: After every answer, difficulty change, stage change

#### 4. `delete_session(session_id)`
```python
def delete_session(session_id):
    """Remove session"""
    del self.sessions[session_id]
```

**When called**: Interview complete (optional cleanup)

#### 5. `advance_stage(session_id)`
```python
def advance_stage(session_id) -> InterviewStage:
    """
    Move to next stage:
    Introduction → Resume → Technical → Behavioral → Closing
    """
```

**When called**: Manually or after N questions per stage

**Storage**: Currently in-memory dictionary
**Production**: Should use MongoDB/Redis

**Global Instance**:
```python
session_manager = SessionManager()  # Singleton
```

---

Continue reading FILE_BY_FILE_PART2.md for services documentation...
