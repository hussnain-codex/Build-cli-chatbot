
"""
Multi-Provider CLI AI Chatbot

This application supports:
1. Groq — cloud-based AI
2. Google Gemini — cloud-based AI
3. Ollama — locally running AI models

Features:
- Provider selection at startup
- Runtime provider switching
- Streaming responses
- Conversation memory
- Save/load/delete conversation history
- Basic error handling
"""

import os
import sys
import json
import argparse

from dotenv import load_dotenv

# Import the correct LangChain integration for each provider.
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# These classes build the prompt and manage conversation messages.
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

# Converts the model's output into plain text.
from langchain_core.output_parsers import StrOutputParser


# =========================================================
# 1. LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load API keys from the .env file into environment variables.
# Never hardcode real API keys in the source code.
load_dotenv()


# =========================================================
# 2. CONFIGURATION
# =========================================================

# File used to save conversations between application sessions.
CONVERSATION_FILE = "conversation.json"

# Providers that users can select.
SUPPORTED_PROVIDERS = ("groq", "gemini", "ollama")


# =========================================================
# 3. INITIALIZE THE SELECTED LANGUAGE MODEL
# =========================================================

def get_llm(provider):
    """
    Create and return the LangChain chat model for a provider.

    Args:
        provider (str): 'groq', 'gemini', or 'ollama'.

    Returns:
        A configured LangChain chat model.

    Raises:
        ValueError: If an API key is missing or provider is invalid.

    Note:
        The model must be available to the selected provider.
        Ollama also needs the model downloaded locally.
    """

    # GROQ: Send requests to Groq's cloud API.
    if provider == "groq":

        # Check that the API key is available before initialization.
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError(
                "GROQ_API_KEY not found. Check your .env file."
            )

        # IMPORTANT: Use ChatGroq, not ChatOllama.
        return ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7,
        )

    # GEMINI: Send requests to Google's Gemini API.
    elif provider == "gemini":

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY not found. Check your .env file."
            )

        # Uses the model name suggested by your previous Gemini error.
        # If this model is unavailable to your API key, check the
        # models listed for your Google AI API account.
        return ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
        )

    # OLLAMA: Run a model through the local Ollama service.
    elif provider == "ollama":

        # A smaller model may reduce RAM requirements compared with
        # llama3.2. Download it first using: ollama pull qwen2.5:1.5b
        return ChatOllama(
            model="qwen2.5:1.5b",
            temperature=0.7,
            num_ctx=2048,
        )

    # Reject unsupported provider names.
    raise ValueError(
        f"Unknown provider: {provider}. "
        f"Choose from: {', '.join(SUPPORTED_PROVIDERS)}"
    )


# =========================================================
# 4. DEFINE THE CHAT PROMPT
# =========================================================

# The system message defines the assistant's behavior.
# MessagesPlaceholder inserts previous messages from conversation memory.
# The human message contains the user's current question.
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Answer clearly and simply."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])


# =========================================================
# 5. DEFINE THE OUTPUT PARSER
# =========================================================

# Converts the model's output into a string that can be displayed
# and stored by the application.
parser_output = StrOutputParser()


# =========================================================
# 6. CREATE THE LCEL CHAIN
# =========================================================

def get_chain(provider):
    """
    Build the processing pipeline for the selected provider.

    Workflow:
        1. Initialize the selected language model.
        2. Connect the prompt to the model.
        3. Connect the model to the output parser.

    LCEL pipeline:
        Prompt -> LLM -> String Output

    Returns:
        A runnable chain that supports streaming.
    """

    llm = get_llm(provider)

    # The pipe operator composes the three processing components.
    return prompt | llm | parser_output


# =========================================================
# 7. SAVE CONVERSATION TO JSON
# =========================================================

def save_conversation(history):
    """
    Save the current conversation to conversation.json.

    LangChain messages cannot be saved directly as ordinary JSON
    objects, so each message is converted into a role and content.

    HumanMessage -> user
    AIMessage    -> assistant
    """

    data = []

    for message in history:

        # Convert a user message into a JSON-compatible dictionary.
        if isinstance(message, HumanMessage):
            data.append({
                "role": "user",
                "content": message.content,
            })

        # Convert an AI message into a JSON-compatible dictionary.
        elif isinstance(message, AIMessage):
            data.append({
                "role": "assistant",
                "content": message.content,
            })

    # Write the converted messages to disk.
    with open(
        CONVERSATION_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Conversation saved to {CONVERSATION_FILE}\n")


# =========================================================
# 8. LOAD CONVERSATION FROM JSON
# =========================================================

def load_conversation():
    """
    Read a previously saved conversation and rebuild its history.

    Workflow:
        1. Check whether the JSON file exists.
        2. Read and parse its contents.
        3. Recreate HumanMessage and AIMessage objects.
        4. Return the restored list.

    Returns:
        A list of LangChain messages, or an empty list on failure.
    """

    # There is nothing to load if the file does not exist.
    if not os.path.exists(CONVERSATION_FILE):
        print("No saved conversation found.\n")
        return []

    try:
        with open(
            CONVERSATION_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        # Validate the basic file structure before rebuilding history.
        if not isinstance(data, list):
            raise ValueError("Conversation JSON must contain a list.")

        history = []

        for message in data:

            if not isinstance(message, dict):
                raise ValueError("Invalid message entry in JSON.")

            role = message.get("role")
            content = message.get("content")

            if not isinstance(content, str):
                raise ValueError("Message content must be text.")

            # Reconstruct the appropriate LangChain message object.
            if role == "user":
                history.append(HumanMessage(content=content))

            elif role == "assistant":
                history.append(AIMessage(content=content))

            else:
                raise ValueError(f"Unknown message role: {role}")

        print(f"Conversation loaded from {CONVERSATION_FILE}\n")
        return history

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error loading conversation: {error}\n")
        return []


# =========================================================
# 9. DELETE SAVED CONVERSATION
# =========================================================

def delete_conversation():
    """
    Delete the saved JSON file from disk.

    This does not clear the history currently held in Python memory.
    Use /clear to clear the active conversation instead.
    """

    if os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)
        print("Saved conversation deleted from JSON.\n")
    else:
        print("No conversation.json found.\n")


# =========================================================
# 10. DISPLAY AVAILABLE COMMANDS
# =========================================================

def show_help():
    """
    Display the commands available inside the chatbot.
    """

    print("\nCommands:")
    print("/help               -> Show available commands")
    print("/model              -> Show current provider")
    print("/model groq         -> Switch to Groq")
    print("/model gemini       -> Switch to Gemini")
    print("/model ollama       -> Switch to Ollama")
    print("/clear              -> Clear current memory")
    print("/save               -> Save conversation to JSON")
    print("/load               -> Load saved conversation")
    print("/delete             -> Delete saved JSON only")
    print("exit                -> Exit chatbot\n")


# =========================================================
# 11. HANDLE SLASH COMMANDS
# =========================================================

def handle_command(user_input, state):
    """
    Process a slash command.

    Args:
        user_input (str): The command entered by the user.
        state (dict): The current provider, chain, and history.

    Returns:
        True if a command was handled; False for normal messages.

    The shared state dictionary lets commands update the active
    chain, provider, or conversation history.
    """

    command = user_input.strip()

    # Show help without sending the command to the AI model.
    if command.lower() == "/help":
        show_help()
        return True

    # Display the active provider.
    if command.lower() == "/model":
        print(f"Current provider: {state['provider']}\n")
        return True

    # Switch provider while preserving the existing conversation.
    if command.lower().startswith("/model "):

        new_provider = command.split(maxsplit=1)[1].strip().lower()

        if new_provider not in SUPPORTED_PROVIDERS:
            print(
                "Invalid provider. Available: "
                + ", ".join(SUPPORTED_PROVIDERS)
                + "\n"
            )
            return True

        try:
            # Build the new chain first. If initialization fails,
            # the current provider and chain remain unchanged.
            new_chain = get_chain(new_provider)

            state["chain"] = new_chain
            state["provider"] = new_provider

            print(f"Switched to {new_provider}\n")

        except Exception as error:
            print(f"Could not switch provider: {error}\n")

        return True

    # Clear the active in-memory conversation.
    if command.lower() == "/clear":
        state["history"].clear()
        print("Current conversation memory cleared.\n")
        return True

    # Save the current conversation.
    if command.lower() == "/save":
        try:
            save_conversation(state["history"])
        except OSError as error:
            print(f"Error saving conversation: {error}\n")
        return True

    # Replace the current history with the saved conversation.
    if command.lower() == "/load":
        state["history"] = load_conversation()
        return True

    # Delete the saved file without changing current memory.
    if command.lower() == "/delete":
        try:
            delete_conversation()
        except OSError as error:
            print(f"Error deleting conversation: {error}\n")
        return True

    # Unknown slash commands should not accidentally go to the AI.
    if command.startswith("/"):
        print("Unknown command. Type /help to see available commands.\n")
        return True

    # This is not a command; the caller should process it as a question.
    return False


# =========================================================
# 12. STREAM THE AI RESPONSE
# =========================================================

def generate_response(chain, history, user_input):
    """
    Send a question and conversation history through the LCEL chain.

    The model's output is streamed in chunks. Each chunk is printed
    immediately and accumulated into one complete response.

    Returns:
        The complete response string on success, or None on failure.

    A failed response is not added to conversation history.
    """

    print("AI: ", end="", flush=True)
    full_response = ""

    try:
        # Supply the prior conversation and current question to the prompt.
        inputs = {
            "history": history,
            "question": user_input,
        }

        # stream() yields output chunks as they become available.
        for chunk in chain.stream(inputs):
            print(chunk, end="", flush=True)
            full_response += chunk

        print()
        return full_response

    except Exception as error:
        print(f"\nERROR: {error}\n")
        return None


# =========================================================
# 13. MAIN APPLICATION
# =========================================================

def main():
    """
    Run the chatbot.

    This function coordinates:
        - Command-line arguments
        - Initial provider setup
        - Interactive input
        - Slash commands
        - Streaming AI responses
        - Conversation history updates
    """

    # Read the initial provider from the command line.
    argument_parser = argparse.ArgumentParser(
        description="Multi-Provider AI Chatbot"
    )

    argument_parser.add_argument(
        "--provider",
        choices=SUPPORTED_PROVIDERS,
        default="groq",
        help="Choose the initial AI provider",
    )

    args = argument_parser.parse_args()
    provider = args.provider

    # Initialize the selected model and its LCEL chain.
    try:
        chain = get_chain(provider)
    except Exception as error:
        print(f"Could not initialize {provider}: {error}")
        sys.exit(1)

    # Store the current provider, chain, and messages together.
    # Runtime provider switching updates this state.
    state = {
        "provider": provider,
        "chain": chain,
        "history": [],
    }

    # Display the application header and command list.
    print("=" * 50)
    print("           MULTI-PROVIDER AI CHATBOT")
    print("=" * 50)
    print(f"Current provider: {state['provider']}")
    show_help()

    # Keep accepting input until the user exits.
    while True:

        try:
            user_input = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        # Ignore empty input instead of sending it to the model.
        if not user_input:
            continue

        # Exit without making another AI request.
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Handle commands before processing normal AI questions.
        if handle_command(user_input, state):
            continue

        # Generate a streamed answer using the active chain.
        response = generate_response(
            state["chain"],
            state["history"],
            user_input,
        )

        # Update memory only if generation succeeded.
        if response is not None:
            state["history"].append(
                HumanMessage(content=user_input)
            )

            state["history"].append(
                AIMessage(content=response)
            )


# =========================================================
# 14. APPLICATION ENTRY POINT
# =========================================================

# This guard prevents main() from running automatically if this
# file is imported into another Python module.
if __name__ == "__main__":
    main()