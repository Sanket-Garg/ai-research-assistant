
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


conversation_history = []


def ask_ollama(prompt):
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
            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["response"]

    except HTTPError as error:
        print(f"HTTP error: {error.code}")
    except URLError as error:
        print(f"Connection error: {error.reason}")
    except (TimeoutError, KeyError, json.JSONDecodeError) as error:
        print(f"Request or response error: {error}")

    return None


def build_prompt(history):
    prompt = (
        "You are a helpful assistant. "
        "Use the conversation history to understand follow-up questions.\n\n"
    )

    for message in history:
        prompt += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt += "assistant:"
    return prompt


while True:
    question = input("\nYou (type 'exit' to quit): ").strip()

    if question.lower() == "exit":
        break

    if not question:
        print("Please enter a question.")
        continue

    conversation_history.append({
        "role": "user",
        "content": question
    })

    recent_history = conversation_history[-6:] 
    prompt = build_prompt(recent_history)
    answer = ask_ollama(prompt)

    if answer is None:
        conversation_history.pop()
        continue

    print(f"\nAssistant: {answer}")

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })
