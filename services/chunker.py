from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,
    chunk_overlap=100
    )

    return splitter.split_documents(docs)