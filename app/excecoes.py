class LivroNaoEncontradoError(LookupError):
    def __init__(self, livro_id: int) -> None:
        super().__init__(f"Livro com ID {livro_id} não encontrado.")
