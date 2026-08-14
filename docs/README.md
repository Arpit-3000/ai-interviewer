# AI Interview Service Documentation

Welcome to the complete documentation for CodeOrbit AI Interview Service!

## 📚 Documentation Files

This `docs/` folder contains comprehensive documentation explaining every aspect of the AI interview system.

### 📖 Available Guides

1. **[COMPLETE_INDEX.md](COMPLETE_INDEX.md)** - Start here! Navigation guide to all docs
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Project structure & design patterns
3. **[FILE_BY_FILE.md](FILE_BY_FILE.md)** - Detailed explanation of each file (Part 1)
4. **[FILE_BY_FILE_PART2.md](FILE_BY_FILE_PART2.md)** - Services documentation (Part 2)
5. **[SERVICES_PART3.md](SERVICES_PART3.md)** - Advanced services (Part 3)
6. **[ROUTES.md](ROUTES.md)** - REST API endpoints reference
7. **[DATASETS.md](DATASETS.md)** - Question banks & RAG system

### 🚀 Quick Links

- New to the project? → [QUICK_START.md](../QUICK_START.md)
- Want to understand the code? → [FILE_BY_FILE.md](FILE_BY_FILE.md)
- Need API reference? → [ROUTES.md](ROUTES.md)
- Adding questions? → [DATASETS.md](DATASETS.md)
- Integrating with backend? → [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)

---

## 🎯 What is this service?

An AI-powered mock interview platform that:

✅ Conducts realistic technical interviews
✅ Adapts difficulty dynamically  
✅ Evaluates answers comprehensively
✅ Generates detailed reports
✅ Supports 12+ interview domains
✅ Integrates with CodeOrbit platform

---

## 🏗️ Architecture at a Glance

```
User Interview Flow:
1. Start interview → Get session ID
2. Answer questions → Get evaluated + next question  
3. Difficulty auto-adjusts
4. End interview → Get comprehensive report

Technical Stack:
- FastAPI (Python web framework)
- LangChain + Groq (LLM orchestration)
- ChromaDB (Vector database for RAG)
- Sentence Transformers (Embeddings)
```

---

## 📂 Project Structure

```
ai-service/
├── docs/              ← You are here
├── models/            ← Data structures
├── services/          ← Business logic
├── routes/            ← API endpoints
├── datasets/          ← Question banks
└── app.py            ← Main application
```

---

## 🤔 Common Questions

**Q: How does the AI generate questions?**
A: Uses RAG (Retrieval-Augmented Generation) combining question banks with LLM

**Q: Can difficulty change during interview?**
A: Yes! Dynamically adjusts based on last 3 answers

**Q: How are answers evaluated?**  
A: LLM scores on 5 dimensions: technical accuracy, depth, clarity, completeness, communication

**Q: What interview types are supported?**
A: DSA, React, Node, DBMS, OS, Networks, System Design, and more

**Q: Is voice support included?**
A: Yes (optional), using Whisper (STT) and gTTS (TTS)

---

## 💡 Tips for Reading Docs

- Start with [COMPLETE_INDEX.md](COMPLETE_INDEX.md) for navigation
- Code examples are included throughout
- Each file has "Purpose" and "When called" sections
- Data flow diagrams explain interactions

---

## 🆘 Need Help?

- Read [IMPLEMENTATION_SUMMARY.md](../../IMPLEMENTATION_SUMMARY.md) for overview
- Check [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md) for setup
- Run `python test_api.py` to test the service

---

Happy learning! 🚀
