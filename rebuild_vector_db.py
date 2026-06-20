"""
Rebuild vector database from datasets
Run this after updating question banks in datasets/
"""

import os
import shutil
from services.question_bank_loader import QuestionBankLoader

def clear_vector_db():
    """Remove old vector database"""
    vector_db_path = "vector_db"
    
    if os.path.exists(vector_db_path):
        print(f"Clearing old vector database at {vector_db_path}...")
        for item in os.listdir(vector_db_path):
            if item != ".gitkeep":
                item_path = os.path.join(vector_db_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        print("✅ Old vector database cleared")
    else:
        os.makedirs(vector_db_path, exist_ok=True)
        print("✅ Created vector_db directory")

def rebuild_all_domains():
    """Load all datasets into vector database"""
    
    loader = QuestionBankLoader()
    
    domains = [
        "dsa",
        "react", 
        "node",
        "cpp_java",
        "dbms",
        "os",
        "cn",
        "oops",
        "system_design"
    ]
    
    print("\n🔄 Rebuilding vector database from datasets...\n")
    
    for domain in domains:
        print(f"Loading {domain}...", end=" ")
        try:
            db = loader.load_dataset(domain)
            if db:
                print(f"✅ Loaded successfully")
            else:
                print(f"⚠️  Dataset file not found")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n✅ Vector database rebuild complete!")
    print(f"📊 Loaded {len(loader.vector_stores)} domains")
    print("\nYou can now start the AI service:")
    print("  uvicorn app:app --reload --port 8000")

if __name__ == "__main__":
    print("=" * 50)
    print("  CodeOrbit AI - Vector Database Rebuild")
    print("=" * 50)
    
    # Step 1: Clear old database
    clear_vector_db()
    
    # Step 2: Rebuild from new datasets
    rebuild_all_domains()
    
    print("\n" + "=" * 50)
