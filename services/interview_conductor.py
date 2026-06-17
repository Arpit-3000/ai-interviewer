from services.llm import llm
from services.difficulty_adapter import DifficultyAdapter
from services.question_bank_loader import question_bank_loader
from models.interview_session import InterviewSession, InterviewStage, InterviewType
from typing import Optional

class InterviewConductor:
    """
    Core interview logic - generates questions based on context
    """
    
    @staticmethod
    def generate_introduction(session: InterviewSession) -> str:
        """Generate personalized introduction"""
        name = session.resume_context.get("name", "candidate")
        
        intro = f"""Hello {name},

I will be conducting your {session.interview_type.value} interview today.
This interview will assess your technical knowledge, problem-solving ability, and communication skills.

Please introduce yourself briefly."""
        
        return intro
    
    @staticmethod
    def generate_question(session: InterviewSession) -> str:
        """Generate next question based on session context"""
        
        # Build context from session
        context_parts = []
        
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
- If at resume discussion stage, ask about specific projects or skills from the resume
- If coding profile shows weak areas, probe those topics
- For technical round, ask domain-specific questions (use sample questions as reference)
- For follow-ups, reference the previous answer

Generate the next interview question:"""
        
        response = llm.invoke(prompt)
        return response.content.strip()
    
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
