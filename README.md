# AI Study Companion (Backend)

An AI-powered study assistant backend built with FastAPI and OpenRouter.

## Features

* Chat with AI
* Generate Notes
* Flashcards (structured JSON)
* Quiz generation (MCQs)
* Clean modular architecture

## Tech Stack

* FastAPI
* OpenRouter (LLM API)
* Python
* Pydantic

## API Endpoints

* /chat
* /notes
* /flashcards
* /quiz

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Future Improvements

* RAG (Retrieval-Augmented Generation)
* Quiz scoring system
* Database integration
* Frontend (React)
