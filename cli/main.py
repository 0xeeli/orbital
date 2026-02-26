import typer
import subprocess
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
        if user_input.lower() in ["quit", "exit", "q", "/quit", "/exit", "/q"]:
            console.print("\n[bold cyan]Session closed. See you![/bold cyan] 🐧👋\n")
            break
            
        # Wipe memory command
        if user_input.lower() == "/clear":
            api.clear_history()
            console.clear()
            ui.show_welcome()
            console.print("[bold green]✨ Memory wiped! Fresh start.[/bold green]\n")
            continue
            
        # --- THE /run COMMAND ---
        if user_input.lower().startswith("/run"):
            # Extract the command string
            command_str = user_input[4:].strip()
            
            if not command_str:
                console.print("[bold red]🚨 Oops: You need to specify a command. Example: /run ls -la[/bold red]")
                continue
                
            console.print(f"[dim cyan]⚡ Executing: '{command_str}'...[/dim cyan]")
            
            try:
                # Run the command in the shell
                result = subprocess.run(
                    command_str, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=60 # Safety: kill the process if it hangs for more than 1 minute
                )
                
                # Combine standard output and standard error
                output = result.stdout + result.stderr
                
                # Handle silent commands (like 'mkdir')
                if not output.strip():
                    output = "[Command executed successfully with no output]"
                    
                console.print("[dim cyan]🧠 Analyzing output...[/dim cyan]")
                
                # The prompt for the AI
                prompt = (
                    f"I executed the shell command: `{command_str}`\n\n"
                    f"Here is the terminal output:\n```\n{output}\n```\n\n"
                    "Please analyze this output briefly. If there are errors, explain them. "
                    "If it's successful, just acknowledge it."
                )
                
                response_generator = api.stream_gemini(prompt)
                ui.stream_response(response_generator)
                
            except subprocess.TimeoutExpired:
                console.print("[bold red]🚨 Oops: Command timed out after 60 seconds.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]🚨 Oops: Failed to execute command. Error: {e}[/bold red]")
            
            continue
        # -----------------------------

        # --- THE /read COMMAND ---
        if user_input.lower().startswith("/read"):
            file_path_str = user_input[5:].strip()
            
            if not file_path_str:
                console.print("[bold red]🚨 Oops: You need to specify a file path. Example: /read cli/main.py[/bold red]")
                continue
                
            file_path = Path(file_path_str)
            base_dir = Path.cwd().resolve()
            
            try:
                absolute_file_path = file_path.resolve(strict=True)
            except FileNotFoundError:
                console.print(f"[bold red]🚨 Oops: File '{file_path_str}' not found.[/bold red]")
                continue
            
            if not absolute_file_path.is_file():
                console.print(f"[bold red]🚨 Oops: '{file_path_str}' is not a valid file.[/bold red]")
                continue

            if not absolute_file_path.is_relative_to(base_dir):
                console.print("[bold red]🚨 Security Alert: Reading files outside the current directory is forbidden.[/bold red]")
                continue
                
            try:
                with open(absolute_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                console.print(f"[dim cyan]📂 Injecting '{absolute_file_path.name}' into Orbital's memory...[/dim cyan]")
                
                prompt = (
                    f"Please read the following file named '{absolute_file_path.name}':\n\n"
                    f"```\n{file_content}\n```\n\n"
                    "Acknowledge that you have read it in one short sentence, and say you are ready to help with it."
                )
                
                response_generator = api.stream_gemini(prompt)
                ui.stream_response(response_generator)
                
            except Exception as e:
                console.print(f"[bold red]🚨 Oops: Could not read file. Error: {e}[/bold red]")
            
            continue
        # -----------------------------
        
        if not user_input.strip():
            continue

        response_generator = api.stream_gemini(user_input)
        ui.stream_response(response_generator)

if __name__ == "__main__":
    app()
