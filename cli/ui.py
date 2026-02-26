from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.theme import Theme

# Custom theme for a modern CLI experience
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "bold yellow",
    "danger": "bold red",
    "success": "bold green",
})

console = Console(theme=custom_theme)

def show_welcome():
    """Displays a sleek, modern welcome banner."""
    welcome_text = (
        "[bold cyan]🪐 Welcome to ORBITAL CLI[/bold cyan]\n"
        "─────────────────────────────────────────\n"
        "Ask anything, or use these core commands:\n\n"
        "[info]▸[/info] [bold]/read[/bold] <file>  : Analyze a local file\n"
        "[info]▸[/info] [bold]/run[/bold] <cmd>    : Execute a shell command\n"
        "[info]▸[/info] [bold]/clear[/bold]       : Wipe memory context\n"
        "[info]▸[/info] [bold]/exit[/bold]        : Close the session"
    )
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2), expand=False))

def show_error(message: str):
    """Displays errors with high visibility."""
    console.print(f"\n[danger]🚨 {message}[/danger]\n")

def show_status(message: str):
    """Displays a subtle status update."""
    console.print(f"[info]⚡ {message}[/info]")

def show_raw_output(output: str):
    """Displays raw terminal output in a dimmed panel."""
    if output.strip():
        console.print(Panel(output.strip(), title="⚙️ Raw Output", border_style="dim white", style="dim"))

def stream_response(response_generator):
    """Renders streamed text dynamically with Markdown support."""
    console.print()
    full_text = ""
    
    with Live(refresh_per_second=15, console=console) as live:
        for chunk in response_generator:
            full_text += chunk
            markdown_content = Markdown(full_text)
            # Upgraded panel with padding for better readability
            panel = Panel(
                markdown_content, 
                title="🤖 [bold bright_green]Orbital[/bold bright_green]", 
                title_align="left", 
                border_style="bright_green",
                padding=(0, 1)
            )
            live.update(panel)
            
    console.print()
