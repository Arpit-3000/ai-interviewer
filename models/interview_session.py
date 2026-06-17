from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class InterviewType(str, Enum):
    HR = "hr"
    TECHNICAL = "technical"
    DSA = "dsa"
    REACT = "react"
    NODE = "node"
    CPP_JAVA = "cpp_java"
    DBMS = "dbms"
    OS = "os"
    CN = "cn"  # Computer Networks
    OOPS = "oops"
    SYSTEM_DESIGN = "system_design"
    COMPETITIVE = "competitive"
    MIXED = "mixed"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class InterviewStage(str, Enum):
    INTRODUCTION = "introduction"
    RESUME_DISCUSSION = "resume_discussion"
    TECHNICAL_ROUND = "technical_round"
    BEHAVIORAL_ROUND = "behavioral_round"
    CLOSING = "closing"

class CodingProfile(BaseModel):
    leetcode_rating: Optional[int] = None
    codeforces_rating: Optional[int] = None
    codechef_rating: Optional[int] = None
    strong_topics: List[str] = []
    weak_topics: List[str] = []
    total_problems_solved: int = 0
    contest_participation: int = 0

class QuestionAnswer(BaseModel):
    question: str
    answer: str
    score: float
    feedback: str
    timestamp: datetime

class InterviewSession(BaseModel):
    session_id: str
    user_id: str
    interview_type: InterviewType
    difficulty: DifficultyLevel
    stage: InterviewStage
    resume_path: Optional[str] = None
    resume_context: Dict = {}
    coding_profile: Optional[CodingProfile] = None
    conversation_history: List[QuestionAnswer] = []
    current_question: Optional[str] = None
    questions_asked: List[str] = []
    start_time: datetime
    end_time: Optional[datetime] = None
    overall_score: float = 0.0
    technical_score: float = 0.0
    communication_score: float = 0.0
    confidence_score: float = 0.0
