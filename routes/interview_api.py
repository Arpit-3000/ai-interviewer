from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from models.interview_session import InterviewType, DifficultyLevel, CodingProfile, QuestionAnswer
from services.session_manager import session_manager
from services.resume_analyzer import analyze_resume
from services.interview_conductor import InterviewConductor
from services.answer_evaluator import AnswerEvaluator
from services.difficulty_adapter import DifficultyAdapter
from services.report_generator import ReportGenerator
from services.resumeParser import parse_resume

router = APIRouter(prefix="/interview", tags=["Interview"])

# Request/Response Models
class StartInterviewRequest(BaseModel):
    user_id: str
    interview_type: InterviewType
    difficulty: DifficultyLevel
    coding_profile: Optional[CodingProfile] = None

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class FollowUpRequest(BaseModel):
    session_id: str
    should_followup: bool = False

# Upload Resume Endpoint
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload resume PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    path = f"uploads/{file.filename}"
    content = await file.read()
    
    with open(path, "wb") as f:
        f.write(content)
    
    # Analyze resume
    try:
        analysis = analyze_resume(path)
    except Exception as e:
        analysis = {"error": str(e)}
    
    return {
        "message": "Resume uploaded successfully",
        "path": path,
        "analysis": analysis
    }

# Start Interview
@router.post("/start")
def start_interview(request: StartInterviewRequest, resume_path: Optional[str] = None):
    """Start a new interview session"""
    try:
        # Create session
        session_id = session_manager.create_session(
            user_id=request.user_id,
            interview_type=request.interview_type,
            difficulty=request.difficulty,
            resume_path=resume_path,
            coding_profile=request.coding_profile
        )
        
        session = session_manager.get_session(session_id)
        
        # Analyze resume if provided
        if resume_path:
            try:
                session.resume_context = analyze_resume(resume_path)
            except Exception as e:
                print(f"Resume analysis error: {e}")
        
        # Generate introduction
        introduction = InterviewConductor.generate_introduction(session)
        session.current_question = introduction
        session.questions_asked.append(introduction)
        
        session_manager.update_session(session_id, session)
        
        return {
            "session_id": session_id,
            "message": "Interview started successfully",
            "question": introduction,
            "stage": session.stage.value,
            "difficulty": session.difficulty.value
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Submit Answer
@router.post("/answer")
def submit_answer(request: AnswerRequest):
    """Submit answer and get next question"""
    session = session_manager.get_session(request.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Extract candidate name from first answer (introduction)
        if len(session.conversation_history) == 0 and request.answer:
            candidate_name = InterviewConductor.extract_candidate_name(request.answer)
            if candidate_name:
                session.resume_context = session.resume_context or {}
                session.resume_context["candidate_name"] = candidate_name
        
        # Evaluate answer
        evaluation = AnswerEvaluator.evaluate_answer(
            question=session.current_question,
            answer=request.answer
        )
        
        # Store Q&A
        qa = QuestionAnswer(
            question=session.current_question,
            answer=request.answer,
            score=evaluation.get("overall_score", 5.0),
            feedback=evaluation.get("feedback", ""),
            timestamp=datetime.now()
        )
        session.conversation_history.append(qa)
        
        # Generate contextual response to answer
        response_to_answer = InterviewConductor.generate_response_to_answer(
            session, request.answer, evaluation
        )
        
        # Check if should adjust difficulty
        if DifficultyAdapter.should_adjust(session):
            new_difficulty = DifficultyAdapter.adjust_difficulty(session)
            if new_difficulty != session.difficulty:
                session.difficulty = new_difficulty
        
        # Generate next question
        next_question = InterviewConductor.generate_question(session)
        session.current_question = next_question
        session.questions_asked.append(next_question)
        
        # Update scores
        scores = AnswerEvaluator.calculate_session_scores(session.conversation_history)
        session.overall_score = scores["overall_score"]
        session.technical_score = scores["technical_score"]
        session.communication_score = scores["communication_score"]
        session.confidence_score = scores["confidence_score"]
        
        session_manager.update_session(request.session_id, session)
        
        return {
            "evaluation": evaluation,
            "response_to_answer": response_to_answer,
            "next_question": next_question,
            "stage": session.stage.value,
            "difficulty": session.difficulty.value,
            "overall_score": session.overall_score,
            "questions_answered": len(session.conversation_history)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate Follow-up Question
@router.post("/followup")
def generate_followup(request: FollowUpRequest):
    """Generate follow-up question based on last answer"""
    session = session_manager.get_session(request.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.conversation_history:
        raise HTTPException(status_code=400, detail="No previous answers to follow up on")
    
    try:
        last_answer = session.conversation_history[-1].answer
        followup = InterviewConductor.generate_followup(session, last_answer)
        
        session.current_question = followup
        session.questions_asked.append(followup)
        session_manager.update_session(request.session_id, session)
        
        return {
            "followup_question": followup
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# End Interview
@router.post("/end/{session_id}")
def end_interview(session_id: str):
    """End interview and generate report"""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session.end_time = datetime.now()
        
        # Generate final report
        report = ReportGenerator.generate_report(session)
        
        session_manager.update_session(session_id, session)
        
        return {
            "message": "Interview ended successfully",
            "report": report
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Session Status
@router.get("/session/{session_id}")
def get_session_status(session_id: str):
    """Get current session status"""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "user_id": session.user_id,
        "interview_type": session.interview_type.value,
        "stage": session.stage.value,
        "difficulty": session.difficulty.value,
        "questions_answered": len(session.conversation_history),
        "overall_score": session.overall_score,
        "current_question": session.current_question
    }

# Advance Stage
@router.post("/advance-stage/{session_id}")
def advance_stage(session_id: str):
    """Manually advance to next interview stage"""
    new_stage = session_manager.advance_stage(session_id)
    
    if not new_stage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = session_manager.get_session(session_id)
    
    # Generate question for new stage
    next_question = InterviewConductor.generate_question(session)
    session.current_question = next_question
    session.questions_asked.append(next_question)
    session_manager.update_session(session_id, session)
    
    return {
        "stage": new_stage.value,
        "question": next_question
    }
