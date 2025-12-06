from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print("\n[bold green]=== FoodGuard UK — Prototype Run ===[/bold green]\n")

# Signals table
signals_table = Table(title="Input Signals", show_header=True, header_style="bold cyan")
signals_table.add_column("Signal")
signals_table.add_column("Value")
for k, v in signals.items():
    signals_table.add_row(k, str(v))
console.print(signals_table)

# Risk panel
console.print(Panel.fit(
    f"[bold yellow]Risk Score:[/bold yellow] {result['risk']['risk_score']}\n"
    f"[bold yellow]Risk Level:[/bold yellow] {result['risk']['risk_level']}",
    title="Risk Assessment",
    border_style="yellow"
))

# Policy
policy = result["policy"]
console.print(Panel.fit(
    f"[bold white]Action:[/bold white] {policy['action']}\n"
    f"[bold white]Rationale:[/bold white] {policy['rationale']}",
    title="LLM Policy Recommendation",
    border_style="white"
))

# Neo execution (if any)
if result["neo_execution"]:
    neo = result["neo_execution"]
    console.print(Panel.fit(
        f"[bold green]TXID:[/bold green] {neo['txid']}\n"
        f"[bold green]Recipient:[/bold green] {neo['recipient']}\n"
        f"[bold green]Amount:[/bold green] {neo['amount']}",
        title="Neo Voucher Issuance (Simulated)",
        border_style="green"
    ))
else:
    console.print(Panel.fit(
        "[bold red]No voucher issued.[/bold red]",
        title="Neo Voucher Result",
        border_style="red"
    ))
