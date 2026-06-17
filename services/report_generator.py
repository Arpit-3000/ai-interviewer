from models.interview_session import InterviewSession
from services.llm import llm
from typing import Dict
import json

class ReportGenerator:
    """
    Generate comprehensive interview report
    """
    
    @staticmethod
    def generate_report(session: InterviewSession) -> Dict:
        """Generate final interview report"""
        
        # Compile all Q&A
        qa_summary = "\n\n".join([
            f"Q: {qa.question}\nA: {qa.answer[:200]}...\nScore: {qa.score}/10"
            for qa in session.conversation_history
        ])
        
        prompt = f"""Generate a comprehensive interview report.

Interview Type: {session.interview_type.value}
Total Questions: {len(session.conversation_history)}
Overall Score: {session.overall_score}/10

Interview Summary:
{qa_summary}

Generate a detailed report in JSON format:
{{
  "overall_score": X,
  "technical_score": X,
  "communication_score": X,
  "confidence_score": X,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "topics_to_improve": ["topic 1", "topic 2", "topic 3"],
  "missed_concepts": ["concept 1", "concept 2"],
  "recommended_topics": ["topic 1", "topic 2"],
  "recommended_leetcode_problems": ["problem 1", "problem 2"],
  "recommended_resources": ["resource 1", "resource 2"],
  "hiring_recommendation": "Strong Hire/Hire/Borderline/Needs Improvement",
  "detailed_feedback": "Comprehensive feedback paragraph"
}}

Return ONLY valid JSON."""
        
        response = llm.invoke(prompt)
        
        try:
            report = json.loads(response.content)
        except:
            # Fallback report
            report = {
                "overall_score": session.overall_score,
                "technical_score": session.technical_score,
                "communication_score": session.communication_score,
                "confidence_score": session.confidence_score,
                "strengths": ["Completed interview"],
                "weaknesses": ["Report generation issue"],
                "topics_to_improve": [],
                "missed_concepts": [],
                "recommended_topics": [],
                "recommended_leetcode_problems": [],
                "recommended_resources": [],
                "hiring_recommendation": "Needs Improvement",
                "detailed_feedback": "Interview completed but detailed report generation failed."
            }
        
        # Add session metadata
        report["session_id"] = session.session_id
        report["user_id"] = session.user_id
        report["interview_type"] = session.interview_type.value
        report["duration_minutes"] = (session.end_time - session.start_time).total_seconds() / 60 if session.end_time else 0
        report["questions_answered"] = len(session.conversation_history)
        
        return report
