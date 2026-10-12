# AI Research Assistant

A local AI research assistant built with Python and Ollama. This project explores LLM integration, conversation history, embeddings, semantic search, and Retrieval-Augmented Generation (RAG).

## Features

- **General mode:** Answers questions using the language model's general knowledge.
- **Research mode:** Retrieves relevant passages from local research notes and uses them as context for answers.
- **Conversation history:** Includes recent messages in the prompt to support follow-up questions.
- **Semantic retrieval:** Uses embeddings and cosine similarity to rank research passages by relevance.
- **Basic evaluation:** Runs test questions against the assistant's research and general modes.

## Technologies

- Python 3.11+
- [Ollama](https://ollama.com/)
- `qwen2.5:3b` — text generation
- `nomic-embed-text` — text embeddings

## Setup

1. Install Python and Ollama.
2. Download the required models:

   ```bash
   ollama pull qwen2.5:3b
   ollama pull nomic-embed-text
   ```

3. Clone this repository and enter its directory.
4. Create and activate a Python virtual environment if desired.
5. Start Ollama and run the assistant:

   ```bash
   python main.py
   ```

## Project files

- `main.py` — interactive command-line interface.
- `assistant.py` — assistant logic, prompts, retrieval, and Ollama generation requests.
- `embeddings.py` — embedding generation and cosine similarity.
- `embedding_demo.py` — experiments with embeddings and retrieval.
- `history_demo.py` — conversation history experiment.
- `evaluate.py` — basic assistant evaluation.
- `research_notes.txt` — sample knowledge base.
- `.gitignore` — excludes local environment and generated files.

## Current limitations

- Research notes are split into paragraphs rather than more advanced chunks.
- The top three passages are retrieved even when they may not be sufficiently relevant.
- Evaluation uses basic expected-phrase matching and does not guarantee answer correctness.
- This is a learning project, not a production-ready application.

## Learning goals

Understand how to connect a language model, maintain conversation context, generate embeddings, retrieve relevant text, and build a basic RAG pipeline.
