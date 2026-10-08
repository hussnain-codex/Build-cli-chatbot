import os
import json
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
# Get LLM Provider
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
# Prompt Template
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
# Create LCEL Chain
# ==========================================

def get_chain(provider):

    llm = get_llm(provider)

    return prompt | llm | parser_output


# ==========================================
# Save Conversation
# ==========================================

def save_conversation(history):

    data = []

    for message in history:

        if isinstance(message, HumanMessage):

            data.append({
                "role": "user",
                "content": message.content
            })

        elif isinstance(message, AIMessage):

            data.append({
                "role": "assistant",
                "content": message.content
            })


    with open(
        "conversation.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


    print(
        "Conversation saved to conversation.json\n"
    )


# ==========================================
# Load Conversation
# ==========================================

def load_conversation():

    if not os.path.exists("conversation.json"):

        print(
            "No saved conversation found.\n"
        )

        return []


    try:

        with open(
            "conversation.json",
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        history = []


        for message in data:

            if message["role"] == "user":

                history.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )


            elif message["role"] == "assistant":

                history.append(
                    AIMessage(
                        content=message["content"]
                    )
                )


        print(
            "Conversation loaded from conversation.json\n"
        )


        return history


    except Exception as e:

        print(
            f"Error loading conversation: {e}\n"
        )

        return []


# ==========================================
# Delete Saved Conversation
# ==========================================

def delete_conversation():

    if os.path.exists("conversation.json"):

        os.remove("conversation.json")

        print(
            "Saved conversation deleted from JSON.\n"
        )

    else:

        print(
            "No conversation.json found.\n"
        )


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
# Chatbot Header
# ==========================================

print("=" * 50)
print("           MULTI-PROVIDER AI CHATBOT")
print("=" * 50)

print(f"Current provider: {provider}")

print("\nCommands:")
print("/model              → Show current provider")
print("/model groq         → Switch to Groq")
print("/model gemini       → Switch to Gemini")
print("/model ollama       → Switch to Ollama")
print("/clear              → Clear current memory")
print("/save               → Save conversation to JSON")
print("/load               → Load conversation from JSON")
print("/delete             → Delete saved JSON only")
print("exit                → Exit chatbot")

print()


# ==========================================
# Main Chat Loop
# ==========================================

while True:

    try:

        user_input = input("You: ")

    except KeyboardInterrupt:

        print("\nGoodbye!")

        break


    # ======================================
    # Exit
    # ======================================

    if user_input.lower() == "exit":

        print("Goodbye!")

        break


    # ======================================
    # Ignore Empty Input
    # ======================================

    if not user_input.strip():

        continue


    # ======================================
    # Show Current Provider
    # ======================================

    if user_input.lower() == "/model":

        print(
            f"Current provider: {provider}\n"
        )

        continue


    # ======================================
    # Switch Provider
    # ======================================

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
                "Invalid provider."
            )

            print(
                "Available: groq, gemini, ollama\n"
            )

            continue


        try:

            new_chain = get_chain(
                new_provider
            )

            chain = new_chain

            provider = new_provider

            print(
                f"Switched to {provider}\n"
            )


        except Exception as e:

            print(
                f"Could not switch provider: {e}\n"
            )


        continue


    # ======================================
    # Clear Current Memory
    # ======================================

    if user_input.lower() == "/clear":

        history.clear()

        print(
            "Current conversation memory cleared.\n"
        )

        continue


    # ======================================
    # Save Conversation
    # ======================================

    if user_input.lower() == "/save":

        try:

            save_conversation(history)

        except Exception as e:

            print(
                f"Error saving conversation: {e}\n"
            )

        continue


    # ======================================
    # Load Conversation
    # ======================================

    if user_input.lower() == "/load":

        history = load_conversation()

        continue


    # ======================================
    # Delete JSON Only
    # ======================================

    if user_input.lower() == "/delete":

        try:

            delete_conversation()

        except Exception as e:

            print(
                f"Error deleting conversation: {e}\n"
            )

        continue


    # ======================================
    # AI Response
    # ======================================

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


    # ======================================
    # Store Conversation in Memory
    # ======================================

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