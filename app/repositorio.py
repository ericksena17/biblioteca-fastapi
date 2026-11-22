from collections.abc import Iterable

from .excecoes import LivroNaoEncontradoError
from .modelos import Livro


class RepositorioLivros:
    def __init__(self, livros: Iterable[Livro]) -> None:
        # O dicionário permite buscar diretamente pelo identificador.
        self._livros = {livro.id: livro for livro in livros}

    def listar(self) -> list[Livro]:
        return list(self._livros.values())

    def buscar_por_id(self, livro_id: int) -> Livro:
        livro = self._livros.get(livro_id)
        if livro is None:
            raise LivroNaoEncontradoError(livro_id)
        return livro


_repositorio_padrao = RepositorioLivros(
    (
        Livro(
            id=1,
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            ano_publicacao=1899,
            disponivel=True,
        ),
        Livro(
            id=2,
            titulo="O Cortiço",
            autor="Aluísio Azevedo",
            ano_publicacao=1890,
            disponivel=False,
        ),
        Livro(
            id=3,
            titulo="Vidas Secas",
            autor="Graciliano Ramos",
            ano_publicacao=1938,
            disponivel=True,
        ),
        Livro(
            id=4,
            titulo="Quarto de Despejo",
            autor="Carolina Maria de Jesus",
            ano_publicacao=1960,
            disponivel=True,
        ),
        Livro(
            id=5,
            titulo="A Hora da Estrela",
            autor="Clarice Lispector",
            ano_publicacao=1977,
            disponivel=False,
        ),
    )
)


def obter_repositorio() -> RepositorioLivros:
    return _repositorio_padrao
