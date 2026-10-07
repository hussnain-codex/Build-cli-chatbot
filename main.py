import os
import argparse


from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


# -----------------------------
# LLM Provider
# -----------------------------

def get_llm(provider):

    if provider == "groq":

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in .env")

        return ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7
        )

    elif provider == "gemini":

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env")

        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0.7,
            timeout=30,
            max_retries=2
        )

    elif provider == "ollama":

        # Imported here so groq/gemini work without langchain-ollama installed
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            temperature=0.7
        )

    else:
        raise ValueError(f"Unknown provider: {provider}")

# -----------------------------
# Command Line Arguments
# -----------------------------

parser = argparse.ArgumentParser(
    description="Multi-Provider AI Chatbot"
)

parser.add_argument(
    "--provider",
    choices=["groq", "gemini", "ollama"],
    default="groq",
    help="Choose AI provider"
)

args = parser.parse_args()


# -----------------------------
# Create LLM
# -----------------------------

try:
    llm = get_llm(args.provider)

except Exception as e:
    print(f"ERROR: {e}")
    exit()


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Answer clearly and simply."
    ),

    MessagesPlaceholder(
        variable_name="history"
    ),

    (
        "human",
        "{question}"
    )
])


# -----------------------------
# Output Parser
# -----------------------------

parser_output = StrOutputParser()


# -----------------------------
# LCEL Chain
# -----------------------------

chain = prompt | llm | parser_output


# -----------------------------
# Conversation History
# -----------------------------

history = []


# -----------------------------
# Start Chatbot
# -----------------------------

print("=" * 40)
print("      MULTI-PROVIDER AI CHATBOT")
print("=" * 40)

print(f"Provider: {args.provider}")
print("Type 'exit' to quit.\n")


# -----------------------------
# Chat Loop
# -----------------------------

while True:

    try:
        user_input = input("You: ")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

    # Exit command
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Ignore empty input
    if not user_input.strip():
        continue


    # -------------------------
    # Stream AI Response
    # -------------------------

    print("AI: ", end="")

    full_response = ""

    try:

        for chunk in chain.stream({
            "history": history,
            "question": user_input
        }):

            print(chunk, end="", flush=True)

            full_response += chunk

        print()

    except KeyboardInterrupt:

        print("\n(Response cancelled)")
        continue

    except Exception as e:

        print("\nERROR:", e)
        continue


    # -------------------------
    # Save Conversation
    # -------------------------

    history.append(
        HumanMessage(
            content=user_input
        )
    )

    history.append(
        AIMessage(
            content=full_response
        )
    )