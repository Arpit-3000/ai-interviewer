from langchain_community.vectorstores import Chroma

from services.embeddings import embedding_model

def create_vector_db(chunks):
    db = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory="vector_db"
    )

    return db