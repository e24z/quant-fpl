import typer

app = typer.Typer()

@app.command()
def fetch():
    print("Fetching bootstrap...")

def main():
    app()
