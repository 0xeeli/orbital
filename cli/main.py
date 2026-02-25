import typer
from rich.prompt import Prompt
from rich.console import Console
from pathlib import Path

# Relative imports for the package to work globally
from . import api, ui

app = typer.Typer(help="Orbital: The coolest AI CLI in the galaxy.")
console = Console()

@app.command()
def chat():
    """Starts the interactive chat with Orbital."""
    console.clear()
    ui.show_welcome()

    while True:
        user_input = Prompt.ask("\n[bold magenta]You[/bold magenta]")
        
        # Magic words to quit
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("\n[bold cyan]Session closed. See you![/bold cyan] 🐧👋\n")
            break
            
        # Wipe memory command
        if user_input.lower() == "/clear":
            api.clear_history()
            console.clear()
            ui.show_welcome()
            console.print("[bold green]✨ Memory wiped! Fresh start.[/bold green]\n")
            continue
            
        # --- THE /read COMMAND ---
        if user_input.lower().startswith("/read"):
            # Extract the file path (everything after "/read ")
            file_path_str = user_input[5:].strip()
            
            if not file_path_str:
                console.print("[bold red]🚨 Oops: You need to specify a file path. Example: /read cli/main.py[/bold red]")
                continue
                
            file_path = Path(file_path_str)
            base_dir = Path.cwd().resolve() # The directory where 'orbital' was launched
            
            try:
                # Resolve absolute path (resolves ../ etc.)
                absolute_file_path = file_path.resolve(strict=True)
            except FileNotFoundError:
                console.print(f"[bold red]🚨 Oops: File '{file_path_str}' not found.[/bold red]")
                continue
            
            # Security Check 1: Is it actually a file?
            if not absolute_file_path.is_file():
                console.print(f"[bold red]🚨 Oops: '{file_path_str}' is not a valid file.[/bold red]")
                continue

            # Security Check 2: Anti-Path Traversal
            if not absolute_file_path.is_relative_to(base_dir):
                console.print("[bold red]🚨 Security Alert: Reading files outside the current directory is forbidden.[/bold red]")
                continue
                
            try:
                # Read the file content
                with open(absolute_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                # UX animation in the terminal
                console.print(f"[dim cyan]📂 Injecting '{absolute_file_path.name}' into Orbital's memory...[/dim cyan]")
                
                # The secret prompt for the AI
                prompt = (
                    f"Please read the following file named '{absolute_file_path.name}':\n\n"
                    f"```\n{file_content}\n```\n\n"
                    "Acknowledge that you have read it in one short sentence, and say you are ready to help with it."
                )
                
                # Stream the response
                response_generator = api.stream_gemini(prompt)
                ui.stream_response(response_generator)
                
            except Exception as e:
                console.print(f"[bold red]🚨 Oops: Could not read file. Error: {e}[/bold red]")
            
            continue # Back to the start of the loop to wait for the real question
        # -----------------------------
        
        # Prevent sending empty prompts to the API
        if not user_input.strip():
            continue

        # Standard chat flow
        response_generator = api.stream_gemini(user_input)
        ui.stream_response(response_generator)

if __name__ == "__main__":
    app()
