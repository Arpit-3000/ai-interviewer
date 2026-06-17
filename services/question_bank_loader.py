"""
Load and retrieve questions from domain-specific datasets
"""
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from services.embeddings import embedding_model
import os
import json
from typing import List, Dict

class QuestionBankLoader:
    """
    Manages loading and retrieving questions from multiple domain datasets
    """
    
    DATASET_MAPPING = {
        "dsa": "datasets/dsa.txt",
        "react": "datasets/react.txt",
        "node": "datasets/node.txt",
        "cpp_java": "datasets/c_cpp_java.txt",
        "dbms": "datasets/dbms.txt",
        "os": "datasets/os.txt",
        "cn": "datasets/cn.txt",
        "oops": "datasets/oops.txt",
        "system_design": "datasets/system_design.txt"
    }
    
    def __init__(self):
        self.vector_stores = {}
    
    def load_dataset(self, domain: str) -> Chroma:
        """Load a specific domain's question bank into vector store"""
        if domain in self.vector_stores:
            return self.vector_stores[domain]
        
        dataset_path = self.DATASET_MAPPING.get(domain)
        if not dataset_path or not os.path.exists(dataset_path):
            return None
        
        try:
            loader = TextLoader(dataset_path)
            docs = loader.load()
            
            # Create vector store for this domain
            db = Chroma.from_documents(
                docs,
                embedding_model,
                persist_directory=f"vector_db/{domain}"
            )
            
            self.vector_stores[domain] = db
            return db
        except Exception as e:
            print(f"Error loading dataset {domain}: {e}")
            return None
    
    def get_questions(self, domain: str, difficulty: str = None, k: int = 5) -> List[Dict]:
        """
        Retrieve questions from a specific domain
        Optionally filter by difficulty
        """
        db = self.load_dataset(domain)
        if not db:
            return []
        
        try:
            # Build query based on difficulty
            if difficulty:
                query = f"difficulty {difficulty} questions"
            else:
                query = f"{domain} interview questions"
            
            retriever = db.as_retriever(search_kwargs={"k": k})
            results = retriever.get_relevant_documents(query)
            
            questions = []
            for doc in results:
                try:
                    # Parse JSON format questions
                    question_data = json.loads(doc.page_content)
                    questions.append(question_data)
                except:
                    # If not JSON, use raw text
                    questions.append({"question": doc.page_content})
            
            return questions
        except Exception as e:
            print(f"Error retrieving questions: {e}")
            return []
    
    def get_random_question(self, domain: str, difficulty: str = None) -> Dict:
        """Get a single random question from domain"""
        questions = self.get_questions(domain, difficulty, k=1)
        return questions[0] if questions else None
    
    def get_multi_domain_questions(self, domains: List[str], difficulty: str = None, k_per_domain: int = 2) -> List[Dict]:
        """Get questions from multiple domains"""
        all_questions = []
        for domain in domains:
            questions = self.get_questions(domain, difficulty, k=k_per_domain)
            all_questions.extend(questions)
        return all_questions

# Global instance
question_bank_loader = QuestionBankLoader()
