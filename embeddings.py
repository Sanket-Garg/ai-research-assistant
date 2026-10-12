
import json
import math
from urllib.request import Request, urlopen


def get_embedding(text):
    """Convert text into a numerical vector using Ollama."""
    url = "http://localhost:11434/api/embed"

    data = {
        "model": "nomic-embed-text",
        "input": text
    }

    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=120) as response:
        response_text = response.read().decode("utf-8")

    result = json.loads(response_text)
    return result["embeddings"][0]


def cosine_similarity(vector_a, vector_b):
    """Calculate the cosine similarity between two vectors."""
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cannot compare a zero-length vector.")

    return dot_product / (magnitude_a * magnitude_b)
