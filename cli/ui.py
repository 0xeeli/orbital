from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.theme import Theme
from rich.table import Table

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
        "[bold cyan]🪐 ORBITAL CLI[/bold cyan]\n"
        "────────────────────────────────────────────────────────────────────────────\n"
        "[dim]Your AI copilot in the terminal to explore your codebase, run commands,[/dim]\n"
        "[dim]and iterate on ideas without leaving the shell.[/dim]\n\n"
        "[bold]Quick commands[/bold]\n"
        "[info]▸[/info] [bold]/read[/bold] <file>       : Read and memorize a local file\n"
        "[info]▸[/info] [bold]/run[/bold] <cmd>        : Execute a shell command & analyze output\n"
        "[info]▸[/info] [bold]/clear[/bold]           : Clear screen and reset conversation context\n"
        "[info]▸[/info] [bold]/help[/bold]            : Show detailed command reference\n"
        "[info]▸[/info] [bold]/exit[/bold]            : Close the session\n\n"
        "[bold]Examples[/bold]\n"
        "[dim]• /read cli/ui.py then ask: \"How can we improve this UI?\"[/dim]\n"
        "[dim]• /run pytest and let Orbital summarize failing tests.[/dim]\n\n"
        "[dim]You can also just start typing in natural language and Orbital will respond.[/dim]"
    )
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 4), expand=True))

def show_help():
    """Displays a detailed command reference table."""
    table = Table(title="Orbital Command Reference", border_style="cyan", show_header=True, header_style="bold magenta")
    
    table.add_column("Command", style="bold cyan", no_wrap=True)
    table.add_column("Arguments", style="dim white")
    table.add_column("Description", style="white")
    table.add_column("Example", style="dim green")

    table.add_row("/read", "<file_path>", "Read and memorize a local file", "/read main.py")
    table.add_row("/run", "<command>", "Execute a shell command & analyze output", "/run ls -la")
    table.add_row("/clear", "", "Wipe chat memory & clear screen", "/clear")
    table.add_row("/help", "", "Show this help message", "/help")
    table.add_row("/exit", "", "Exit the application", "/exit")

    console.print(Panel(table, border_style="dim cyan", expand=False))

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
            panel = Panel(
                markdown_content, 
                title="🤖 [bold bright_green]Orbital[/bold bright_green]", 
                title_align="left", 
                border_style="bright_green",
                padding=(0, 1)
            )
            live.update(panel)
            
    console.print()
