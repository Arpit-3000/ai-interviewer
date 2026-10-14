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

Be a strict, calibrated grader. Score only what the candidate actually said, not what they might know:
- 0-2: no answer, "I don't know", off-topic, or wrong
- 3-4: mostly wrong or very shallow
- 5-6: partly correct, missing important points
- 7-8: correct and reasonably complete
- 9-10: excellent, precise, covers edge cases or trade-offs
Short or vague answers cannot score above 5. Confidence is "low" when the candidate hedges or says they do not know, "high" only when they answer directly and decisively. If the question was a simple introduction, judge clarity and relevance.

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
        
        evaluation = None
        try:
            match = re.search(r'\{.*\}', response.content.strip(), re.DOTALL)
            evaluation = json.loads(match.group()) if match else None
        except Exception:
            evaluation = None

        dims = ("technical_accuracy", "depth", "clarity", "completeness", "communication")
        try:
            clean = {k: max(0.0, min(10.0, float(evaluation[k]))) for k in dims}
        except Exception:
            # Unreadable reply: say so, and keep this answer out of the averages instead of inventing a 5/10
            return {
                **{k: 0.0 for k in dims},
                "overall_score": 0.0,
                "strengths": [],
                "weaknesses": [],
                "feedback": "This answer couldn't be scored automatically, so it isn't counted in your results.",
                "confidence_level": "medium",
                "evaluated": False,
            }

        # The overall score is computed here (not taken from the model) so it always matches the dimensions
        overall = (
            0.35 * clean["technical_accuracy"] + 0.20 * clean["depth"] + 0.20 * clean["completeness"]
            + 0.15 * clean["clarity"] + 0.10 * clean["communication"]
        )
        level = str(evaluation.get("confidence_level", "medium")).lower()
        return {
            **clean,
            "overall_score": round(overall, 1),
            "strengths": [str(x) for x in (evaluation.get("strengths") or [])][:3],
            "weaknesses": [str(x) for x in (evaluation.get("weaknesses") or [])][:3],
            "feedback": str(evaluation.get("feedback", "")),
            "confidence_level": level if level in ("high", "medium", "low") else "medium",
            "evaluated": True,
        }
    
    @staticmethod
    def calculate_session_scores(conversation_history) -> Dict[str, float]:
        """Aggregate the real per-answer scores. Answers that couldn't be scored are ignored."""
        scored = [qa for qa in conversation_history if qa.evaluated]
        if not scored:
            return {"overall_score": 0.0, "technical_score": 0.0, "communication_score": 0.0, "confidence_score": 0.0}

        mean = lambda xs: round(sum(xs) / len(xs), 2) if xs else 0.0

        # Technical: how correct, deep and complete the answers were, from the technical questions
        # (the introduction and closing say little about technical ability)
        tech = [qa for qa in scored if qa.stage not in ("introduction", "closing")] or scored
        technical = mean([(qa.dims.get("technical_accuracy", 0) + qa.dims.get("depth", 0) + qa.dims.get("completeness", 0)) / 3 for qa in tech])
        communication = mean([(qa.dims.get("clarity", 0) + qa.dims.get("communication", 0)) / 2 for qa in scored])
        # Confidence is judged from how the answers read (we only get a transcript, not tone of voice)
        level_score = {"high": 9.0, "medium": 6.0, "low": 3.0}
        confidence = mean([level_score.get(qa.confidence_level, 6.0) for qa in scored])

        return {
            "overall_score": mean([qa.score for qa in scored]),
            "technical_score": technical,
            "communication_score": communication,
            "confidence_score": confidence,
        }
