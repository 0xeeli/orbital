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
        # Sleeker prompt
        user_input = Prompt.ask("\n[bold magenta]❯ You[/bold magenta]")
        
        # Magic words to quit
        if user_input.lower() in ["quit", "exit", "q", "/quit", "/exit", "/q"]:
            console.print("\n[bold cyan]Session closed. See you in orbit! 🐧👋[/bold cyan]\n")
            break
            
        # Wipe memory command
        if user_input.lower() == "/clear":
            api.clear_history()
            console.clear()
            ui.show_welcome()
            ui.show_status("Memory wiped! Fresh start.")
            continue
            
        # --- THE /run COMMAND ---
        if user_input.lower().startswith("/run"):
            command_str = user_input[4:].strip()
            
            if not command_str:
                ui.show_error("You need to specify a command. Example: /run ls -la")
                continue
                
            ui.show_status(f"Executing: '{command_str}'...")
            
            try:
                result = subprocess.run(
                    command_str, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=60
                )
                
                output = result.stdout + result.stderr
                
                if not output.strip():
                    output = "[Command executed successfully with no output]"
                    
                # Display the raw output in a nice panel before analyzing
                ui.show_raw_output(output)
                ui.show_status("Analyzing output...")
                
                prompt = (
                    f"I executed the shell command: `{command_str}`\n\n"
                    f"Here is the terminal output:\n```\n{output}\n```\n\n"
                    "Please analyze this output briefly. If there are errors, explain them. "
                    "If it's successful, just acknowledge it."
                )
                
                response_generator = api.stream_gemini(prompt)
                ui.stream_response(response_generator)
                
            except subprocess.TimeoutExpired:
                ui.show_error("Command timed out after 60 seconds.")
            except Exception as e:
                ui.show_error(f"Failed to execute command. Error: {e}")
            
            continue
        # -----------------------------

        # --- THE /read COMMAND ---
        if user_input.lower().startswith("/read"):
            file_path_str = user_input[5:].strip()
            
            if not file_path_str:
                ui.show_error("You need to specify a file path. Example: /read cli/main.py")
                continue
                
            file_path = Path(file_path_str)
            base_dir = Path.cwd().resolve()
            
            try:
                absolute_file_path = file_path.resolve(strict=True)
            except FileNotFoundError:
                ui.show_error(f"File '{file_path_str}' not found.")
                continue
            
            if not absolute_file_path.is_file():
                ui.show_error(f"'{file_path_str}' is not a valid file.")
                continue

            if not absolute_file_path.is_relative_to(base_dir):
                ui.show_error("Security Alert: Reading files outside the current directory is forbidden.")
                continue
                
            try:
                with open(absolute_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                ui.show_status(f"Injecting '{absolute_file_path.name}' into Orbital's memory...")
                
                prompt = (
                    f"Please read the following file named '{absolute_file_path.name}':\n\n"
                    f"```\n{file_content}\n```\n\n"
                    "Acknowledge that you have read it in one short sentence, and say you are ready to help with it."
                )
                
                response_generator = api.stream_gemini(prompt)
                ui.stream_response(response_generator)
                
            except Exception as e:
                ui.show_error(f"Could not read file. Error: {e}")
            
            continue
        # -----------------------------
        
        if not user_input.strip():
            continue

        # Standard chat flow
        response_generator = api.stream_gemini(user_input)
        ui.stream_response(response_generator)

if __name__ == "__main__":
    app()
