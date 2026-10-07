# Day 1 - Multi Provider CLI Chatbot

## Stage 1 - Raw Groq API

Learned:
- Groq Python SDK
- API authentication
- System and user messages
- API response
- Token usage

## Stage 2 - Conversation Memory

Learned:
- Python list as conversation history
- User messages
- Assistant messages
- Sending previous messages to the model

## Stage 3 - Streaming

Learned:
- stream=True
- Receiving response chunks
- Printing chunks immediately
- Saving the complete streamed response

## Stage 4 - Temperature

Tested:
- temperature = 0
- temperature = 0.7
- temperature = 1.5

Observation:

Temperature controls how predictable or varied the model's responses can be.

0:
More deterministic

0.7:
Balanced behavior

1.5:
More varied/creative behavior
