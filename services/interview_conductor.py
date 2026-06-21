from services.llm import llm
from services.difficulty_adapter import DifficultyAdapter
from services.question_bank_loader import question_bank_loader
from models.interview_session import InterviewSession, InterviewStage, InterviewType
from typing import Optional, Dict

class InterviewConductor:
    """
    Core interview logic - generates questions based on context
    """
    
    @staticmethod
    def generate_introduction(session: InterviewSession) -> str:
        """Generate personalized introduction"""
        # Don't use name from resume in introduction - we'll get it from their response
        intro = f"""Hello,

I will be conducting your {session.interview_type.value} interview today.
This interview will assess your technical knowledge, problem-solving ability, and communication skills.

Please introduce yourself briefly and let me know your name."""
        
        return intro
    
    @staticmethod
    def generate_response_to_answer(session: InterviewSession, answer: str, evaluation: Dict) -> str:
        """Generate contextual response to candidate's answer before asking next question"""
        candidate_name = session.resume_context.get("candidate_name", "")
        last_qa = session.conversation_history[-1] if session.conversation_history else None
        
        # Check if answer indicates "don't know" or uncertainty
        dont_know_indicators = ["don't know", "not sure", "i don't", "no idea", "don't remember", "can't recall", "not familiar"]
        is_uncertain = any(indicator in answer.lower() for indicator in dont_know_indicators)
        
        score = evaluation.get("overall_score", 5.0)
        
        prompt = f"""You are an empathetic interviewer responding to a candidate's answer.

Candidate Name: {candidate_name if candidate_name else "the candidate"}
Question Asked: {last_qa.question if last_qa else ""}
Candidate's Answer: {answer}
Answer Score: {score}/10
Is Uncertain/Don't Know: {is_uncertain}

Generate a brief, natural response that:
1. If they said "I don't know" or showed uncertainty: Be supportive and encouraging, say something like "That's okay, let's move on to another question" or "No worries, let me ask you something different"
2. If they answered well (score > 7): Acknowledge positively but briefly, like "Good explanation" or "That's a solid understanding"
3. If they answered partially (score 4-7): Acknowledge their attempt, like "I see your point" or "You're on the right track"
4. If they answered poorly (score < 4): Be encouraging, like "Let's explore another area"

IMPORTANT:
- Use their name if available: "{candidate_name}" 
- Keep it under 15 words
- Be natural and conversational
- Don't say "Let's continue the interview" - that's robotic
- Don't give detailed feedback here - just acknowledge and transition

Generate ONLY the response text, nothing else:"""
        
        response = llm.invoke(prompt)
        return response.content.strip()
    
    @staticmethod
    def generate_question(session: InterviewSession) -> str:
        """Generate next question based on session context"""
        
        # Build context from session
        context_parts = []
        
        # Candidate name if available
        candidate_name = session.resume_context.get("candidate_name", "")
        
        # Resume context
        if session.resume_context:
            skills = session.resume_context.get("skills", [])
            projects = session.resume_context.get("projects", [])
            context_parts.append(f"Candidate Skills: {', '.join(skills[:10])}")
            context_parts.append(f"Projects: {projects[:3]}")
        
        # Coding profile context
        if session.coding_profile:
            context_parts.append(f"LeetCode Rating: {session.coding_profile.leetcode_rating}")
            context_parts.append(f"Strong Topics: {', '.join(session.coding_profile.strong_topics)}")
            context_parts.append(f"Weak Topics: {', '.join(session.coding_profile.weak_topics)}")
        
        # Get relevant questions from question bank for technical domains
        sample_questions = ""
        if session.stage == InterviewStage.TECHNICAL_ROUND:
            domain = InterviewConductor._get_domain_from_interview_type(session.interview_type)
            if domain:
                questions = question_bank_loader.get_questions(
                    domain, 
                    session.difficulty.value, 
                    k=3
                )
                if questions:
                    sample_questions = "Sample questions from question bank:\n" + "\n".join([
                        f"- {q.get('question', '')}" for q in questions[:3]
                    ])
        
        # Previous questions
        previous_questions = "\n".join([f"- {qa.question}" for qa in session.conversation_history[-5:]])
        
        # Difficulty context
        difficulty_ctx = DifficultyAdapter.get_difficulty_context(session.difficulty)
        
        # Stage-specific instructions
        stage_instructions = InterviewConductor._get_stage_instructions(session.stage, session.interview_type)
        
        prompt = f"""You are conducting a professional {session.interview_type.value} interview.

Context:
{chr(10).join(context_parts)}
Candidate Name: {candidate_name if candidate_name else "Not yet provided"}

Current Stage: {session.stage.value}
Difficulty: {session.difficulty.value}

{stage_instructions}

{difficulty_ctx}

{sample_questions}

Previous Questions Asked:
{previous_questions}

Rules:
- Ask ONE clear, specific question
- Do NOT repeat previous questions
- Make it feel like a real interviewer, not a chatbot
- Be professional but friendly
- DON'T use generic terms like "candidate" - use their name "{candidate_name}" if you have it
- If at resume discussion stage, ask about specific projects or skills from the resume
- If coding profile shows weak areas, probe those topics
- For technical round, ask domain-specific questions (use sample questions as reference)
- For follow-ups, reference the previous answer

Generate the next interview question:"""
        
        response = llm.invoke(prompt)
        return response.content.strip()
    
    @staticmethod
    def extract_candidate_name(introduction_answer: str) -> str:
        """Extract candidate's name from their introduction"""
        prompt = f"""Extract the candidate's name from their introduction.

Introduction: {introduction_answer}

Rules:
- Return ONLY the first name or preferred name
- If they say "My name is John Doe", return "John"
- If they say "I'm Jane Smith", return "Jane"
- If no clear name is found, return empty string

Return only the name, nothing else:"""
        
        response = llm.invoke(prompt)
        name = response.content.strip().strip('"').strip("'")
        return name if name and len(name) < 30 else ""
    
    @staticmethod
    def _get_domain_from_interview_type(interview_type: InterviewType) -> str:
        """Map interview type to dataset domain"""
        domain_mapping = {
            InterviewType.DSA: "dsa",
            InterviewType.REACT: "react",
            InterviewType.NODE: "node",
            InterviewType.CPP_JAVA: "cpp_java",
            InterviewType.DBMS: "dbms",
            InterviewType.OS: "os",
            InterviewType.CN: "cn",
            InterviewType.OOPS: "oops",
            InterviewType.SYSTEM_DESIGN: "system_design"
        }
        return domain_mapping.get(interview_type)
    
    @staticmethod
    def _get_stage_instructions(stage: InterviewStage, interview_type: InterviewType) -> str:
        """Get instructions for current stage"""
        instructions = {
            InterviewStage.INTRODUCTION: "Ask the candidate to introduce themselves.",
            InterviewStage.RESUME_DISCUSSION: "Ask about specific projects, technologies, or experiences mentioned in their resume. Probe for depth.",
            InterviewStage.TECHNICAL_ROUND: "Ask technical questions based on their skills and interview type. Test understanding and problem-solving.",
            InterviewStage.BEHAVIORAL_ROUND: "Ask behavioral questions: challenges faced, teamwork, conflict resolution, leadership.",
            InterviewStage.CLOSING: "Ask if they have any questions. Wrap up professionally."
        }
        
        return instructions.get(stage, "")
    
    @staticmethod
    def generate_followup(session: InterviewSession, last_answer: str) -> str:
        """Generate follow-up question based on previous answer"""
        last_qa = session.conversation_history[-1]
        
        prompt = f"""You are conducting an interview.

Original Question: {last_qa.question}

Candidate's Answer: {last_answer}

Based on their answer, generate ONE follow-up question to:
- Probe deeper into their understanding
- Ask about edge cases or trade-offs
- Ask about alternatives or comparisons
- Clarify vague points

Make it feel natural and conversational.

Follow-up question:"""
        
        response = llm.invoke(prompt)
        return response.content.strip()
