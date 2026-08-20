import os
import sys
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.scanner import AdvancedWebScanner
BANNER = """
 [bold red] ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██╗    ██╗███████╗██████╗ [/bold red]
 [bold red]██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██║    ██║██╔════╝██╔══██╗[/bold red]
 [bold white]██║  ███╗███████║██║   ██║███████╗   ██║        ██║ █╗ ██║█████╗  ██████╔╝[/bold white]
 [bold white]██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██║███╗██║██╔══╝  ██╔══██╗[/bold white]
 [bold blue]╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ╚███╔███╔╝███████╗██████╔╝[/bold blue]
 [bold blue] ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝   ╚══╝╚══╝ ╚══════╝╚═════╝ [/bold blue]
 [bold yellow]         Advanced Web Vulnerability Scanner & Exploit Verification[/bold yellow]
 [italic cyan]                         Ghost-SY1 Security 2026[/italic cyan]
"""
console = Console()
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
async def main():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    target = Prompt.ask("[bold yellow]Enter Target URL (e.g. target.com)[/bold yellow]")
    console.print(f"[bold cyan][*][/bold cyan] Initializing 2026 WAF Evasion Engine for target: {target}")
    scanner = AdvancedWebScanner(target)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Executing Advanced Payload Injection & WAF Bypass...", total=None)
        vulnerabilities = await scanner.scan()
    if vulnerabilities:
        t = Table(title="Discovered Critical Vulnerabilities", border_style="bold red")
        t.add_column("Type", style="cyan")
        t.add_column("Endpoint", style="white")
        t.add_column("Payload", style="yellow")
        for v in vulnerabilities:
            t.add_row(v['type'].upper(), v['endpoint'], v['payload'])
        console.print(t)
    else:
        console.print("[bold green][+][/bold green] Target is heavily hardened or no vulnerabilities found with current signatures.")
if __name__ == "__main__":
    asyncio.run(main())
