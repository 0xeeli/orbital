from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def show_welcome():
    """Displays a cool welcome banner."""
    welcome_text = (
        "[bold cyan]🚀 Welcome to Gemini CLI[/bold cyan]\n"
        "[dim]Ask your questions, or type 'quit', 'exit' or 'q' to leave.[/dim]"
    )
    console.print(Panel(welcome_text, border_style="cyan", expand=False))

def show_error(message: str):
    """Displays errors in red."""
    console.print(f"\n[bold red]🚨 Oops:[/bold red] {message}\n")

def show_response(text: str):
    """Renders raw text nicely with Markdown support."""
    console.print() 
    markdown_content = Markdown(text)
    console.print(Panel(markdown_content, title="🤖 [bold green]Gemini[/bold green]", title_align="left", border_style="green"))
    console.print()
