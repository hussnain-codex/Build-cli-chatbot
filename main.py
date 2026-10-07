import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY not found")
    exit()

client = Groq(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]

print("AI Chatbot Started!")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        stream=True
    )

    print("AI: ", end="")

    assistant_response = ""

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            assistant_response += content

    print()

    messages.append({
        "role": "assistant",
        "content": assistant_response
    })