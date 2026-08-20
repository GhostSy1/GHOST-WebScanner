import os
import sys
import asyncio
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
 [bold yellow]     GHOST-WebScanner: Deep Crawler, JS Analyzer & 1100+ CVE Engine[/bold yellow]
 [italic cyan]                               Ghost-SY1 Security[/italic cyan]
"""

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
    console.print("[bold yellow][*] Initializing GHOST-WebScanner Deep Recon & JS Analysis Engine...[/bold yellow]\n")
    
    target_url = Prompt.ask("[bold cyan]Enter Target Web URL[/bold cyan]")
    
    console.print(f"\n[bold green][*][/bold green] Executing Automated Deep Crawling on: {target_url}")
    crawler = DeepWebCrawler(target_url)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Crawling endpoints and extracting JavaScript files...", total=None)
        crawl_results = await asyncio.run_coroutine_threadsafe(crawler.run(), asyncio.get_event_loop()) if False else await crawler.run()
        
    console.print(f"[bold green][+][/bold green] Discovered [bold white]{len(crawl_results['endpoints'])}+[/bold white] endpoints and [bold white]{len(crawl_results['js_files'])}+[/bold white] JS files.")
    
    if crawl_results['js_files']:
        console.print(f"\n[bold green][*][/bold green] Analyzing JavaScript files for hardcoded secrets and hidden API routes...")
        js_analyzer = JSDeepAnalyzer(crawl_results['js_files'])
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Parsing JS source code for vulnerabilities and tokens...", total=None)
            js_findings = await js_analyzer.run()
            
        if js_findings:
            t = Table(title="Sensitive Findings in JavaScript Files", border_style="bold red")
            t.add_column("Finding Type", style="cyan")
            t.add_column("Source JS File", style="white")
            t.add_column("Details", style="yellow")
            for f in js_findings:
                t.add_row(f['type'], f['source'], f['detail'])
            console.print(t)
        else:
            console.print("[bold green][+][/bold green] No hardcoded secrets found in JS files.")

    console.print(f"\n[bold green][+][/bold green] Module Focus: [bold white]Deep Web Crawling, JS Source Analysis, and API Security Only[/bold white]")

if __name__ == "__main__":
    asyncio.run(main())
