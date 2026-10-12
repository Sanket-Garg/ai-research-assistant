
from assistant import ask_assistant, AssistantError


def main():
    while True:
        print("\n=== AI Assistant ===")
        print("1. Research mode")
        print("2. General mode")
        print("3. Exit")

        mode_choice = input("Choose a mode: ").strip()

        if mode_choice == "3":
            print("Goodbye!")
            break

        if mode_choice == "1":
            mode = "research"
        elif mode_choice == "2":
            mode = "general"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        # A new, empty history for each new chat.
        history = []

        print(f"\nStarting a new {mode} chat.")
        print("Type 'exit' at a question prompt to end the program.")

        while True:
            question = input("\nYou: ").strip()

            if question.lower() == "exit":
                print("Goodbye!")
                return

            if not question:
                print("Please enter a question.")
                continue

            try:
                answer = ask_assistant(
                    question,
                    mode=mode,
                    history=history,
                )

                print(f"\n[{mode.upper()} MODE]")
                print(answer)

                # Save the exchange only after a successful answer.
                history.append({
                    "role": "user",
                    "content": question,
                })

                history.append({
                    "role": "assistant",
                    "content": answer,
                })

            except (AssistantError, ValueError) as error:
                print(f"\nAssistant error: {error}")
                continue

            print("\nWhat would you like to do?")
            print("1. Continue this chat")
            print("2. Start a new chat")
            print("3. Exit")

            next_choice = input("Choose an option: ").strip()

            if next_choice == "1":
                continue

            elif next_choice == "2":
                # Leave this chat and return to mode selection.
                break

            elif next_choice == "3":
                print("Goodbye!")
                return

            else:
                print("Invalid choice. Starting the next question in this chat.")


if __name__ == "__main__":
    main()

