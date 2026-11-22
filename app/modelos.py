from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

TextoObrigatorio = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Livro(BaseModel):
    # A validação estrita evita conversões como "2020" para inteiro e 1 para booleano.
    model_config = ConfigDict(strict=True, frozen=True)

    id: int = Field(gt=0)
    titulo: TextoObrigatorio
    autor: TextoObrigatorio
    ano_publicacao: int = Field(gt=0)
    disponivel: bool


class ErroConsulta(BaseModel):
    detail: str
