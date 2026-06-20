from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

# Using HuggingFace embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)