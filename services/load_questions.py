from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from services.embeddings import embedding_model

loader = TextLoader("datasets/dsa.txt")

docs = loader.load()

db = Chroma.from_documents(
    docs,
    embedding_model,
    persist_directory="vector_db/questions"
)

