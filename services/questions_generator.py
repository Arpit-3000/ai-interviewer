from services.llm import llm

def generate_questions(
        resume_context, previous_questions
):
    prompt = f"""
    Resume:
    {resume_context}

    Previous:
    {previous_questions}

    Ask ONE interview question.

    """

    response = llm.invoke(prompt)

    return response.content