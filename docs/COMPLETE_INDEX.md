# Complete Documentation Index

## 📚 AI Interview Service - Complete Documentation

### Start Here
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Project structure & core concepts
- **[QUICK_START.md](../QUICK_START.md)** - Get running in 5 minutes

### Deep Dive Documentation

#### 1. File-by-File Explanations
- **[FILE_BY_FILE.md](FILE_BY_FILE.md)** - Root files, models, session manager
- **[FILE_BY_FILE_PART2.md](FILE_BY_FILE_PART2.md)** - Interview conductor, evaluator, difficulty adapter
- **[SERVICES_PART3.md](SERVICES_PART3.md)** - Report generator, resume analyzer, question bank, voice

#### 2. API Documentation
- **[ROUTES.md](ROUTES.md)** - All REST endpoints with examples

#### 3. Question Banks
- **[DATASETS.md](DATASETS.md)** - Question bank format & RAG system
- **[DOMAINS.md](../DOMAINS.md)** - Supported interview domains

#### 4. Integration
- **[INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)** - Connect to Node.js backend
- **[IMPLEMENTATION_SUMMARY.md](../../IMPLEMENTATION_SUMMARY.md)** - What's built & how to use

---

## 🎯 Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | FastAPI app entry point |
| `models/interview_session.py` | Data models & enums |
| `services/session_manager.py` | Session CRUD operations |
| `services/interview_conductor.py` | Question generation brain |
| `services/answer_evaluator.py` | Answer scoring |
| `services/difficulty_adapter.py` | Dynamic difficulty |
| `services/report_generator.py` | Final report |
| `services/question_bank_loader.py` | RAG system |
| `routes/interview_api.py` | Main API endpoints |

### Key Concepts

- **Session**: Each interview is a session with unique ID
- **Stages**: Introduction → Resume → Technical → Behavioral → Closing
- **RAG**: Question banks + LLM for intelligent generation
- **Dynamic Difficulty**: Adjusts based on performance
- **Multi-dimensional Scoring**: 5 metrics per answer

### Data Flow

```
User → Frontend → Node Backend → AI Service
                                     ↓
                          Session Manager
                                     ↓
                          Interview Conductor
                                     ↓
                    Question Bank + Resume + Profile
                                     ↓
                                  Groq LLM
                                     ↓
                          Answer Evaluator
                                     ↓
                          Difficulty Adapter
                                     ↓
                             Next Question
```

---

## 📖 Reading Guide

### For Developers
1. Start with ARCHITECTURE.md
2. Read FILE_BY_FILE.md series
3. Understand ROUTES.md
4. Review DATASETS.md
5. Check INTEGRATION_GUIDE.md

### For Users
1. QUICK_START.md
2. DOMAINS.md
3. INTEGRATION_GUIDE.md

### For Contributors
1. All above
2. IMPLEMENTATION_SUMMARY.md
3. Code comments in services/

---

## 🔗 External Resources

- **Groq**: https://console.groq.com/
- **LangChain**: https://python.langchain.com/
- **ChromaDB**: https://www.trychroma.com/
- **FastAPI**: https://fastapi.tiangolo.com/

---

Generated for CodeOrbit AI Interview Service v1.0
