# CompilaRef

O CompilaRef é um software educacional desenvolvido para auxiliar
estudantes no aprendizado de análise léxica na disciplina de Compiladores.

## Linguagem escolhida

A linguagem escolhida como referência foi Python, principalmente
por possuir uma sintaxe simples e de fácil leitura.

Nesta primeira versão será utilizado apenas um subconjunto
simplificado da linguagem.

Inicialmente serão considerados:

- identificadores;
- números inteiros;
- operadores aritméticos (+, -, *, /);
- operador de atribuição (=);
- palavras reservadas;
- parênteses.

O objetivo inicial do projeto será permitir que estudantes
visualizem e pratiquem a identificação e classificação de tokens.

## Tecnologias utilizadas

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Ambiente

- Docker
- Docker Compose

## Estrutura do projeto

- `frontend/`: interface web da aplicação.
- `backend/`: processamento da aplicação.
- `docker-compose.yml`: configuração dos serviços Docker.

## Pré-requisitos

Para executar o projeto é necessário possuir:

- Git
- Docker
- Docker Compose

## Executando o projeto

Clone o repositório:

```bash
git clone https://github.com/ClaitonCaio/CompilaRef.git


## Etapa 2 — Interface Web e Entrada de Código-Fonte

Nesta etapa, o CompilaRef foi atualizado para permitir que
estudantes insiram códigos escritos em Python simplificado
e solicitem seu processamento.

### Funcionalidades implementadas

- Interface web para entrada e edição de código.
- Seleção de três exemplos de programas.
- Botão para solicitar o processamento do código.
- Comunicação entre frontend e backend por HTTP.
- Validação de entradas vazias e inválidas.
- Exibição de mensagens de sucesso e erro.
- Testes automatizados do frontend, backend e integração.

### Exemplos disponíveis

**Exemplo 1 — Atribuição**
```python
idade = 20
```

**Exemplo 2 — Operação aritmética**
```python
resultado = 10 + 5
```

**Exemplo 3 — Expressão com parênteses**
```python
total = (10 + 5) * 2
```

### Tecnologias utilizadas

- Frontend: HTML, CSS e JavaScript.
- Backend: Python, Flask e Flask-CORS.
- Ambiente: Docker e Docker Compose.
- Testes: unittest (Python) e node:test (JavaScript).

### Como executar

Com o Docker Desktop em execução, utilize:

```bash
docker compose up -d --build
```

Acesse a interface pelo navegador:

http://localhost:8080

Para encerrar:

```bash
docker compose down
```

### Comunicação entre frontend e backend

O frontend envia uma requisição HTTP POST para
o endpoint `/analisar`, contendo um objeto JSON.

Exemplo:

```json
{
  "codigo": "idade = 20"
}
```

O backend valida a entrada e retorna uma resposta.

Exemplo:

```json
{
  "mensagem": "Código recebido com sucesso!",
  "recebido": true,
  "codigo": "idade = 20"
}
```

### Testes automatizados

**Testes do backend:**

```bash
docker compose exec backend python -m unittest discover -s tests -p test_api.py -v
```

**Testes do frontend (PowerShell):**

```powershell
docker run --rm -v "${PWD}/frontend:/app" -w /app node:22-alpine node --test tests/script.test.cjs
```

**Testes de integração:**

```bash
docker compose exec backend python -m unittest discover -s tests -p test_integracao.py -v
```

### Resultados dos testes

| Categoria | Testes aprovados |
|---|---:|
| Backend | 8 |
| Frontend | 6 |
| Integração | 4 |
| Total | 18 |

### Limitações atuais

Nesta etapa, o CompilaRef recebe e valida códigos-fonte,
mas ainda não realiza análise léxica, sintática ou semântica.

O reconhecimento e a classificação de tokens serão
implementados nas próximas etapas.

O projeto utiliza um subconjunto simplificado de Python,
voltado para exemplos introdutórios.
