from openai import OpenAI

client = OpenAI(api_key="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")


SYSTEM_PROMPT = (
    "You are a calm, assertive emergency AI assistant. "
    "Gather critical details quickly and respond clearly. "
    "Prioritize life-threatening emergencies. Ask for location, nature of emergency, and if help is needed."
)

def emergency_chat():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    print("\nEmergency Assistant is ready. Type your messages below (type 'exit' to quit):\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(model="gpt-4-0613",
            messages=messages,
            temperature=0.3)
            bot_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": bot_message})
            print(f"AI: {bot_message}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    emergency_chat()
