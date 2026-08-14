# Interview Domains Supported

CodeOrbit AI Interview Service supports multiple technical domains with curated question banks:

## Available Interview Types

### 1. **DSA** (`dsa`)
- Data Structures & Algorithms
- Arrays, Linked Lists, Trees, Graphs
- Dynamic Programming, Greedy, Backtracking
- Time & Space Complexity Analysis
- **Dataset**: `datasets/dsa.txt`

### 2. **React** (`react`)
- React fundamentals
- Hooks, Components, State Management
- Performance Optimization
- React Router, Context API
- **Dataset**: `datasets/react.txt`

### 3. **Node.js** (`node`)
- Node.js core concepts
- Event Loop, Streams, Buffers
- Express.js, REST APIs
- Database Integration
- **Dataset**: `datasets/node.txt`

### 4. **C++/Java** (`cpp_java`)
- Language fundamentals
- OOP concepts in C++/Java
- Memory management
- STL/Collections
- **Dataset**: `datasets/c_cpp_java.txt`

### 5. **DBMS** (`dbms`)
- Database concepts
- SQL queries, Joins, Indexes
- Normalization, ACID properties
- Transactions, Concurrency
- **Dataset**: `datasets/dbms.txt`

### 6. **Operating Systems** (`os`)
- OS fundamentals
- Process, Threads, Scheduling
- Memory Management
- Deadlocks, Synchronization
- **Dataset**: `datasets/os.txt`

### 7. **Computer Networks** (`cn`)
- Networking fundamentals
- OSI Model, TCP/IP
- HTTP/HTTPS, DNS
- Routing, Protocols
- **Dataset**: `datasets/cn.txt`

### 8. **OOP** (`oops`)
- Object-Oriented Programming
- Encapsulation, Inheritance, Polymorphism
- Design Patterns
- SOLID Principles
- **Dataset**: `datasets/oops.txt`

### 9. **System Design** (`system_design`)
- System Architecture
- Scalability, Load Balancing
- Caching, Database Design
- Microservices, APIs
- **Dataset**: `datasets/system_design.txt`

### 10. **HR** (`hr`)
- Behavioral questions
- Leadership, Teamwork
- Conflict Resolution
- Career Goals

### 11. **Competitive Programming** (`competitive`)
- Contest strategies
- Problem-solving techniques
- LeetCode/Codeforces style
- Optimization tricks

### 12. **Mixed** (`mixed`)
- Combination of multiple domains
- Full-stack interview simulation
- HR + Technical + DSA

---

## How It Works

### 1. Question Bank RAG System
- Each domain has curated questions in JSON format
- Questions stored with metadata: difficulty, expected points
- Vector embeddings for semantic search
- Retrieves relevant questions based on difficulty

### 2. Dynamic Question Generation
- AI uses question bank as reference
- Generates natural, conversational questions
- Adapts based on candidate's resume & coding profile
- Maintains interview flow and context

### 3. Difficulty Levels Per Domain
- **Beginner**: Fundamental concepts
- **Intermediate**: Applied knowledge, problem-solving
- **Advanced**: Deep concepts, edge cases, optimization

---

## API Usage

### Start Domain-Specific Interview

```javascript
POST /api/ai-interview/start
{
  "interview_type": "react",  // or "dsa", "dbms", "os", etc.
  "difficulty": "intermediate"
}
```

### Supported Interview Types
```javascript
[
  "hr",
  "dsa",
  "react",
  "node",
  "cpp_java",
  "dbms",
  "os",
  "cn",
  "oops",
  "system_design",
  "competitive",
  "mixed"
]
```

### Example: React Interview
```javascript
POST /api/ai-interview/start
{
  "interview_type": "react",
  "difficulty": "advanced"
}

// AI will ask React-specific questions like:
// - "Explain React's reconciliation algorithm"
// - "How does useEffect differ from useLayoutEffect?"
// - "What are React performance optimization techniques?"
```

### Example: DBMS Interview
```javascript
POST /api/ai-interview/start
{
  "interview_type": "dbms",
  "difficulty": "intermediate"
}

// AI will ask DBMS questions like:
// - "Explain database normalization"
// - "What's the difference between clustered and non-clustered indexes?"
// - "How do you handle deadlocks?"
```

### Example: Mixed Interview
```javascript
POST /api/ai-interview/start
{
  "interview_type": "mixed",
  "difficulty": "intermediate"
}

// AI will ask questions from multiple domains:
// - HR behavioral questions
// - DSA problem-solving
// - System design scenarios
// - Domain-specific technical questions based on resume
```

---

## Question Bank Format

Each dataset file contains questions in JSON format:

```json
{
  "domain": "DSA",
  "difficulty": "Medium",
  "question": "Explain the concept of Dynamic Programming",
  "expected_points": [
    "Overlapping subproblems",
    "Optimal substructure",
    "Memoization vs Tabulation",
    "Time-space tradeoff"
  ]
}
```

---

## Adding Custom Domains

To add a new domain:

1. Create dataset file: `datasets/your_domain.txt`
2. Add questions in JSON format
3. Update `DATASET_MAPPING` in `question_bank_loader.py`
4. Add enum value to `InterviewType` in `interview_session.py`
5. Update domain mapping in `interview_conductor.py`

---

## Integration Examples

### Frontend Dropdown
```typescript
const interviewTypes = [
  { value: "hr", label: "HR Interview" },
  { value: "dsa", label: "Data Structures & Algorithms" },
  { value: "react", label: "React" },
  { value: "node", label: "Node.js" },
  { value: "dbms", label: "Database Management" },
  { value: "os", label: "Operating Systems" },
  { value: "cn", label: "Computer Networks" },
  { value: "system_design", label: "System Design" },
  { value: "mixed", label: "Full Interview (Mixed)" }
];
```

### Resume-Based Domain Selection
```javascript
// Analyze resume and suggest domain
const resume = analyzeResume(file);
const suggestedDomain = resume.skills.includes("React") ? "react" 
                      : resume.skills.includes("Node") ? "node"
                      : "mixed";
```

---

## Benefits

✅ **Domain-Specific**: Focused questions for each technology
✅ **Curated**: High-quality questions from real interviews
✅ **Adaptive**: Difficulty adjusts based on performance
✅ **Contextual**: Uses resume & coding profile for relevance
✅ **Realistic**: Natural conversation flow
✅ **Comprehensive**: Covers 12+ technical domains

---

## Next Steps

- Add more questions to each dataset
- Implement domain combination logic for "mixed" interviews
- Create domain-specific evaluation criteria
- Add company-specific interview patterns (FAANG, startups, etc.)
