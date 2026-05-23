from rich.console import Console 
from rich.panel import Panel 
from rich.markdown import Markdown 
from rich import print as rprint 
from rich import print as rprint 

# One global console - Rich
console = Console()

def show_welcome(model: str, system_prompt: str) -> None:
    """ Print the welcome banner when the chtbot starts.""" 
    
    welcome_text = (
        f"[bold purple]Model:[/bold purple] {model}\n"
        f"[bold purple]Persona:[/bold purple] {system_prompt[:80]}...\n\n"
        "[dim]Commands: type [bold]quit[/bold] to stop, [bold]clear[/bold] to reset memory [/dim]"
        
    )
    
    console.print(
        Panel(
            welcome_text,
            title="[bold]Mentor Chatbot[/bold]",
            subtitle="[dim]Powered by Groq + Llama[/dim]",
            border_style="purple",
            padding=(1, 2),
        )
    )
    console.print()
    
def get_user_input() -> str:
    """ 
    Show the user prompt and their input. 
    Returns the raw string they typed (stripped of whitespace).
    """
    
    try:
        # Rich markup: [bold cyan]You[/bold cyan] makes "You" bold cyan
        user_input = console.input("[bold cyan]You[/bold cyan] › ")
        return user_input.strip()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C  or Ctrl+D -> treat as "exit" 
        return "exit"
    
def show_assistant_streaming(client, memory) -> str:
    """ 
    Print the assistant label, then stream the reply token by token.
    Returnsthe full reply text when done (so we can save it to memory).
    """ 
    
    console.print()
    console.print("[bold green]Assistant[/bold green] › ", end="")
    full_reply = client.send_streaming(memory)
    
    console.print()
    console.print()
    
    return full_reply

   
    
def show_info(message: str) -> None:
    """Show a dimmed info/status message.""" 
    console.print(f"[dim]{message}[/dim]")
    
def show_error(message: str) -> None:
    """Show a red error message.""" 
    console.print(f"[bold red]Error:[/bold red] {message}")
    
def show_goodbye() -> None:
    """Say goodby when the user exits."""
    console.print()
    console.print("[dim]Goodbye! Session ended.[/dim]")
    console.print()