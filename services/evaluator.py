from services.llm import llm

def evaluate(question,answer):
    prompt = f"""
    Question:
    {question}

    Answer:
    {answer}

    Give:
    Score/10
    
    Strenghts

    Weakness

    """

    response=llm.invoke(prompt)

    return response.content