from re import fullmatch
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BeforeValidator

from .excecoes import LivroNaoEncontradoError
from .modelos import ErroConsulta, Livro
from .repositorio import RepositorioLivros, obter_repositorio

roteador = APIRouter(prefix="/livros", tags=["Livros"])


def converter_id(valor: str) -> int:
    # O segmento da URL chega como texto. O formato inteiro exclui valores como "1.0".
    if fullmatch(r"[+-]?[0-9]+", valor) is None:
        raise ValueError("Informe o identificador como número inteiro.")
    return int(valor)


IdLivro = Annotated[int, Path(gt=0, description="ID do livro"), BeforeValidator(converter_id)]
Repositorio = Annotated[RepositorioLivros, Depends(obter_repositorio)]


@roteador.get("", response_model=list[Livro], summary="Listar o acervo")
def listar_livros(repositorio: Repositorio) -> list[Livro]:
    return repositorio.listar()


@roteador.get(
    "/{livro_id}",
    response_model=Livro,
    summary="Consultar um livro pelo ID",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErroConsulta, "description": "Livro não encontrado"},
    },
)
def consultar_livro(livro_id: IdLivro, repositorio: Repositorio) -> Livro:
    try:
        return repositorio.buscar_por_id(livro_id)
    except LivroNaoEncontradoError as erro:
        # A rota traduz a exceção do repositório para HTTP.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
