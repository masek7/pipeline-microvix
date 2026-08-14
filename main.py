from pathlib import Path
from typing_extensions import Annotated
import typer

from entrypoints.fluxo_colecao import executar_fluxo_colecao
from entrypoints.fluxo_divergentes import executar_fluxo_divergentes
from infra.log_config import setup_logging

app = typer.Typer(
    help="Data Reconcilier — Pipeline de validação e conciliação de produtos MICROVIX x EMPRESA."
)


@app.command("colecao")
def comando_colecao(
    nome_arquivo: Annotated[
        str,
        typer.Option(
            ...,
            "--nome-arquivo",
            "-n",
            help="Nome base para os arquivos gerados e arquivo de log."
        )
    ],
    caminho_planilha_modelos: Annotated[
        Path,
        typer.Option(
            ...,
            "--caminho-planilha-modelos",
            "-p",
            help="Caminho do arquivo Excel (.xlsx) contendo os modelos da coleção."
        )
    ],
    caminho_base_microvix: Annotated[
        Path,
        typer.Option(
            ...,
            "--caminho-base-microvix",
            "-b",
            help="Caminho do arquivo Excel (.xlsx) com a base espelho da Microvix."
        )
    ]
) -> None:
    """
    Executa o fluxo completo de validação de coleção por Modelo.
    Busca os dados no Oracle, trata divergências, deduplica e calcula o diff contra a Microvix.
    """
    setup_logging(nome_arquivo=nome_arquivo)
    executar_fluxo_colecao(
        nome_arquivo=nome_arquivo,
        caminho_planilha_modelos=caminho_planilha_modelos,
        caminho_base_microvix=caminho_base_microvix
    )


@app.command("divergentes")
def comando_divergentes(
    nome_arquivo: Annotated[
        str,
        typer.Option(
            ...,
            "--nome-arquivo",
            "-n",
            help="Nome base para os arquivos gerados e arquivo de log."
        )
    ],
    caminho_planilha_produtos: Annotated[
        Path,
        typer.Option(
            ...,
            "--caminho-planilha-produtos",
            "-p",
            help="Caminho da planilha de produtos com divergências (ex: a_verificar.xlsx)."
        )
    ],
    caminho_base_microvix: Annotated[
        Path,
        typer.Option(
            ...,
            "--caminho-base-microvix",
            "-b",
            help="Caminho do arquivo Excel (.xlsx) com a base espelho da Microvix."
        )
    ]
) -> None:
    """
    Executa o fluxo de conciliação direta para a planilha de produtos divergentes.
    """
    setup_logging(nome_arquivo=nome_arquivo)
    executar_fluxo_divergentes(
        nome_arquivo=nome_arquivo,
        caminho_planilha_produtos=caminho_planilha_produtos,
        caminho_base_microvix=caminho_base_microvix
    )


if __name__ == "__main__":
    app()