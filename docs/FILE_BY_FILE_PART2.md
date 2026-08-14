# File-by-File Documentation (Part 2)

## 🔧 services/ - Business Logic (Continued)

### `services/interview_conductor.py` - Question Generation Brain

**Purpose**: Core AI interviewer logic - generates contextual questions

**Class**: `InterviewConductor`

**Methods**:

#### 1. `generate_introduction(session)`
```python
@staticmethod
def generate_introduction(session: InterviewSession) -> str:
    """
    Creates personalized welcome message
    
    Uses:
    - Candidate name from resume
    - Interview type
    
    Returns: 
    "Hello [Name], I will be conducting your [type] interview..."
    """
```

**When called**: First question of interview

#### 2. `generate_question(session)` ⭐ MOST IMPORTANT
```python
@staticmethod
def generate_question(session: InterviewSession) -> str:
    """
    Generate next interview question based on full context
    
    Process:
    1. Build context from:
       - Resume (skills, projects)
       - Coding profile (ratings, topics)
       - Previous Q&A
       - Current stage & difficulty
    
    2. Get sample questions from question bank (RAG)
       question_bank_loader.get_questions(domain, difficulty, k=3)
    
    3. Create comprehensive prompt for LLM
    
    4. LLM generates natural, conversational question
    
    5. Return question
    """
```

**Example Flow**:
```python
# Session context:
- Type: "react"
- Stage: "technical_round"
- Difficulty: "intermediate"
- Resume: Skills include React, built CodeOrbit
- Previous: Asked about intro, CodeOrbit architecture

# Loads from question bank:
datasets/react.txt → Sample questions:
- "Explain React reconciliation"
- "What are React hooks?"

# Builds prompt:
"""
You are conducting a React interview.
Candidate has React experience, built CodeOrbit.
Current stage: Technical Round
Difficulty: Intermediate

Sample questions from bank:
- Explain React reconciliation
- What are React hooks?

Previous questions:
- Introduce yourself
- Explain CodeOrbit architecture

Ask ONE new technical React question.
Reference their CodeOrbit project if relevant.
"""

# LLM generates:
"In your CodeOrbit project, you likely handled real-time
updates. Can you explain how React's reconciliation algorithm
optimizes re-renders in such scenarios?"
```

**Key Features**:
- Context-aware (uses all available data)
- Non-repetitive (tracks previous questions)
- Natural & conversational
- Domain-specific (uses question bank)
- Adaptive to difficulty

#### 3. `generate_followup(session, last_answer)`
```python
@staticmethod
def generate_followup(session, last_answer: str) -> str:
    """
    Generate follow-up question based on previous answer
    
    Purpose: Probe deeper, like real interviewer
    
    Example:
    Original Q: "What is React reconciliation?"
    Answer: "It's when React updates the DOM..."
    
    Follow-up: "Can you explain the diffing algorithm
                used in reconciliation?"
    """
```

**When called**: User requests follow-up or AI decides to probe

#### 4. `_get_stage_instructions(stage, type)`
```python
@staticmethod
def _get_stage_instructions(stage, type) -> str:
    """
    Get prompt instructions for each stage
    
    Returns stage-specific guidance:
    - Introduction: "Ask candidate to introduce themselves"
    - Resume: "Ask about projects and experiences"
    - Technical: "Ask domain questions, test understanding"
    - Behavioral: "Ask about teamwork, challenges"
    - Closing: "Ask if they have questions, wrap up"
    """
```

#### 5. `_get_domain_from_interview_type(type)`
```python
@staticmethod
def _get_domain_from_interview_type(type) -> str:
    """
    Map interview type to dataset domain
    
    react → "react"
    dsa → "dsa"
    node → "node"
    etc.
    
    Used to load correct question bank
    """
```

**Dependencies**:
- `llm.py` - For generation
- `question_bank_loader.py` - For RAG
- `difficulty_adapter.py` - For difficulty context
- `models/interview_session.py` - For data structures

---

### `services/answer_evaluator.py` - Answer Scoring

**Purpose**: Evaluate and score user answers

**Class**: `AnswerEvaluator`

**Methods**:

#### 1. `evaluate_answer(question, answer, expected_context)`
```python
@staticmethod
def evaluate_answer(question: str, answer: str, 
                   expected_context: str = "") -> Dict:
    """
    Comprehensive answer evaluation
    
    Prompt to LLM:
    "You are an expert interviewer evaluating a candidate.
    
    Question: [question]
    Answer: [answer]
    Expected Points: [expected_context]
    
    Evaluate on:
    1. Technical Accuracy (0-10)
    2. Depth (0-10)
    3. Clarity (0-10)
    4. Completeness (0-10)
    5. Communication (0-10)
    
    Return JSON:
    {
      'technical_accuracy': X,
      'depth': X,
      'clarity': X,
      'completeness': X,
      'communication': X,
      'overall_score': X,
      'strengths': ['point1', 'point2'],
      'weaknesses': ['point1', 'point2'],
      'feedback': 'Brief feedback',
      'confidence_level': 'high/medium/low'
    }
    "
    
    Returns: Structured evaluation dict
    """
```

**Example**:
```python
question = "What is React reconciliation?"
answer = "Reconciliation is how React updates the DOM efficiently 
         by comparing virtual DOM trees and only updating what changed."

evaluation = evaluate_answer(question, answer)

# Returns:
{
  "technical_accuracy": 9.0,
  "depth": 7.5,
  "clarity": 8.5,
  "completeness": 7.0,
  "communication": 8.0,
  "overall_score": 8.0,
  "strengths": [
    "Correct understanding of core concept",
    "Mentioned virtual DOM and diffing"
  ],
  "weaknesses": [
    "Could elaborate on the diffing algorithm",
    "Missing mention of keys"
  ],
  "feedback": "Good grasp of fundamentals. Consider studying 
               the reconciliation algorithm in more depth.",
  "confidence_level": "high"
}
```

#### 2. `calculate_session_scores(conversation_history)`
```python
@staticmethod
def calculate_session_scores(conversation_history) -> Dict[str, float]:
    """
    Aggregate scores for entire session
    
    Calculates:
    - overall_score: Average of all question scores
    - technical_score: Weighted by technical accuracy
    - communication_score: Weighted by clarity & communication
    - confidence_score: Derived metric
    
    Returns:
    {
      "overall_score": 8.3,
      "technical_score": 8.5,
      "communication_score": 8.7,
      "confidence_score": 8.0
    }
    """
```

**When called**: After each answer (for session update)

**Error Handling**: Falls back to default scores if LLM fails

---

### `services/difficulty_adapter.py` - Dynamic Difficulty

**Purpose**: Automatically adjust interview difficulty based on performance

**Class**: `DifficultyAdapter`

**Methods**:

#### 1. `should_adjust(session)`
```python
@staticmethod
def should_adjust(session: InterviewSession) -> bool:
    """
    Determine if difficulty should change
    
    Logic:
    - Need at least 3 answers
    - Calculate average of last 3 scores
    - If avg > 8.5 or avg < 4.0 → adjust
    
    Returns: True if adjustment needed
    """
```

#### 2. `adjust_difficulty(session)`
```python
@staticmethod
def adjust_difficulty(session) -> DifficultyLevel:
    """
    Calculate new difficulty level
    
    Rules:
    If avg score > 8.5:
        beginner → intermediate
        intermediate → advanced
        (advanced stays advanced)
    
    If avg score < 4.0:
        advanced → intermediate
        intermediate → beginner
        (beginner stays beginner)
    
    Returns: New difficulty level
    """
```

**Example**:
```python
# Current: intermediate
# Last 3 scores: [9.2, 9.0, 8.8] → avg = 9.0

# Result: difficulty → advanced
# Next questions will be harder!
```

#### 3. `get_difficulty_context(difficulty)`
```python
@staticmethod
def get_difficulty_context(difficulty) -> str:
    """
    Get prompt instructions for difficulty level
    
    beginner: "Ask basic conceptual questions. Focus on fundamentals."
    intermediate: "Ask moderate questions requiring understanding."
    advanced: "Ask advanced questions with edge cases & optimization."
    
    Used in question generation prompt
    """
```

**When called**: 
- `should_adjust()` - After each answer
- `adjust_difficulty()` - If should_adjust returns True
- `get_difficulty_context()` - During question generation

**Impact**: Makes interview adaptive and fair

---

Continue reading FILE_BY_FILE_PART3.md...
