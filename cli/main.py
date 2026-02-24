import typer
from rich.prompt import Prompt
from rich.console import Console

# On importe nos propres modules
from cli import api, ui

app = typer.Typer(help="Le CLI Gemini le plus stylé de la galaxie.")
console = Console()

@app.command()
def chat():
    """Lance la discussion interactive avec l'IA."""
    # On affiche la belle bannière
    ui.show_welcome()

    while True:
        # Le prompt stylé pour l'utilisateur
        user_input = Prompt.ask("\n[bold magenta]Toi[/bold magenta]")
        
        # Les mots magiques pour quitter
        if user_input.lower() in ["quit", "exit", "q", "quitter"]:
            console.print("\n[bold cyan]À la prochaine, boss ![/bold cyan] 👋\n")
            break
        
        # Si on appuie sur Entrée par erreur
        if not user_input.strip():
            continue

        # L'UX moderne : le spinner d'attente qui tourne
        with console.status("[bold green]L'IA fait chauffer ses neurones...[/bold green]", spinner="dots"):
            response = api.ask_gemini(user_input)

        # On affiche le rendu Markdown tout propre
        ui.show_response(response)

if __name__ == "__main__":
    app()
