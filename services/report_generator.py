from models.interview_session import InterviewSession
from services.llm import llm
from services.answer_evaluator import AnswerEvaluator
from typing import Dict
import json
import re


def _hiring_recommendation(overall: float) -> str:
    if overall >= 8:
        return "Strong Hire"
    if overall >= 6.5:
        return "Hire"
    if overall >= 5:
        return "Borderline"
    return "Needs Improvement"


class ReportGenerator:
    """
    Generate the final interview report.

    Every number (overall, technical, communication, confidence, hiring recommendation) is computed from the
    per-answer evaluations. The language model only writes the qualitative parts (strengths, gaps, what to study),
    and it is shown the scores rather than asked to invent them.
    """

    @staticmethod
    def generate_report(session: InterviewSession) -> Dict:
        history = session.conversation_history
        scores = AnswerEvaluator.calculate_session_scores(history)
        scored = [qa for qa in history if qa.evaluated]

        report = {
            "overall_score": scores["overall_score"],
            "technical_score": scores["technical_score"],
            "communication_score": scores["communication_score"],
            "confidence_score": scores["confidence_score"],
            "hiring_recommendation": _hiring_recommendation(scores["overall_score"]),
            "strengths": [],
            "weaknesses": [],
            "topics_to_improve": [],
            "missed_concepts": [],
            "recommended_topics": [],
            "recommended_leetcode_problems": [],
            "recommended_resources": [],
            "detailed_feedback": "",
        }

        if not scored:
            report["hiring_recommendation"] = "Needs Improvement"
            report["detailed_feedback"] = "No answers were scored in this interview, so there is nothing to assess yet. Answer a few questions and try again."
        else:
            qa_summary = "\n\n".join(
                f"Q{i + 1} ({qa.stage or 'interview'}): {qa.question}\n"
                f"Candidate said: {qa.answer[:800]}\n"
                f"Score: {qa.score}/10 (accuracy {qa.dims.get('technical_accuracy', 0):.0f}, depth {qa.dims.get('depth', 0):.0f}, "
                f"completeness {qa.dims.get('completeness', 0):.0f}, clarity {qa.dims.get('clarity', 0):.0f})\n"
                f"Grader notes: {qa.feedback}"
                for i, qa in enumerate(scored)
            )
            limited = "Only a few questions were answered, so say plainly that the assessment is based on limited evidence." if len(scored) < 3 else ""

            prompt = f"""You are writing the qualitative part of a mock-interview assessment.

Interview type: {session.interview_type.value}
Questions answered: {len(scored)}
Final scores (already computed, do not change them): overall {scores['overall_score']}/10, technical {scores['technical_score']}/10, communication {scores['communication_score']}/10.
{limited}

What happened in the interview:
{qa_summary}

Using ONLY evidence from the answers above (do not invent topics the candidate never discussed), return JSON:
{{
  "strengths": ["specific strength 1", "specific strength 2"],
  "weaknesses": ["specific weakness 1", "specific weakness 2"],
  "topics_to_improve": ["topic 1", "topic 2"],
  "missed_concepts": ["concept the candidate missed or got wrong"],
  "recommended_topics": ["topic to study next"],
  "recommended_leetcode_problems": ["problem name"],
  "recommended_resources": ["resource"],
  "detailed_feedback": "One honest paragraph that matches the scores above"
}}

Return ONLY valid JSON."""

            llm_part = None
            try:
                content = llm.invoke(prompt).content
                match = re.search(r"\{.*\}", content, re.DOTALL)
                llm_part = json.loads(match.group()) if match else None
            except Exception:
                llm_part = None

            if isinstance(llm_part, dict):
                for key in ("strengths", "weaknesses", "topics_to_improve", "missed_concepts", "recommended_topics",
                            "recommended_leetcode_problems", "recommended_resources"):
                    if isinstance(llm_part.get(key), list):
                        report[key] = [str(x) for x in llm_part[key]]
                report["detailed_feedback"] = str(llm_part.get("detailed_feedback", ""))

            # If the writer failed, fall back to what the grader already noted for each answer
            if not report["detailed_feedback"]:
                report["strengths"] = report["strengths"] or [x for qa in scored for x in qa.strengths][:4]
                report["weaknesses"] = report["weaknesses"] or [x for qa in scored for x in qa.weaknesses][:4]
                report["detailed_feedback"] = (
                    f"Across {len(scored)} scored answers you averaged {scores['overall_score']}/10. "
                    "The written summary couldn't be generated this time; the strengths and gaps listed come from the per-answer feedback."
                )

        report["session_id"] = session.session_id
        report["user_id"] = session.user_id
        report["interview_type"] = session.interview_type.value
        report["duration_minutes"] = (session.end_time - session.start_time).total_seconds() / 60 if session.end_time else 0
        report["questions_answered"] = len(history)
        report["questions_scored"] = len(scored)

        return report
