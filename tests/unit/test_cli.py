from typer.testing import CliRunner

from local_coder.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "ask" in result.stdout


def test_correct(tmp_path):
    result = runner.invoke(app, ["--project", str(tmp_path), "ask", "hi"])

    assert result.exit_code == 0
    assert "You asked: hi" in result.stdout


def test_path_wrong(tmp_path):
    missing_path = tmp_path / "Wrong_path"

    result = runner.invoke(app, ["--project", str(missing_path), "ask", "hi"])

    assert result.exit_code != 0
    assert "Project path does not exist" in result.stderr


def test_path_is_not_directory(tmp_path):
    missing_path = tmp_path / "project.txt"
    missing_path.write_text("test")

    result = runner.invoke(app, ["--project", str(missing_path), "ask", "hi"])

    assert result.exit_code != 0
    assert "Project path must be a directory" in result.stderr
