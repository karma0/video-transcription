import click
from datetime import timedelta


def print_info(message):
    """Print info message in blue."""
    click.echo(click.style(message, fg='blue'))


def print_success(message):
    """Print success message in green."""
    click.echo(click.style(message, fg='green'))


def print_error(message):
    """Print error message in red."""
    click.echo(click.style(message, fg='red', err=True))


def print_warning(message):
    """Print warning message in yellow."""
    click.echo(click.style(message, fg='yellow'))


def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = td.total_seconds() % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')