from langchain_community.vectorstores import Chroma
from services.embeddings import embedding_model
db = Chroma(
    persist_directory="vector_db/questions",
    embedding_function = embedding_model
)

retriever=db.as_retriever(
    search_kwargs={"k":5}
)