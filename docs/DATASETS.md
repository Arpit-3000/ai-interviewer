# Datasets Documentation

## 📚 datasets/ - Question Banks

**Purpose**: Curated question banks for each technical domain

**Format**: JSON Lines (one question per line)

**Location**: `ai-service/datasets/`

---

## Question File Structure

Each line is a JSON object:

```json
{
  "domain": "DSA",
  "difficulty": "Medium",
  "question": "What is dynamic programming?",
  "expected_points": [
    "Overlapping subproblems",
    "Optimal substructure",
    "Memoization vs Tabulation"
  ]
}
```

---

## Available Datasets

### 1. `dsa.txt` - Data Structures & Algorithms

**Topics Covered**:
- Arrays, Linked Lists, Stacks, Queues
- Trees, Graphs, Heaps
- Sorting, Searching
- Dynamic Programming
- Greedy Algorithms
- Recursion

**Example Questions**:
- "What is time complexity?"
- "Explain binary search"
- "What is dynamic programming?"

---

### 2. `react.txt` - React Framework

**Topics Covered**:
- Components, Props, State
- Hooks (useState, useEffect, etc.)
- Virtual DOM, Reconciliation
- Context API, Redux
- Performance Optimization
- React Router

**Example Questions**:
- "Explain React reconciliation"
- "What are React hooks?"
- "How does useEffect work?"

---

### 3. `node.txt` - Node.js

**Topics Covered**:
- Event Loop
- Streams, Buffers
- Express.js
- Middleware
- Database Integration
- Error Handling

**Example Questions**:
- "Explain Node.js event loop"
- "What are streams in Node.js?"
- "How does middleware work in Express?"

---

### 4. `c_cpp_java.txt` - C++/Java

**Topics Covered**:
- Language syntax
- OOP concepts
- Memory management
- STL/Collections
- Templates/Generics
- Exception handling

---

### 5. `dbms.txt` - Database Management

**Topics Covered**:
- SQL queries
- Joins, Indexes
- Normalization
- ACID properties
- Transactions
- NoSQL basics

**Example Questions**:
- "Explain database normalization"
- "What are indexes?"
- "ACID properties?"

---

### 6. `os.txt` - Operating Systems

**Topics Covered**:
- Processes, Threads
- Scheduling algorithms
- Memory management
- Deadlocks
- File systems
- Synchronization

---

### 7. `cn.txt` - Computer Networks

**Topics Covered**:
- OSI Model
- TCP/IP
- HTTP/HTTPS
- DNS, Routing
- Network protocols

---

### 8. `oops.txt` - Object-Oriented Programming

**Topics Covered**:
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Design patterns
- SOLID principles

---

### 9. `system_design.txt` - System Design

**Topics Covered**:
- Scalability
- Load balancing
- Caching
- Database design
- Microservices
- API design

---

## How Questions Are Used

### 1. RAG (Retrieval-Augmented Generation)

Questions are loaded into vector database (ChromaDB):

```python
# Load dataset
loader = TextLoader("datasets/react.txt")
docs = loader.load()

# Create vector store with embeddings
db = Chroma.from_documents(
    docs,
    embedding_model,
    persist_directory="vector_db/react"
)
```

### 2. Semantic Search

During interview, retrieve relevant questions:

```python
# Get 3 intermediate React questions
questions = question_bank_loader.get_questions(
    domain="react",
    difficulty="intermediate",
    k=3
)
```

### 3. LLM Reference

Retrieved questions guide the LLM:

```python
prompt = f"""
Sample questions from question bank:
{questions}

Generate a new question in similar style
but adapted to candidate's context...
"""
```

### 4. Not Direct Asking

**Important**: Questions are NOT asked directly. They:
- Serve as reference/inspiration
- Guide question difficulty
- Ensure coverage of key topics
- Help maintain consistency

LLM generates natural, contextual questions based on these references.

---

## Adding New Questions

To add questions to a dataset:

1. Open relevant `.txt` file
2. Add new line with JSON:
```json
{"domain":"React","difficulty":"Hard","question":"Explain React Fiber architecture","expected_points":["Reconciliation","Prioritization","Incremental rendering"]}
```
3. Save file
4. Vector DB will update on next load

---

## Creating New Domain Dataset

To add a new domain:

1. Create file: `datasets/your_domain.txt`
2. Add questions in JSON format
3. Update `question_bank_loader.py`:
```python
DATASET_MAPPING = {
    ...
    "your_domain": "datasets/your_domain.txt"
}
```
4. Update `models/interview_session.py`:
```python
class InterviewType(str, Enum):
    ...
    YOUR_DOMAIN = "your_domain"
```
5. Update domain mapping in `interview_conductor.py`

---

## Question Quality Guidelines

Good questions should:
- Be clear and specific
- Have verifiable answers
- Include expected key points
- Cover range of difficulties
- Be relevant to real interviews

---

## Vector Database Storage

Questions are stored in `vector_db/` subdirectories:

```
vector_db/
├── react/
├── dsa/
├── node/
└── ...
```

Each contains ChromaDB files for fast semantic search.

---

See FILE_BY_FILE.md for complete documentation of all services.
