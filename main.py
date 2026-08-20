import os
import sys
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.scanner import UltimateWebScanner

BANNER = """
 [bold red] ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██╗    ██╗███████╗██████╗ [/bold red]
 [bold red]██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██║    ██║██╔════╝██╔══██╗[/bold red]
 [bold white]██║  ███╗███████║██║   ██║███████╗   ██║        ██║ █╗ ██║█████╗  ██████╔╝[/bold white]
 [bold white]██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██║███╗██║██╔══╝  ██╔══██╗[/bold white]
 [bold blue]╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ╚███╔███╔╝███████╗██████╔╝[/bold blue]
 [bold blue] ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝   ╚══╝╚══╝ ╚══════╝╚═════╝ [/bold blue]
 [bold yellow]     GHOST-WebScanner: Elite Weaponized Web Arsenal & 1100+ DB[/bold yellow]
 [italic cyan]                               Ghost-SY1 Security[/italic cyan]
"""

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    console.print("[bold yellow][*] Initializing GHOST-WebScanner Elite Web Engine...[/bold yellow]\n")
    
    target_url = Prompt.ask("[bold cyan]Enter Target Web URL[/bold cyan]")
    
    console.print(f"\n[bold green][*][/bold green] Engaging Anti-Ban WAF Evasion & Elite Vulnerability Matching...")
    
    scanner = UltimateWebScanner(target_url)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning and matching 1100+ weaponized web vulnerabilities...", total=None)
        results = await scanner.run()
        
    if results:
        t = Table(title=f"Discovered Critical Web Vulnerabilities on {target_url}", border_style="bold red")
        t.add_column("CVE ID", style="cyan")
        t.add_column("Product", style="white")
        t.add_column("Reliability", style="bold green")
        t.add_column("Status", style="bold red")
        
        # In this professional view, we fetch the first match's detail for demonstration
        for r in results[:5]:
            # Fetch from DB for more detail
            match = next((v for v in scanner.vulnerabilities if v['cve'] == r['cve']), None)
            reliability = f"{match['reliability_score']}/10" if match else "9.0/10"
            t.add_row(r['cve'], r['product'], reliability, r['status'])
        console.print(t)
    else:
        console.print("[bold green][+][/bold green] Target web application is heavily secured or no critical flaws found.")

if __name__ == "__main__":
    asyncio.run(main())
