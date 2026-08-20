import os
import sys
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.scanner import UltimateWebEngine
BANNER = """
 [bold red] ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██╗    ██╗███████╗██████╗ [/bold red]
 [bold red]██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██║    ██║██╔════╝██╔══██╗[/bold red]
 [bold white]██║  ███╗███████║██║   ██║███████╗   ██║        ██║ █╗ ██║█████╗  ██████╔╝[/bold white]
 [bold white]██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██║███╗██║██╔══╝  ██╔══██╗[/bold white]
 [bold blue]╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ╚███╔███╔╝███████╗██████╔╝[/bold blue]
 [bold blue] ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝   ╚══╝╚══╝ ╚══════╝╚═════╝ [/bold blue]
 [bold yellow]         Ultimate Web Vulnerability & SSRF/LFI Scanner (2026)[/bold yellow]
 [italic cyan]                         Ghost-SY1 Security[/italic cyan]
"""
console = Console()
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
async def main():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    console.print("[bold yellow][*] Initializing Ghost-WebScanner Interactive Engine...[/bold yellow]\n")
    target = Prompt.ask("[bold cyan]Enter Target URL (e.g. target.com)[/bold cyan]")
    console.print(f"\n[bold green][*][/bold green] Executing Advanced Vulnerability Fuzzing & SSRF/LFI Checks on: {target}")
    scanner = UltimateWebEngine(target)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for SSRF, LFI, and API vulnerabilities...", total=None)
        results = await asyncio.run(scanner.scan()) if 'asyncio.run' in dir() else await scanner.scan()
    if results:
        t = Table(title="Discovered Advanced Web Vulnerabilities", border_style="bold red")
        t.add_column("Vulnerability", style="cyan")
        t.add_column("Endpoint", style="white")
        for r in results:
            t.add_row(r['vuln'], r['endpoint'])
        console.print(t)
    else:
        console.print("[bold green][+][/bold green] Target web application is heavily secured or no high-risk flaws found.")
if __name__ == "__main__":
    asyncio.run(main())
