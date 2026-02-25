from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

console = Console()

def show_welcome():
    """Displays a cool welcome banner."""
    welcome_text = (
        "[bold cyan]🚀 Welcome to Gemini CLI[/bold cyan]\n"
        "[dim]Ask your questions, or type 'quit', 'exit' or 'q' to leave.[/dim]"
    )
    console.print(Panel(welcome_text, border_style="cyan", expand=False))

def stream_response(response_generator):
    """Renders streamed text dynamically with Markdown support."""
    console.print()
    full_text = ""
    
    # Le composant Live met à jour l'affichage en temps réel (15 fps)
    with Live(refresh_per_second=15, console=console) as live:
        for chunk in response_generator:
            full_text += chunk
            markdown_content = Markdown(full_text)
            panel = Panel(
                markdown_content, 
                title="🤖 [bold green]Gemini[/bold green]", 
                title_align="left", 
                border_style="green"
            )
            # On met à jour le panel avec le nouveau texte
            live.update(panel)
            
    console.print()
