#!/usr/bin/env python3

import sys
import json
import requests
import os

# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# Define the chat history file path
CHAT_HISTORY_FILE = "chat_history.txt"

# Load the chat history from file
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            chat_history = json.load(f)
    except:
        chat_history = []

    return chat_history

# Save the chat history to file
def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chat_history, f)

# Define the function that sends a request to the OpenAI API
def openai_chat(prompt, messages_role="user"):
    if not prompt:
        print("Please provide a prompt as the first argument.")
        return None

    # Load the chat history and append the new message
    chat_history = load_chat_history()
    chat_history.append({"prompt": prompt, "role": messages_role})

    # Set up the request to the OpenAI API
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "messages": [
            {
                "role": messages_role,
                "content": prompt
            }
        ]
    }

    # Send the request to the OpenAI API and store the response in a variable
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']

    # Update the chat history with the API response
    chat_history[-1]["response"] = content

    # Save the chat history to file
    save_chat_history(chat_history)

    print(content)

    return content


# Call the function with the command line arguments
if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else None
    messages_role = sys.argv[2] if len(sys.argv) > 2 else "user"
    openai_chat(prompt, messages_role)
