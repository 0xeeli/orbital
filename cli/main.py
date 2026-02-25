import typer
from rich.prompt import Prompt
from rich.console import Console

# L'import relatif crucial pour que ça marche une fois installé globalement
from . import api, ui

# C'est CETTE variable 'app' que la commande 'orbital' vient chercher
app = typer.Typer(help="Orbital: The coolest AI CLI in the galaxy.")
console = Console()

@app.command()
def chat():
    """Starts the interactive chat with Orbital."""
    ui.show_welcome()

    while True:
        user_input = Prompt.ask("\n[bold magenta]You[/bold magenta]")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("\n[bold cyan]Session closed. See you![/bold cyan] 🐧👋\n")
            break
        
        if not user_input.strip():
            continue

        response_generator = api.stream_gemini(user_input)
        ui.stream_response(response_generator)

if __name__ == "__main__":
    app()
