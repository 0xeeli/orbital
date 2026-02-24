from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

# Notre baguette magique pour tout l'affichage
console = Console()

def show_welcome():
    """Affiche une bannière d'accueil qui claque."""
    welcome_text = (
        "[bold cyan]🚀 Bienvenue dans Gemini CLI[/bold cyan]\n"
        "[dim]Pose tes questions, ou tape 'quit', 'exit' ou 'q' pour quitter.[/dim]"
    )
    console.print(Panel(welcome_text, border_style="cyan", expand=False))

def show_error(message: str):
    """Affiche les erreurs en rouge pour qu'elles sautent aux yeux."""
    console.print(f"\n[bold red]🚨 Oups :[/bold red] {message}\n")

def show_response(text: str):
    """Prend du texte brut et le rend magnifique avec le support du Markdown."""
    # On ajoute un saut de ligne pour respirer un peu
    console.print() 
    markdown_content = Markdown(text)
    console.print(Panel(markdown_content, title="🤖 [bold green]Gemini[/bold green]", title_align="left", border_style="green"))
    console.print()
