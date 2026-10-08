import os
import argparse

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_core.output_parsers import StrOutputParser


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Get LLM
# ==========================================

def get_llm(provider):

    if provider == "groq":

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        return ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7
        )

    elif provider == "gemini":

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY not found in .env"
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7
        )

    elif provider == "ollama":

        return ChatOllama(
            model="llama3.2",
            temperature=0.7
        )

    else:

        raise ValueError(
            f"Unknown provider: {provider}"
        )


# ==========================================
# Prompt
# ==========================================

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


# ==========================================
# Output Parser
# ==========================================

parser_output = StrOutputParser()


# ==========================================
# Create Chain
# ==========================================

def get_chain(provider):

    llm = get_llm(provider)

    return prompt | llm | parser_output


# ==========================================
# Command Line Arguments
# ==========================================

parser = argparse.ArgumentParser(
    description="Multi-Provider AI Chatbot"
)

parser.add_argument(
    "--provider",
    choices=[
        "groq",
        "gemini",
        "ollama"
    ],
    default="groq",
    help="Choose AI provider"
)

args = parser.parse_args()


# ==========================================
# Initial Provider
# ==========================================

provider = args.provider


try:

    chain = get_chain(provider)

except Exception as e:

    print(f"ERROR: {e}")
    exit()


# ==========================================
# Conversation History
# ==========================================

history = []


# ==========================================
# Start Chatbot
# ==========================================

print("=" * 45)
print("        MULTI-PROVIDER AI CHATBOT")
print("=" * 45)

print(f"Provider: {provider}")

print("\nCommands:")
print("/model              → Show current provider")
print("/model groq         → Switch to Groq")
print("/model gemini       → Switch to Gemini")
print("/model ollama       → Switch to Ollama")
print("/clear              → Clear conversation")
print("exit                → Quit chatbot")

print()


# ==========================================
# Chat Loop
# ==========================================

while True:

    try:

        user_input = input("You: ")

    except KeyboardInterrupt:

        print("\nGoodbye!")
        break


    # --------------------------------------
    # Exit
    # --------------------------------------

    if user_input.lower() == "exit":

        print("Goodbye!")
        break


    # --------------------------------------
    # Empty Input
    # --------------------------------------

    if not user_input.strip():

        continue


    # --------------------------------------
    # Show Current Provider
    # --------------------------------------

    if user_input.lower() == "/model":

        print(
            f"Current provider: {provider}\n"
        )

        continue


    # --------------------------------------
    # Switch Provider
    # --------------------------------------

    if user_input.lower().startswith("/model "):

        new_provider = user_input.split(
            " ",
            1
        )[1].strip().lower()


        if new_provider not in [
            "groq",
            "gemini",
            "ollama"
        ]:

            print(
                "Invalid provider.\n"
                "Available: groq, gemini, ollama\n"
            )

            continue


        try:

            chain = get_chain(new_provider)

            provider = new_provider

            print(
                f"Switched to {provider}\n"
            )

        except Exception as e:

            print(
                f"Could not switch provider: {e}\n"
            )

        continue


    # --------------------------------------
    # Clear Conversation
    # --------------------------------------

    if user_input.lower() == "/clear":

        history.clear()

        print(
            "Conversation history cleared.\n"
        )

        continue


    # --------------------------------------
    # AI Response
    # --------------------------------------

    print("AI: ", end="")

    full_response = ""


    try:

        for chunk in chain.stream({

            "history": history,

            "question": user_input

        }):

            print(
                chunk,
                end="",
                flush=True
            )

            full_response += chunk


        print()


    except Exception as e:

        print(
            f"\nERROR: {e}\n"
        )

        continue


    # --------------------------------------
    # Save Conversation
    # --------------------------------------

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