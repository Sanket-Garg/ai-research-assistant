
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from embeddings import get_embedding, cosine_similarity

class AssistantError(Exception):
    """An expected error while running the AI assistant."""


def load_research_notes():
    """Read research notes from the project folder."""
    notes_path = Path(__file__).parent / "research_notes.txt"

    try:
        return notes_path.read_text(encoding="utf-8")
    except OSError as error:
        raise AssistantError(
            f"Could not read research notes: {error}"
        ) from error

def retrieve_context(question, top_k=3):
    """Retrieve the most relevant research passages for a question."""
    notes = load_research_notes()

    chunks = [
        paragraph.strip()
        for paragraph in notes.split("\n\n")
        if paragraph.strip()
    ]

    chunk_embeddings = [
        get_embedding(chunk)
        for chunk in chunks
    ]

    question_embedding = get_embedding(question)

    results = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(question_embedding, embedding)
        results.append((score, chunk))

    results.sort(key=lambda item: item[0], reverse=True)

    top_results = results[:top_k]

    context = "\n\n".join(
        chunk for score, chunk in top_results
    )

    return context

def format_history(history):
    """Format recent conversation messages as text."""
    recent_history = history[-6:]

    if not recent_history:
        return "No previous conversation."

    formatted_messages = []

    for message in recent_history:
        role = message["role"]
        content = message["content"]
        formatted_messages.append(f"{role}: {content}")

    return "\n".join(formatted_messages)

def ask_assistant(question, mode, history =None, context = None):
    """Answer a question in research or general mode."""

    if not question or not question.strip():
        raise ValueError("The question cannot be empty.")

    if mode not in ("research", "general"):
        raise ValueError(
            "Invalid mode. Choose 'research' or 'general'."
        )
    history_text = format_history(history)
    if mode == "research":
        if context is None:
            context = retrieve_context(question)
        3
        
        prompt = f"""
        You are a careful AI research assistant.

        Rules:
        1. Answer using only the context below.
        2. If the context lacks relevant information, say:
        "The research notes do not contain enough information
        to answer this question."
        3. Do not invent facts or use outside knowledge to fill gaps.
        4. Keep your answer clear and concise.

        RETRIEVED CONTEXT:
        {context}

        PREVIOUS CONVERSATION:
        {history_text}

        USER QUESTION:
        {question}

        ANSWER:
        """

    else:
        prompt = f"""
        You are a helpful AI assistant.

        Answer the user's question using your general knowledge.
        Be clear and concise. If you are uncertain, say so.
        Do not claim to have searched the internet.

        PREVIOUS CONVERSATION:
        {history_text}

        USER QUESTION:
        {question}

        ANSWER:
        """
    if history is None:
        history = []

    request_data = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }

    request = Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(request_data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(request, timeout=120) as response:
            response_text = response.read().decode("utf-8")

    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise AssistantError(
            f"Ollama returned HTTP {error.code}: {details}"
        ) from error

    except URLError as error:
        raise AssistantError(
            f"Could not connect to Ollama: {error.reason}. "
            "Check that Ollama is running."
        ) from error

    except TimeoutError as error:
        raise AssistantError(
            "The request timed out. Please try again."
        ) from error

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise AssistantError(
            "Ollama returned invalid JSON."
        ) from error

    answer = result.get("response")

    if not isinstance(answer, str):
        raise AssistantError(
            "Ollama's response did not contain a valid answer."
        )
    
    return answer

