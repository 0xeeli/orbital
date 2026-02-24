import os
from google import genai
from dotenv import load_dotenv

# On charge les variables du fichier .env
load_dotenv()

# On vérifie si la clé est bien là, sinon on râle avec élégance
if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("🚨 Oups ! Il manque la GEMINI_API_KEY dans ton fichier .env.")

# Initialisation du client (il trouve la clé dans l'environnement tout seul)
client = genai.Client()

def ask_gemini(prompt: str) -> str:
    """
    Envoie un message à l'API et récupère la réponse.
    """
    try:
        # On utilise gemini-2.5-flash : rapide, efficace, parfait pour un CLI
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"❌ Aïe, court-circuit lors de la communication avec l'API : {e}"
