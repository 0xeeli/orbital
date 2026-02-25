from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

console = Console()

def show_welcome():
    """Displays a cool welcome banner."""
    welcome_text = (
        "[bold cyan]🚀 Welcome to Orbital CLI[/bold cyan]\n"
        "[dim]Ask your questions. Type 'quit' to leave, or '/clear' to wipe memory.[/dim]"
    )
    console.print(Panel(welcome_text, border_style="cyan", expand=False))

def show_error(message: str):
    """Displays errors in red."""
    console.print(f"\n[bold red]🚨 Oops:[/bold red] {message}\n")

def stream_response(response_generator):
    """Renders streamed text dynamically with Markdown support."""
    console.print()
    full_text = ""
    
    with Live(refresh_per_second=15, console=console) as live:
        for chunk in response_generator:
            full_text += chunk
            markdown_content = Markdown(full_text)
            panel = Panel(
                markdown_content, 
                title="🤖 [bold green]Orbital[/bold green]", 
                title_align="left", 
                border_style="green"
            )
            live.update(panel)
            
    console.print()
