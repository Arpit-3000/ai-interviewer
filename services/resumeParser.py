from langchain_community.document_loaders import PyPDFLoader

def parse_resume(path):
    loader = PyPDFLoader(path)

    docs = loader.load()

    return docs
