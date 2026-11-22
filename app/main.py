from fastapi import FastAPI

from .rotas import roteador

app = FastAPI(
    title="API da Biblioteca",
    description="Consulta ao acervo de livros e à disponibilidade para empréstimo.",
    version="1.0.0",
)
app.include_router(roteador)
