import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("🚨 Oops! GEMINI_API_KEY is missing in your .env file.")

client = genai.Client()

# --- THE ORBITAL DIRECTORY ---
ORBITAL_DIR = Path.home() / ".orbital"
HISTORY_FILE = ORBITAL_DIR / "history.json"

# Create the hidden directory if it doesn't exist
ORBITAL_DIR.mkdir(parents=True, exist_ok=True)

# The System Prompt in English
system_prompt = (
    "You are Orbital, an expert AI developer and terminal assistant "
    "powered by Gemini. You are currently running in a CLI interface on Debian Linux. "
    "You are talking to a developer, you are precise, technical, and you always "
    "format your responses with elegant Markdown."
)

def load_history():
    """Loads chat history from the JSON file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [{"role": item["role"], "parts": [{"text": item["text"]}]} for item in data]
        except Exception:
            return []
    return []

def save_message(role: str, text: str):
    """Appends a new message to the local JSON history."""
    try:
        current_history = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                current_history = json.load(f)
        
        current_history.append({"role": role, "text": text})
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(current_history, f, indent=4, ensure_ascii=False)
    except Exception:
        pass # Silence is golden in CLI errors for non-critical features

# Initialize session with memory
chat_session = client.chats.create(
    model='gemini-2.5-flash',
    history=load_history(),
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.7, 
    )
)

def stream_gemini(prompt: str):
    """Streams the response and saves to history."""
    save_message("user", prompt)
    
    full_response = ""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                yield chunk.text
        
        if full_response:
            save_message("model", full_response)
    except Exception as e:
        yield f"❌ API short-circuit: {e}"

def clear_history():
    """Wipes the local history and resets the active session."""
    global chat_session
    
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
        
    chat_session = client.chats.create(
        model='gemini-2.5-flash',
        history=[],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7, 
        )
    )
