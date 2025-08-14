import typer
import asyncio
from quant_fpl.data.fpl_client import FPLClient
from quant_fpl.data.tidy import tidy_payload
from quant_fpl.data.greedy_picker import assert_squad_constraints

app = typer.Typer()

@app.command()
def fetch():
    """Fetch the raw element DataFrame. Output timestamped .json and .parquet. """
    client = FPLClient()
    df = asyncio.run(client.bootstrap())
    print(df)

@app.command()
def tidy():
    """Return a tidied view of the element DataFrame"""
    client = FPLClient()
    payload = asyncio.run(client.bootstrap_payload())
    df = tidy_payload(payload)
    print(df.head(10).to_string(index=False))

@app.command()
def check():
    """assert that the tidied view conforms to squad constraints"""
    client = FPLClient()
    payload = asyncio.run(client.bootstrap_payload())
    df = tidy_payload(payload)
    assert_squad_constraints(df.head(15))

def main():
    app()
