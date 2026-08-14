import pytest
from typer.testing import CliRunner
from main import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Data Reconcilier" in result.stdout
    assert "colecao" in result.stdout
    assert "divergentes" in result.stdout


def test_cli_colecao_arquivo_inexistente(tmp_path):
    arquivo_inexistente = tmp_path / "nao_existe.xlsx"
    base_inexistente = tmp_path / "base_nao_existe.xlsx"

    result = runner.invoke(app, [
        "colecao",
        "-n", "teste_erro",
        "-p", str(arquivo_inexistente),
        "-b", str(base_inexistente)
    ])

    assert result.exit_code == 1
    assert "Erro: O arquivo de modelos" in result.output


def test_cli_divergentes_arquivo_inexistente(tmp_path):
    arquivo_inexistente = tmp_path / "nao_existe.xlsx"
    base_inexistente = tmp_path / "base_nao_existe.xlsx"

    result = runner.invoke(app, [
        "divergentes",
        "-n", "teste_erro",
        "-p", str(arquivo_inexistente),
        "-b", str(base_inexistente)
    ])

    assert result.exit_code == 1
    assert "Erro: O arquivo de produtos" in result.output
