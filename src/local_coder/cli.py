from pathlib import Path

import typer

app = typer.Typer()


@app.callback()
def main(project: Path = typer.Option(Path("."), "--project")) -> None:
    """Local CLI Coder"""

    project = project.expanduser().resolve()

    if not project.exists():
        raise typer.BadParameter("Project path does not exist")

    if not project.is_dir():
        raise typer.BadParameter("Project path must be a directory")


@app.command()
def ask(text: str) -> None:
    print(f"You asked: {text}")
