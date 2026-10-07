import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY not found")
    exit()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

messages = [
    SystemMessage(
        content="You are a helpful assistant."
    )
]

print("AI Chatbot Started!")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user message
    messages.append(
        HumanMessage(content=user_input)
    )

    # Send complete conversation
    response = llm.invoke(messages)

    # Display AI response
    print("AI:", response.content)

    # Save AI response
    messages.append(
        AIMessage(content=response.content)
    )