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
 [bold yellow]     GHOST-WebScanner: Dedicated Web Application & API Security Specialist[/bold yellow]
 [italic cyan]                               Ghost-SY1 Security[/italic cyan]
"""

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    console.print("[bold yellow][*] Initializing GHOST-WebScanner Security Specialist...[/bold yellow]\n")
    
    target_url = Prompt.ask("[bold cyan]Enter Target Web URL or API Endpoint[/bold cyan]")
    
    console.print(f"\n[bold green][*][/bold green] Engaging WAF Evasion & Web Vulnerability Fuzzing on: {target_url}")
    scanner = UltimateWebEngine(target_url)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning web application for SSRF, LFI, and SQLi...", total=None)
        results = await scanner.scan()
        
    if results:
        t = Table(title=f"Discovered Web Vulnerabilities on {target_url}", border_style="bold red")
        t.add_column("Vulnerability", style="cyan")
        t.add_column("Endpoint", style="white")
        for r in results:
            t.add_row(r['vuln'], r['endpoint'])
        console.print(t)
    else:
        console.print("[bold green][+][/bold green] Target web application is heavily secured or no vulnerabilities found.")
        
    console.print(f"\n[bold green][+][/bold green] Module Focus: [bold white]Web Applications, APIs, and HTTP/S Security Only[/bold white]")

if __name__ == "__main__":
    asyncio.run(main())
