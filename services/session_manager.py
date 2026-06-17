import uuid
from datetime import datetime
from typing import Dict, Optional
from models.interview_session import InterviewSession, InterviewType, DifficultyLevel, InterviewStage, CodingProfile

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
    
    def create_session(
        self,
        user_id: str,
        interview_type: InterviewType,
        difficulty: DifficultyLevel,
        resume_path: Optional[str] = None,
        coding_profile: Optional[CodingProfile] = None
    ) -> str:
        """Create a new interview session"""
        session_id = str(uuid.uuid4())
        
        session = InterviewSession(
            session_id=session_id,
            user_id=user_id,
            interview_type=interview_type,
            difficulty=difficulty,
            stage=InterviewStage.INTRODUCTION,
            resume_path=resume_path,
            coding_profile=coding_profile,
            start_time=datetime.now()
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Retrieve session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, session: InterviewSession):
        """Update session data"""
        self.sessions[session_id] = session
    
    def delete_session(self, session_id: str):
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def advance_stage(self, session_id: str) -> InterviewStage:
        """Move to next interview stage"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        stage_order = [
            InterviewStage.INTRODUCTION,
            InterviewStage.RESUME_DISCUSSION,
            InterviewStage.TECHNICAL_ROUND,
            InterviewStage.BEHAVIORAL_ROUND,
            InterviewStage.CLOSING
        ]
        
        current_idx = stage_order.index(session.stage)
        if current_idx < len(stage_order) - 1:
            session.stage = stage_order[current_idx + 1]
            self.update_session(session_id, session)
        
        return session.stage

# Global session manager instance
session_manager = SessionManager()
