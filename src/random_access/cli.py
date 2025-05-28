import click
import uvicorn
from random_access.main import app

@click.group()
def cli():
    """Random Access Server CLI."""
    pass

@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to.")
@click.option("--port", default=8000, help="Port to bind to.")
def run(host, port):
    """Run the FastAPI app."""
    uvicorn.run(app, host=host, port=port)
