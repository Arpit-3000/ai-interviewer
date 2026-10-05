from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os

load_dotenv()

# Override with GROQ_MODEL in .env if Groq retires/renames the model again
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

llm = ChatGroq(model=GROQ_MODEL, api_key=os.getenv("GROQ_API_KEY"))
