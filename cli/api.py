import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("🚨 Oops! GEMINI_API_KEY is missing in your .env file.")

client = genai.Client()

# The System Prompt in English
system_prompt = (
    "You are Orbital, an expert AI developer and terminal assistant "
    "powered by Gemini. You are currently running in a CLI interface on Debian Linux. "
    "You are talking to a developer, you are precise, technical, and you always "
    "format your responses with elegant Markdown."
)

chat_session = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.7, 
    )
)

def stream_gemini(prompt: str):
    """Streams the response from the active chat session."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"❌ API short-circuit: {e}"
