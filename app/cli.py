import typer
from tasks.freshdesk_pipeline import run_freshdesk_pipeline
import subprocess

app = typer.Typer()


@app.command()
def fetch():
    """Récupère les tickets Freshdesk (demande initiale uniquement)."""
    run_freshdesk_pipeline()
    typer.echo("✅ Tickets Freshdesk enregistrés.")

@app.command()
def analyze():
    """Lance l’analyse GPT sur les tickets Freshdesk."""
    subprocess.run(["python", "run_analyze.py"], check=True)
    typer.echo("✅ Analyse GPT terminée.")

@app.command()
def all():
    """Exécute l'extraction + analyse GPT d'un coup."""
    run_freshdesk_pipeline()
    subprocess.run(["python", "run_analyze.py"], check=True)
    typer.echo("✅ Pipeline complet exécuté.")


if __name__ == "__main__":
    app()
