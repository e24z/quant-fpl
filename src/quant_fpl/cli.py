import typer
import asyncio
from quant_fpl.data.fpl_client import FPLClient

app = typer.Typer()

@app.command()
def fetch():
    """Fetch the raw element data frame. Output timestamped .json and .parquet. """
    client = FPLClient()
    df = asyncio.run(client.bootstrap())
    print(df)

def main():
    app()
