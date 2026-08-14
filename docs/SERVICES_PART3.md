# Services Documentation (Part 3)

## 🔧 services/ - Business Logic (Continued)

### `services/report_generator.py` - Final Interview Report

**Purpose**: Generate comprehensive report at interview end

**Class**: `ReportGenerator`

**Method**: `generate_report(session)`

```python
@staticmethod
def generate_report(session: InterviewSession) -> Dict:
    """
    Create detailed interview assessment
    
    Process:
    1. Compile all Q&A from session
    2. Build summary of performance
    3. Send to LLM for analysis
    4. LLM generates structured report
    5. Add metadata
    
    Returns: Complete report dict
    """
```

**Report Structure**:
```python
{
  # Scores
  "overall_score": 8.3,
  "technical_score": 8.5,
  "communication_score": 8.7,
  "confidence_score": 8.0,
  
  # Analysis
  "strengths": [
    "Strong React fundamentals",
    "Clear communication",
    "Good project experience"
  ],
  "weaknesses": [
    "Limited performance optimization knowledge",
    "Could improve testing practices"
  ],
  "topics_to_improve": [
    "React Performance",
    "Advanced Hooks",
    "Testing"
  ],
  "missed_concepts": [
    "React.memo",
    "Code splitting"
  ],
  
  # Recommendations
  "recommended_topics": [...],
  "recommended_leetcode_problems": [...],
  "recommended_resources": [...],
  
  # Decision
  "hiring_recommendation": "Hire",
  "detailed_feedback": "Comprehensive paragraph..."
  
  # Metadata
  "session_id": "...",
  "duration_minutes": 35,
  "questions_answered": 12
}
```

**LLM Prompt Structure**:
```python
"""
Analyze this interview:

Type: React Interview
Total Questions: 12
Overall Score: 8.3/10

Q&A Summary:
Q1: Introduce yourself (8.4/10)
Q2: Explain CodeOrbit (9.0/10)
Q3: React reconciliation (7.5/10)
...

Generate comprehensive report with:
- Strengths
- Weaknesses
- Topics to improve
- Hiring recommendation

Return JSON.
"""
```

**When called**: User clicks "End Interview"

**Fallback**: If LLM fails, returns basic report with scores

---

### `services/resume_analyzer.py` - Resume Parsing

**Purpose**: Extract structured data from PDF resume

**Function**: `analyze_resume(resume_path)`

```python
def analyze_resume(resume_path: str) -> Dict:
    """
    Parse and analyze resume
    
    Steps:
    1. Load PDF using PyPDF (resumeParser)
    2. Extract text from all pages
    3. Send to LLM for structured extraction
    4. Return parsed data
    """
```

**LLM Extraction Prompt**:
```python
"""
Extract from this resume:

[Resume Text]

Return JSON:
{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["React", "Node.js", ...],
  "projects": [
    {"name": "...", "description": "..."}
  ],
  "experience": [
    {"company": "...", "role": "...", "duration": "..."}
  ],
  "education": [...],
  "years_of_experience": 2,
  "primary_domain": "Full Stack"
}
"""
```

**Output Example**:
```python
{
  "name": "Arpit Srivastava",
  "email": "arpit@example.com",
  "skills": ["React", "Node.js", "MongoDB", "Python"],
  "projects": [
    {
      "name": "CodeOrbit",
      "description": "Social platform for competitive programmers"
    }
  ],
  "experience": [...],
  "years_of_experience": 2,
  "primary_domain": "Full Stack"
}
```

**When called**: After resume upload, before interview start

**Error Handling**: Returns basic structure if parsing fails

---

### `services/resumeParser.py` - PDF Reader

**Purpose**: Low-level PDF text extraction

**Function**: `parse_resume(path)`

```python
def parse_resume(path):
    """
    Read PDF and extract text
    
    Uses: PyPDFLoader from langchain
    Returns: List of Document objects with page_content
    """
    loader = PyPDFLoader(path)
    docs = loader.load()
    return docs
```

**Usage**:
```python
docs = parse_resume("uploads/resume.pdf")
text = "\n".join([doc.page_content for doc in docs])
```

---

### `services/question_bank_loader.py` - RAG System

**Purpose**: Load and retrieve questions from domain datasets

**Class**: `QuestionBankLoader`

**Dataset Mapping**:
```python
DATASET_MAPPING = {
    "dsa": "datasets/dsa.txt",
    "react": "datasets/react.txt",
    "node": "datasets/node.txt",
    "cpp_java": "datasets/c_cpp_java.txt",
    "dbms": "datasets/dbms.txt",
    "os": "datasets/os.txt",
    "cn": "datasets/cn.txt",
    "oops": "datasets/oops.txt",
    "system_design": "datasets/system_design.txt"
}
```

**Methods**:

#### 1. `load_dataset(domain)`
```python
def load_dataset(domain: str) -> Chroma:
    """
    Load questions into vector database
    
    Process:
    1. Check if already loaded (cache)
    2. Read dataset file (TextLoader)
    3. Create embeddings
    4. Store in ChromaDB
    5. Return vector store
    """
```

#### 2. `get_questions(domain, difficulty, k=5)`
```python
def get_questions(domain, difficulty=None, k=5) -> List[Dict]:
    """
    Retrieve relevant questions
    
    Args:
        domain: "react", "dsa", etc.
        difficulty: "beginner", "intermediate", "advanced"
        k: Number of questions
    
    Returns: List of question dicts
    """
```

**Example Usage**:
```python
loader = question_bank_loader
questions = loader.get_questions("react", "intermediate", k=3)

# Returns:
[
  {
    "domain": "React",
    "difficulty": "Medium",
    "question": "Explain React reconciliation",
    "expected_points": ["Virtual DOM", "Diffing", "Keys"]
  },
  {
    "domain": "React",
    "difficulty": "Medium",
    "question": "What are React hooks?",
    "expected_points": ["useState", "useEffect", "Rules"]
  },
  ...
]
```

#### 3. `get_random_question(domain, difficulty)`
```python
def get_random_question(domain, difficulty=None) -> Dict:
    """Get single random question"""
```

#### 4. `get_multi_domain_questions(domains, difficulty, k_per_domain)`
```python
def get_multi_domain_questions(domains, ...) -> List[Dict]:
    """
    Get questions from multiple domains
    
    For "mixed" interview type
    """
```

**Vector Search**:
- Uses semantic search (embeddings)
- Finds similar/relevant questions
- Filters by difficulty if specified

**Global Instance**:
```python
question_bank_loader = QuestionBankLoader()
```

---

### `services/speech_service.py` - Voice Support

**Purpose**: Speech-to-text and text-to-speech for voice interviews

**Class**: `SpeechService`

**Dependencies** (Optional):
- `openai-whisper` - Speech to text
- `gtts` - Text to speech

**Methods**:

#### 1. `speech_to_text(audio_file_path)`
```python
def speech_to_text(audio_file_path: str) -> str:
    """
    Convert audio to text using Whisper
    
    Args: Path to audio file (wav, mp3, etc.)
    Returns: Transcribed text
    """
```

**Example**:
```python
text = speech_service.speech_to_text("uploads/answer.wav")
# Returns: "React reconciliation is the process..."
```

#### 2. `text_to_speech(text, output_path)`
```python
def text_to_speech(text: str, output_path=None) -> str:
    """
    Convert text to speech using gTTS
    
    Args: Text to convert
    Returns: Path to generated audio file
    """
```

**Example**:
```python
audio_path = speech_service.text_to_speech(
    "What is React reconciliation?"
)
# Returns: "/tmp/audio_xyz.mp3"
```

**Initialization**:
```python
def __init__(self):
    try:
        import whisper
        self.whisper_model = whisper.load_model("base")
        self.stt_enabled = True
    except:
        self.stt_enabled = False
    
    try:
        from gtts import gTTS
        self.tts_engine = gTTS
        self.tts_enabled = True
    except:
        self.tts_enabled = False
```

**Global Instance**:
```python
speech_service = SpeechService()
```

**Note**: Voice features are optional. If not installed, raises helpful error.

---

Continue reading ROUTES.md for API endpoint documentation...
