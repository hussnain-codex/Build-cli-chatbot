
# Import os to access environment variables
import os

# Import load_dotenv to load API keys from the .env file
from dotenv import load_dotenv

# Import Groq to connect with the Groq AI API
from groq import Groq


# Load environment variables from the .env file
load_dotenv()

# Get the Groq API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Check whether the API key exists
if not api_key:
    print("ERROR: GROQ_API_KEY not found")
    exit()

# Create a Groq client using the API key
client = Groq(api_key=api_key)


# Store the conversation messages
# The system message defines the AI assistant's behavior
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]


# Display the chatbot startup message
print("AI Chatbot Started!")
print("Type 'exit' to quit.\n")


# Keep the chatbot running until the user types 'exit'
while True:

    # Get input from the user
    user_input = input("You: ")

    # Stop the chatbot if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add the user's message to the conversation history
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Keep the system prompt and the last 10 conversation messages
    # This helps limit the amount of conversation sent to the API
    # The system prompt is always preserved
    recent_messages = [messages[0]] + messages[1:][-10:]

    # Send the conversation to the Groq API
    # stream=True allows the response to arrive in small chunks
    # temperature=0.7 controls response randomness
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=recent_messages,
        stream=True,
        temperature=0.7
    )

    # Print the AI response on the same line
    print("AI: ", end="")

    # Create an empty string to store the complete AI response
    assistant_response = ""

    # Receive the streamed response chunk by chunk
    for chunk in response:

        # Extract the text from the current chunk
        content = chunk.choices[0].delta.content

        # Check that the chunk contains text
        if content:
            # Display the text immediately without waiting for the full answer
            print(content, end="", flush=True)

            # Add the current chunk to the complete response
            assistant_response += content

    # Move to the next line after the AI finishes responding
    print()

    # Save the AI response in conversation history
    # The chatbot can use it to understand future questions
    messages.append({
        "role": "assistant",
        "content": assistant_response
    })