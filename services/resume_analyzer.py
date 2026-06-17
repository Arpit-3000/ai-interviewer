from services.resumeParser import parse_resume
from services.llm import llm
from typing import Dict
import json

def analyze_resume(resume_path: str) -> Dict:
    """
    Parse and analyze resume to extract key information
    """
    docs = parse_resume(resume_path)
    resume_text = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
    Analyze this resume and extract structured information in JSON format.
    
    Resume:
    {resume_text}
    
    Extract:
    - name
    - email
    - phone
    - skills (list of technical skills)
    - projects (list of project names and brief descriptions)
    - experience (list of companies and roles)
    - education (degrees and institutions)
    - years_of_experience (estimate in years)
    - primary_domain (Frontend/Backend/Full Stack/Data Science/etc.)
    
    Return ONLY valid JSON, no additional text.
    """
    
    response = llm.invoke(prompt)
    
    try:
        analysis = json.loads(response.content)
    except:
        # Fallback if JSON parsing fails
        analysis = {
            "raw_text": resume_text,
            "skills": [],
            "projects": [],
            "experience": [],
            "education": []
        }
    
    return analysis
