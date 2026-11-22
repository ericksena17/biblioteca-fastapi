from unittest import IsolatedAsyncioTestCase, TestCase

from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.main import app
from app.modelos import Livro
from app.repositorio import RepositorioLivros, obter_repositorio


class TesteRotasLivros(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.cliente = AsyncClient(transport=ASGITransport(app=app), base_url="http://teste")
        self.addAsyncCleanup(self.cliente.aclose)

    async def test_listar_acervo(self) -> None:
        resposta = await self.cliente.get("/livros")
        self.assertEqual(resposta.status_code, 200)
        acervo = resposta.json()
        self.assertIsInstance(acervo, list)
        self.assertGreaterEqual(len(acervo), 5)
        for livro in acervo:
            Livro.model_validate(livro)

    async def test_listar_acervo_vazio(self) -> None:
        def obter_repositorio_vazio() -> RepositorioLivros:
            return RepositorioLivros(())

        app.dependency_overrides[obter_repositorio] = obter_repositorio_vazio
        self.addCleanup(app.dependency_overrides.pop, obter_repositorio)

        resposta = await self.cliente.get("/livros")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), [])

    async def test_consultar_livro_existente(self) -> None:
        resposta = await self.cliente.get("/livros/1")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.json(),
            {
                "id": 1,
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "ano_publicacao": 1899,
                "disponivel": True,
            },
        )

    async def test_consultar_livro_inexistente(self) -> None:
        resposta = await self.cliente.get("/livros/999")
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.json(), {"detail": "Livro com ID 999 não encontrado."})

    async def test_rejeitar_ids_invalidos(self) -> None:
        for livro_id in ("0", "-1", "abc", "1.0", "1.5"):
            with self.subTest(livro_id=livro_id):
                resposta = await self.cliente.get(f"/livros/{livro_id}")
                self.assertEqual(resposta.status_code, 422)
                self.assertEqual(resposta.json()["detail"][0]["loc"], ["path", "livro_id"])


class TesteModeloLivro(TestCase):
    def test_rejeitar_dados_invalidos(self) -> None:
        dados = Livro(
            id=1,
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            ano_publicacao=1899,
            disponivel=True,
        ).model_dump()
        casos_invalidos = (
            ("id", 0),
            ("id", "1"),
            ("titulo", ""),
            ("autor", "   "),
            ("ano_publicacao", -1),
            ("ano_publicacao", 1899.5),
            ("disponivel", 1),
        )
        for campo, valor in casos_invalidos:
            with self.subTest(campo=campo, valor=valor):
                with self.assertRaises(ValidationError):
                    Livro.model_validate({**dados, campo: valor})
