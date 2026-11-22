# API da Biblioteca

Atividade **Desenvolvimento de API com FastAPI** da disciplina Arquitetura de Software (7PPA), Engenharia de Software. A API consulta um acervo de cinco livros armazenados em memória e informa a disponibilidade para empréstimo.

## Como executar

**Pré-requisito** — Python 3.10 ou superior.

Clone o repositório e abra a pasta do projeto:

```bash
git clone https://github.com/ericksena17/biblioteca-fastapi.git
cd biblioteca-fastapi
```

No Windows, usando PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

No Linux ou macOS:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m uvicorn app.main:app --reload
```

Com o servidor em execução, abra a [documentação interativa Swagger](http://127.0.0.1:8000/docs). Expanda uma rota, clique em **Try it out** e depois em **Execute**.

## Rotas

| Requisição | Status | Resultado |
| --- | --- | --- |
| `GET /livros` | 200 | Lista JSON de livros. Se o acervo estiver vazio, retorna `[]`. |
| `GET /livros/1` | 200 | Objeto JSON com o livro encontrado. |
| `GET /livros/999` | 404 | O ID é válido, mas o livro está ausente do acervo. |
| `GET /livros/0`, `/livros/-1`, `/livros/abc` ou `/livros/1.5` | 422 | O ID deve ser um inteiro maior que zero. |

Exemplo de resposta para `GET /livros/1`:

```json
{
  "id": 1,
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano_publicacao": 1899,
  "disponivel": true
}
```

## Organização do código

| Arquivo | Responsabilidade |
| --- | --- |
| `app/main.py` | Cria a aplicação FastAPI e registra as rotas. |
| `app/rotas.py` | Define rotas e modelos de resposta, valida o ID da URL e converte a exceção em HTTP 404. |
| `app/modelos.py` | Define o modelo de livro com Pydantic e o formato da resposta 404. |
| `app/repositorio.py` | Armazena os livros em memória e implementa a listagem e a busca por ID. |
| `app/excecoes.py` | Define a exceção de livro ausente. |

O modelo exige ID e ano de publicação inteiros positivos, disponibilidade booleana, título e autor com conteúdo após a remoção dos espaços nas extremidades.

## Testes automatizados

Com o ambiente virtual já criado, execute no Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

No Linux ou macOS:

```bash
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/python -m unittest discover -s tests -v
```
