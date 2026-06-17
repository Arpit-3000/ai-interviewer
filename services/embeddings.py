from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

# Using HuggingFace embeddings (works with Groq)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)