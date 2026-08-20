import os
import sys
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.crawler import DeepWebCrawler
from core.js_analyzer import JSDeepAnalyzer
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

def show_help():
    help_text = """
[bold yellow]GHOST-WebScanner Help Menu[/bold yellow]

[bold cyan]Description:[/bold cyan]
Specialized web security scanner for deep crawling, JS analysis, and CVE matching.

[bold cyan]Features:[/bold cyan]
1. [bold white]Deep Crawler[/bold white]: Automatically discovers all website paths.
2. [bold white]JS Analyzer[/bold white]: Extracts secrets and hidden endpoints from JS files.
3. [bold white]Vulnerability Matcher[/bold white]: Links target tech stack to 1100+ weaponized CVEs.

[bold cyan]Usage:[/bold cyan]
Run the script and enter the target URL when prompted.
"""
    console.print(Panel(help_text, title="Help & Documentation", border_style="blue"))

async def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return

    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    
    # Explicit Database Check
    db_path = os.path.join(os.path.dirname(__file__), 'db/vulnerabilities.json')
    if os.path.exists(db_path):
        with open(db_path, 'r') as f:
            db_size = len(json.load(f))
        console.print(f"[bold green][*] Successfully loaded web vulnerability database with {db_size} entries.[/bold green]")
    else:
        console.print("[bold red][!] Warning: Web vulnerability database not found![/bold red]")

    console.print("[bold yellow][*] Initializing GHOST-WebScanner Elite Web Engine...[/bold yellow]\n")
    
    target_url = Prompt.ask("[bold cyan]Enter Target Web URL[/bold cyan]")
    
    console.print(f"\n[bold green][*][/bold green] Executing Automated Deep Crawling on: {target_url}")
    crawler = DeepWebCrawler(target_url)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Crawling endpoints and extracting JavaScript files...", total=None)
        crawl_results = await crawler.run()
        
    console.print(f"[bold green][+][/bold green] Discovered [bold white]{len(crawl_results['endpoints'])}+[/bold white] endpoints and [bold white]{len(crawl_results['js_files'])}+[/bold white] JS files.")
    
    # Rest of the scanning logic...
    scanner = UltimateWebScanner(target_url)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Matching weaponized CVEs against target tech stack...", total=None)
        results = await scanner.run()
    
    if results:
        t = Table(title=f"Critical Findings for {target_url}", border_style="bold red")
        t.add_column("CVE ID", style="cyan")
        t.add_column("Product", style="white")
        t.add_column("Status", style="bold red")
        for r in results[:5]:
            t.add_row(r['cve'], r['product'], r['status'])
        console.print(t)

if __name__ == "__main__":
    asyncio.run(main())
