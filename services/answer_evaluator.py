from services.llm import llm
from typing import Dict
import json
import re

class AnswerEvaluator:
    """
    Comprehensive answer evaluation system
    """
    
    @staticmethod
    def evaluate_answer(question: str, answer: str, expected_context: str = "") -> Dict:
        """
        Evaluate answer on multiple dimensions
        Returns scores and feedback
        """
        
        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer.

Question: {question}

Candidate's Answer: {answer}

{f"Expected Key Points: {expected_context}" if expected_context else ""}

Evaluate the answer on these dimensions (score 0-10 for each):

1. Technical Accuracy: Correctness of the answer
2. Depth: How deep is the understanding
3. Clarity: How clearly they explained
4. Completeness: Did they cover key points
5. Communication: Structure and articulation

Provide scores in JSON format:
{{
  "technical_accuracy": X,
  "depth": X,
  "clarity": X,
  "completeness": X,
  "communication": X,
  "overall_score": X,
  "strengths": ["point 1", "point 2"],
  "weaknesses": ["point 1", "point 2"],
  "feedback": "Brief constructive feedback",
  "confidence_level": "high/medium/low"
}}

Return ONLY valid JSON."""
        
        response = llm.invoke(prompt)
        
        try:
            # Extract JSON from response
            content = response.content.strip()
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                evaluation = json.loads(json_match.group())
            else:
                evaluation = json.loads(content)
        except Exception as e:
            # Fallback evaluation
            evaluation = {
                "technical_accuracy": 5.0,
                "depth": 5.0,
                "clarity": 5.0,
                "completeness": 5.0,
                "communication": 5.0,
                "overall_score": 5.0,
                "strengths": ["Response provided"],
                "weaknesses": ["Could not parse detailed evaluation"],
                "feedback": "Answer received but detailed evaluation unavailable.",
                "confidence_level": "medium"
            }
        
        return evaluation
    
    @staticmethod
    def calculate_session_scores(conversation_history) -> Dict[str, float]:
        """Calculate aggregate scores for the entire session"""
        if not conversation_history:
            return {
                "overall_score": 0.0,
                "technical_score": 0.0,
                "communication_score": 0.0,
                "confidence_score": 0.0
            }
        
        scores = [qa.score for qa in conversation_history]
        
        return {
            "overall_score": round(sum(scores) / len(scores), 2),
            "technical_score": round(sum(scores) / len(scores), 2),  # Can be calculated separately
            "communication_score": round(sum(scores) / len(scores) * 0.9, 2),  # Weighted
            "confidence_score": round(sum(scores) / len(scores) * 0.95, 2)  # Weighted
        }
