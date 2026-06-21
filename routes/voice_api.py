from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from services.speech_service import speech_service
from services.session_manager import session_manager
from services.interview_conductor import InterviewConductor
from services.answer_evaluator import AnswerEvaluator
from datetime import datetime
from models.interview_session import QuestionAnswer

router = APIRouter(prefix="/voice", tags=["Voice Interview"])

class TextToSpeechRequest(BaseModel):
    text: str

@router.post("/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """Convert audio answer to text"""
    try:
        # Save uploaded audio
        temp_path = f"uploads/audio_{audio.filename}"
        content = await audio.read()
        
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Convert to text
        transcription = speech_service.speech_to_text(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        return {
            "transcription": transcription
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-to-speech")
def text_to_speech(request: TextToSpeechRequest):
    """Convert question text to speech"""
    try:
        output_path = speech_service.text_to_speech(request.text)
        
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename="question.mp3"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice-answer/{session_id}")
async def submit_voice_answer(session_id: str, audio: UploadFile = File(...)):
    """
    Complete voice interview flow:
    1. Convert audio to text
    2. Evaluate answer
    3. Generate contextual response
    4. Generate next question
    5. Convert to speech
    6. Return both text and audio
    """
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Save audio
        temp_audio_path = f"uploads/audio_{session_id}_{len(session.conversation_history)}.wav"
        content = await audio.read()
        
        with open(temp_audio_path, "wb") as f:
            f.write(content)
        
        # Speech to text
        answer_text = speech_service.speech_to_text(temp_audio_path)
        
        # Extract candidate name from first answer
        if len(session.conversation_history) == 0 and answer_text:
            candidate_name = InterviewConductor.extract_candidate_name(answer_text)
            if candidate_name:
                session.resume_context = session.resume_context or {}
                session.resume_context["candidate_name"] = candidate_name
        
        # Evaluate answer
        evaluation = AnswerEvaluator.evaluate_answer(
            question=session.current_question,
            answer=answer_text
        )
        
        # Store Q&A
        qa = QuestionAnswer(
            question=session.current_question,
            answer=answer_text,
            score=evaluation.get("overall_score", 5.0),
            feedback=evaluation.get("feedback", ""),
            timestamp=datetime.now()
        )
        session.conversation_history.append(qa)
        
        # Generate contextual response
        response_to_answer = InterviewConductor.generate_response_to_answer(
            session, answer_text, evaluation
        )
        
        # Generate next question
        next_question = InterviewConductor.generate_question(session)
        session.current_question = next_question
        session.questions_asked.append(next_question)
        
        # Update session
        session_manager.update_session(session_id, session)
        
        # Combine response and next question for speech
        full_response = f"{response_to_answer} {next_question}"
        
        # Convert to speech
        question_audio_path = speech_service.text_to_speech(full_response)
        
        # Cleanup input audio
        os.remove(temp_audio_path)
        
        return {
            "transcription": answer_text,
            "evaluation": evaluation,
            "response_to_answer": response_to_answer,
            "next_question": next_question,
            "audio_url": f"/voice/audio/{os.path.basename(question_audio_path)}",
            "stage": session.stage.value,
            "difficulty": session.difficulty.value
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audio/{filename}")
def get_audio_file(filename: str):
    """Serve generated audio files"""
    file_path = f"/tmp/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )

@router.post("/stop-speech/{session_id}")
def stop_speech(session_id: str):
    """Stop AI speech when interview ends or user interrupts"""
    session = session_manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Signal to stop any ongoing speech
        # This will be handled on frontend by stopping audio playback
        return {
            "message": "Speech stopped",
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
