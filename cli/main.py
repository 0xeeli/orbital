import typer
from rich.prompt import Prompt
from rich.console import Console

from cli import api, ui

app = typer.Typer(help="The coolest Gemini CLI in the galaxy.")
console = Console()

@app.command()
def chat():
    """Starts the interactive chat with the AI."""
    ui.show_welcome()

    while True:
        user_input = Prompt.ask("\n[bold magenta]You[/bold magenta]")
        
        # The magic words to quit
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("\n[bold cyan]Session closed. See you![/bold cyan] 🐧👋\n")
            break
        
        if not user_input.strip():
            continue

        # The modern UX: waiting spinner
        with console.status("[bold green]AI is thinking...[/bold green]", spinner="dots"):
            response = api.ask_gemini(user_input)

        ui.show_response(response)

if __name__ == "__main__":
    app()
