import os
import sys
import argparse
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from core.recon import ReconModule
from modules.vuln_scanner import VulnScanner
from utils.reporter import Reporter
BANNER = """
 [bold red] ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ███████╗██╗   ██╗ ██╗[/bold red]
 [bold red]██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██╔════╝╚██╗ ██╔╝███║[/bold red]
 [bold white]██║  ███╗███████║██║   ██║███████╗   ██║        ███████╗ ╚████╔╝ ╚██║[/bold white]
 [bold white]██║   ██║██╔══██║██║   ██║╚════██║   ██║        ╚════██║  ╚██╔╝   ██║[/bold white]
 [bold blue]╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ███████║   ██║    ██║[/bold blue]
 [bold blue] ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚══════╝   ╚═╝    ╚═╝[/bold blue]
 [bold yellow]             Advanced Web Security & Recon Suite[/bold yellow]
 [italic cyan]                    Developed by Ghost-SY1[/italic cyan]
"""
console = Console()
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def display_banner():
    clear_screen()
    console.print(Panel(BANNER, border_style="bold red", expand=False))
async def run_scan(target):
    console.print(f"\n[bold green][+][/bold green] Initializing scan for: [bold cyan]{target}[/bold cyan]\n")
    recon = ReconModule(target)
    vuln = VulnScanner(target)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Performing Reconnaissance...", total=None)
        recon_results = await recon.run()
        progress.add_task(description="Scanning for Vulnerabilities...", total=None)
        vuln_results = await vuln.run()
        progress.add_task(description="Generating Report...", total=None)
        reporter = Reporter(target, recon_results, vuln_results)
        report_path = reporter.generate_txt_report()
    table = Table(title="Ghost-SY1 Scan Results", border_style="bold red")
    table.add_column("Category", style="cyan")
    table.add_column("Finding", style="white")
    table.add_column("Severity", style="bold red")
    table.add_row("Network", f"IP: {recon_results['ip']}", "Info")
    table.add_row("Network", f"Open Ports: {', '.join(map(str, recon_results['ports']))}", "Low")
    for v in vuln_results:
        table.add_row(v['type'], v['finding'], v['severity'])
    console.print(table)
    console.print(f"\n[bold green][+][/bold green] Scan completed. Report saved to: [bold yellow]{report_path}[/bold yellow]")
def main():
    display_banner()
    target = Prompt.ask("[bold yellow]Enter Target URL[/bold yellow]")
    if target:
        if not target.startswith("http"):
            target = "http://" + target
        asyncio.run(run_scan(target))
if __name__ == "__main__":
    main()
