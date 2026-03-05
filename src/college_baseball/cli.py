"""Command-line interface using Typer."""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from college_baseball import __version__
from college_baseball.config import get_settings
from college_baseball.database import get_db_context, init_db
from college_baseball.loaders import DataLoader
from college_baseball.processors import SilverProcessor

app = typer.Typer(
    name="college-baseball",
    help="College Baseball Statistics CLI",
    add_completion=False,
)
console = Console()
settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold green]College Baseball Statistics v{__version__}[/bold green]")


@app.command()
def init() -> None:
    """Initialize the database with tables."""
    console.print("[bold yellow]Initializing database...[/bold yellow]")
    try:
        init_db()
        console.print("[bold green]✓ Database initialized successfully[/bold green]")
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def load(
    data_dir: Path = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Directory containing upload folders (e.g., data/)",
    ),
    folder_name: Optional[str] = typer.Option(
        None,
        "--folder",
        "-f",
        help="Specific upload folder to load (e.g., upload_02_13_2026)",
    ),
) -> None:
    """Load CSV data into bronze layer from upload folders.
    
    Looks for folders named 'upload_MM_DD_YYYY' in the data directory
    and extracts the date to use as data_date.
    """
    if data_dir is None:
        data_dir = Path("data")
    
    if not data_dir.exists():
        console.print(f"[bold red]✗ Directory not found: {data_dir}[/bold red]")
        raise typer.Exit(1)
    
    # Pattern to match upload_MM_DD_YYYY
    pattern = re.compile(r"upload_(\d{2})_(\d{2})_(\d{4})")
    
    # Find all matching folders or use specified folder
    if folder_name:
        upload_folders = [data_dir / folder_name]
        if not upload_folders[0].exists():
            console.print(f"[bold red]✗ Folder not found: {upload_folders[0]}[/bold red]")
            raise typer.Exit(1)
    else:
        upload_folders = [
            f for f in data_dir.iterdir()
            if f.is_dir() and pattern.match(f.name)
        ]
        upload_folders.sort()  # Process in chronological order
    
    if not upload_folders:
        console.print(f"[bold red]✗ No upload folders found in {data_dir}[/bold red]")
        console.print("[yellow]Expected folder format: upload_MM_DD_YYYY[/yellow]")
        raise typer.Exit(1)
    
    all_results = {}
    
    for upload_folder in upload_folders:
        # Extract date from folder name
        match = pattern.match(upload_folder.name)
        if not match:
            console.print(f"[yellow]Skipping invalid folder: {upload_folder.name}[/yellow]")
            continue
        
        month, day, year = match.groups()
        try:
            data_date = datetime(int(year), int(month), int(day))
        except ValueError as e:
            console.print(f"[yellow]Skipping folder with invalid date {upload_folder.name}: {e}[/yellow]")
            continue
        
        console.print(f"\n[bold yellow]Loading data from {upload_folder.name} (date: {data_date.date()})...[/bold yellow]")
        
        try:
            with get_db_context() as db:
                loader = DataLoader(db)
                results = loader.load_all(upload_folder, data_date)
            
            all_results[upload_folder.name] = results
            
            # Display results for this folder
            table = Table(title=f"Load Results - {upload_folder.name}")
            table.add_column("Dataset", style="cyan")
            table.add_column("Records", style="green", justify="right")
            
            for name, count in results.items():
                table.add_row(name.replace("_", " ").title(), str(count))
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[bold red]✗ Error loading {upload_folder.name}: {e}[/bold red]")
            continue
    
    if all_results:
        console.print(f"\n[bold green]✓ Successfully loaded {len(all_results)} upload folder(s)[/bold green]")
    else:
        console.print("[bold red]✗ No data was loaded[/bold red]")
        raise typer.Exit(1)


@app.command()
def process(
    all_dates: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Process all available dates, not just the latest",
    ),
) -> None:
    """Process bronze data and calculate percentiles for silver layer."""
    console.print("[bold yellow]Processing bronze data...[/bold yellow]")
    
    try:
        with get_db_context() as db:
            if all_dates:
                # Get all unique dates from bronze layer
                from sqlalchemy import select, func
                from college_baseball.models import BronzeAdvBatting
                
                dates = db.execute(
                    select(func.distinct(BronzeAdvBatting.data_date))
                    .order_by(BronzeAdvBatting.data_date)
                ).scalars().all()
                
                console.print(f"[yellow]Found {len(dates)} date(s) to process[/yellow]\n")
                
                all_results = {}
                for data_date in dates:
                    date_str = str(data_date) if isinstance(data_date, datetime) else str(data_date)
                    console.print(f"[bold cyan]Processing {date_str}...[/bold cyan]")
                    processor = SilverProcessor(db)
                    results = processor.process_all(data_date)
                    all_results[date_str] = results
                
                # Display summary
                console.print("\n[bold green]✓ All dates processed successfully[/bold green]")
                
            else:
                processor = SilverProcessor(db)
                results = processor.process_all()
            
                # Display results
                table = Table(title="Processing Results")
                table.add_column("Dataset", style="cyan")
                table.add_column("Records", style="green", justify="right")
                
                for name, count in results.items():
                    table.add_row(name.replace("_", " ").title(), str(count))
                
                console.print(table)
                console.print("[bold green]✓ Data processed successfully[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def update(
    data_dir: Path = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Directory containing CSV files",
    ),
) -> None:
    """Full update: load and process data."""
    console.print("[bold cyan]Starting full update...[/bold cyan]\n")
    
    # Load data
    load(data_dir)
    console.print()
    
    # Process data
    process()
    console.print()
    
    console.print("[bold green]✓ Full update completed successfully[/bold green]")


@app.command(name="load-and-process")
def load_and_process(
    data_dir: Path = typer.Option(
        None,
        "--data-dir",
        "-d",
        help="Directory containing upload folders (e.g., data/)",
    ),
) -> None:
    """Clear database and reload all data from scratch.
    
    This command will:
    1. Drop all tables and recreate them (fresh start)
    2. Load all data from upload folders in /data directory
    3. Process all dates into the silver layer
    """
    console.print("[bold cyan]Starting full pipeline rebuild...[/bold cyan]\n")
    
    # Step 1: Reinitialize database (clears all data)
    console.print("[bold yellow]Step 1/3: Reinitializing database...[/bold yellow]")
    try:
        from college_baseball.database import engine
        from college_baseball.models import Base
        
        # Drop all tables
        Base.metadata.drop_all(engine)
        console.print("[dim]Dropped all tables[/dim]")
        
        # Recreate all tables
        init_db()
        console.print("[bold green]✓ Database reinitialized[/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Error reinitializing database: {e}[/bold red]")
        raise typer.Exit(1)
    
    # Step 2: Load all data
    console.print("[bold yellow]Step 2/3: Loading all data from upload folders...[/bold yellow]")
    try:
        if data_dir is None:
            data_dir = Path("data")
        
        if not data_dir.exists():
            console.print(f"[bold red]✗ Directory not found: {data_dir}[/bold red]")
            raise typer.Exit(1)
        
        # Pattern to match upload_MM_DD_YYYY
        pattern = re.compile(r"upload_(\d{2})_(\d{2})_(\d{4})")
        
        upload_folders = [
            f for f in data_dir.iterdir()
            if f.is_dir() and pattern.match(f.name)
        ]
        upload_folders.sort()  # Process in chronological order
        
        if not upload_folders:
            console.print(f"[bold red]✗ No upload folders found in {data_dir}[/bold red]")
            console.print("[yellow]Expected folder format: upload_MM_DD_YYYY[/yellow]")
            raise typer.Exit(1)
        
        all_results = {}
        
        for upload_folder in upload_folders:
            # Extract date from folder name
            match = pattern.match(upload_folder.name)
            if not match:
                console.print(f"[yellow]Skipping invalid folder: {upload_folder.name}[/yellow]")
                continue
            
            month, day, year = match.groups()
            try:
                data_date = datetime(int(year), int(month), int(day))
            except ValueError as e:
                console.print(f"[yellow]Skipping folder with invalid date {upload_folder.name}: {e}[/yellow]")
                continue
            
            console.print(f"\n[bold yellow]Loading data from {upload_folder.name} (date: {data_date.date()})...[/bold yellow]")
            
            try:
                with get_db_context() as db:
                    loader = DataLoader(db)
                    results = loader.load_all(upload_folder, data_date)
                
                all_results[upload_folder.name] = results
                
                # Display results for this folder
                table = Table(title=f"Load Results - {upload_folder.name}")
                table.add_column("Dataset", style="cyan")
                table.add_column("Records", style="green", justify="right")
                
                for name, count in results.items():
                    table.add_row(name.replace("_", " ").title(), str(count))
                
                console.print(table)
                
            except Exception as e:
                console.print(f"[bold red]✗ Error loading {upload_folder.name}: {e}[/bold red]")
                continue
        
        if all_results:
            console.print(f"\n[bold green]✓ Successfully loaded {len(all_results)} upload folder(s)[/bold green]")
        else:
            console.print("[bold red]✗ No data was loaded[/bold red]")
            raise typer.Exit(1)
        
        console.print()
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Error loading data: {e}[/bold red]")
        raise typer.Exit(1)
    
    # Step 2.5: Remove duplicates
    console.print("[bold yellow]Step 2.5/3: Removing duplicate records...[/bold yellow]")
    try:
        with get_db_context() as db:
            loader = DataLoader(db)
            dup_results = loader.remove_duplicates()
            
            # Display deduplication results
            table = Table(title="Duplicates Removed")
            table.add_column("Table", style="cyan")
            table.add_column("Removed", style="yellow", justify="right")
            
            total_removed = 0
            for table_name, count in dup_results.items():
                table.add_row(table_name.replace("_", " ").title(), str(count))
                total_removed += count
            
            console.print(table)
            
            if total_removed > 0:
                console.print(f"[bold green]✓ Removed {total_removed} duplicate record(s)[/bold green]\n")
            else:
                console.print(f"[bold green]✓ No duplicates found[/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Error removing duplicates: {e}[/bold red]")
        raise typer.Exit(1)
    
    # Step 3: Process all dates
    console.print("[bold yellow]Step 3/3: Processing all dates...[/bold yellow]")
    try:
        with get_db_context() as db:
            # Get all unique dates from bronze layer
            from sqlalchemy import select, func
            from college_baseball.models import BronzeAdvBatting
            
            dates = db.execute(
                select(func.distinct(BronzeAdvBatting.data_date))
                .order_by(BronzeAdvBatting.data_date)
            ).scalars().all()
            
            console.print(f"[yellow]Found {len(dates)} date(s) to process[/yellow]\n")
            
            all_results = {}
            for data_date in dates:
                date_str = str(data_date) if isinstance(data_date, datetime) else str(data_date)
                console.print(f"[bold cyan]Processing {date_str}...[/bold cyan]")
                processor = SilverProcessor(db)
                results = processor.process_all(data_date)
                all_results[date_str] = results
            
            # Display summary
            console.print("\n[bold green]✓ All dates processed successfully[/bold green]")
        
        console.print()
    except Exception as e:
        console.print(f"[bold red]✗ Error processing data: {e}[/bold red]")
        raise typer.Exit(1)
    
    console.print("[bold green]✓ Full pipeline completed successfully![/bold green]")
    console.print("[dim]Database has been rebuilt with all data from /data folder[/dim]")


@app.command()
def serve(
    host: str = typer.Option(None, "--host", "-h", help="API host"),
    port: int = typer.Option(None, "--port", "-p", help="API port"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
) -> None:
    """Start the FastAPI server."""
    import uvicorn
    
    host = host or settings.api_host
    port = port or settings.api_port
    reload = reload or settings.api_reload
    
    console.print(f"[bold cyan]Starting API server on {host}:{port}...[/bold cyan]")
    
    uvicorn.run(
        "college_baseball.api:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
