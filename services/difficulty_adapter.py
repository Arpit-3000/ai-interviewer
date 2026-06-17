from models.interview_session import DifficultyLevel, InterviewSession

class DifficultyAdapter:
    """
    Dynamically adjust interview difficulty based on performance
    """
    
    @staticmethod
    def should_adjust(session: InterviewSession) -> bool:
        """Check if difficulty should be adjusted"""
        if len(session.conversation_history) < 3:
            return False
        
        # Check last 3 answers
        recent_scores = [qa.score for qa in session.conversation_history[-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        return avg_score > 8.5 or avg_score < 4.0
    
    @staticmethod
    def adjust_difficulty(session: InterviewSession) -> DifficultyLevel:
        """Adjust difficulty based on recent performance"""
        if len(session.conversation_history) < 3:
            return session.difficulty
        
        recent_scores = [qa.score for qa in session.conversation_history[-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        current_diff = session.difficulty
        
        # Increase difficulty if performing well
        if avg_score > 8.5:
            if current_diff == DifficultyLevel.BEGINNER:
                return DifficultyLevel.INTERMEDIATE
            elif current_diff == DifficultyLevel.INTERMEDIATE:
                return DifficultyLevel.ADVANCED
        
        # Decrease difficulty if struggling
        elif avg_score < 4.0:
            if current_diff == DifficultyLevel.ADVANCED:
                return DifficultyLevel.INTERMEDIATE
            elif current_diff == DifficultyLevel.INTERMEDIATE:
                return DifficultyLevel.BEGINNER
        
        return current_diff
    
    @staticmethod
    def get_difficulty_context(difficulty: DifficultyLevel) -> str:
        """Get prompt context for difficulty level"""
        contexts = {
            DifficultyLevel.BEGINNER: "Ask basic conceptual questions. Focus on fundamentals.",
            DifficultyLevel.INTERMEDIATE: "Ask moderate questions requiring good understanding and some problem-solving.",
            DifficultyLevel.ADVANCED: "Ask advanced questions involving deep concepts, edge cases, and optimization."
        }
        return contexts.get(difficulty, "")
