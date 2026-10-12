from assistant import ask_assistant, AssistantError


test_cases = [
    {
        "question": "What is overfitting?",
        "mode": "research",
        "expected_phrases": ["training"],
        "description": "Research: supported question",
    },
    {
        "question": "What do my notes say about quantum computing?",
        "mode": "research",
        "expected_phrases": [
            "not contain enough information",
            "do not contain enough information",
            "do not contain any information",
        ],
        "description": "Research: missing information",
    },
    {
        "question": "What is supervised learning?",
        "mode": "research",
        "expected_phrases": ["labeled"],
        "description": "Research: supervised learning",
    },
    {
        "question": "What is quantum computing?",
        "mode": "general",
        "expected_phrases": ["quantum"],
        "description": "General: outside the notes",
    },
]

passed = 0
failed = 0
errors = 0

for index, test in enumerate(test_cases, start=1):
    print(f"\nTest {index}: {test['description']}")
    print(f"Mode: {test['mode']}")
    print(f"Question: {test['question']}")

    try:
        answer = ask_assistant(
            test["question"],
            mode=test["mode"],
        )

        print(f"Answer: {answer}")

        expected_phrases = test["expected_phrases"]

        if any(
            phrase.lower() in answer.lower()
            for phrase in expected_phrases
        ):
            print("Result: PASS")
            passed += 1
        else:
            print("Result: FAIL")
            print("Expected one of:", expected_phrases)
            failed += 1

    except (AssistantError, ValueError) as error:
        print(f"Result: ERROR — {error}")
        errors += 1

total = len(test_cases)

print("\n" + "=" * 40)
print("EVALUATION REPORT")
print("=" * 40)
print(f"Total tests: {total}")
print(f"Passed:      {passed}")
print(f"Failed:      {failed}")
print(f"Errors:      {errors}")
print(f"Pass rate:   {passed / total:.1%}")
print("=" * 40)
