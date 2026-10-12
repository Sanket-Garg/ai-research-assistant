
import json
import math
from urllib.request import Request, urlopen
from embeddings import get_embedding, cosine_similarity
from pathlib import Path



notes_path = Path(__file__).parent / "research_notes.txt"
notes = notes_path.read_text(encoding="utf-8")


# Step 2: Split the notes into paragraphs.
chunks = [
    paragraph.strip()
    for paragraph in notes.split("\n\n")
    if paragraph.strip()
]


# Step 3: Generate one embedding for each paragraph.
chunk_embeddings = []

for chunk in chunks:
    embedding = get_embedding(chunk)
    chunk_embeddings.append(embedding)


# Step 4: Ask a question.
question = input("Enter your research question: ").strip()

if not question:
    raise ValueError("The question cannot be empty.")


# Step 5: Embed the question.
question_embedding = get_embedding(question)


# Step 6: Score every paragraph against the question.
results = []

for chunk, embedding in zip(chunks, chunk_embeddings):
    score = cosine_similarity(question_embedding, embedding)
    results.append((score, chunk))


# Step 7: Sort from highest similarity to lowest.
results.sort(key=lambda item: item[0], reverse=True)


# Step 8: Display the ranking.
print("\nRetrieved research passages:")

for rank, (score, chunk) in enumerate(results, start=1):
    print(f"\nRank {rank} | Similarity: {score:.4f}")
    print(chunk)

top_results = results[:3]

context = "\n\n".join(
    chunk for score, chunk in top_results
)

prompt = f"""
You are a careful research assistant.

Answer using only the context below.
If the context does not contain enough information,
say so. Do not invent facts.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

print("\nGenerated prompt:")
print(prompt)