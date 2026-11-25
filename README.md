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
```

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


---

## Etapa 3 — Análise Léxica

Nesta etapa, foi implementado o analisador léxico
(scanner) do CompilaRef, utilizando Python.

O scanner recebe o código-fonte enviado pela interface,
identifica os elementos da linguagem e apresenta os
tokens encontrados, suas categorias, lexemas e posições.

### Subconjunto da linguagem

O CompilaRef utiliza um subconjunto simplificado de
Python, voltado para o ensino introdutório de compiladores.

| Categoria | Elementos suportados |
|---|---|
| Palavras reservadas | if, else, while, and, or, not, True, False |
| Identificadores | idade, numero1, _valor |
| Inteiros | 10, 20, 100 |
| Reais | 3.14, 10.5 |
| Strings | "Python", 'Olá' |
| Operadores aritméticos | +, -, *, / |
| Atribuição | = |
| Operadores relacionais | ==, !=, <, >, <=, >= |
| Delimitadores | (, ), :, vírgula |
| Comentários | # comentário |

Espaços e comentários são ignorados durante a
identificação dos tokens. As posições dos elementos
são registradas por linha e coluna.

### Implementação do scanner

O scanner foi desenvolvido em Python, no arquivo
`backend/scanner.py`.

Ele percorre o código caractere por caractere e agrupa
os elementos reconhecidos em tokens.

A implementação foi feita diretamente em Python,
sem bibliotecas externas de análise léxica, permitindo
acompanhar a lógica de reconhecimento dos elementos.

O scanner também identifica caracteres não reconhecidos,
literais numéricos malformados e strings não fechadas.

### Exemplo de análise

Código de entrada:

```python
idade = 20 + 5
```

Resultado esperado:

| Tipo | Lexema | Linha | Coluna |
|---|---|---|---|
| IDENTIFICADOR | idade | 1 | 1 |
| OPERADOR | = | 1 | 7 |
| LITERAL_INTEIRO | 20 | 1 | 9 |
| OPERADOR | + | 1 | 12 |
| LITERAL_INTEIRO | 5 | 1 | 14 |

### Tratamento de erros léxicos

O scanner informa a linha e a coluna dos caracteres
ou sequências que não pertencem ao subconjunto definido.

Exemplo:

```python
idade = 20 @ 5
```

Nesse caso, o sistema informa que o caractere `@`
não foi reconhecido, na linha 1, coluna 12.

A análise continua após o erro, sempre que possível,
permitindo identificar os demais tokens.

### Comunicação com o backend

A interface continua utilizando o endpoint:

POST /analisar

A requisição utiliza o formato JSON:

```json
{
  "codigo": "idade = 20"
}
```

A resposta contém os tokens e os erros encontrados:

```json
{
  "mensagem": "Análise léxica concluída com sucesso!",
  "recebido": true,
  "codigo": "idade = 20",
  "sucesso": true,
  "tokens": [
    {
      "tipo": "IDENTIFICADOR",
      "lexema": "idade",
      "linha": 1,
      "coluna": 1
    },
    {
      "tipo": "OPERADOR",
      "lexema": "=",
      "linha": 1,
      "coluna": 7
    },
    {
      "tipo": "LITERAL_INTEIRO",
      "lexema": "20",
      "linha": 1,
      "coluna": 9
    }
  ],
  "erros": []
}
```

Entradas vazias ou requisições inválidas retornam
HTTP 400. Códigos com erros léxicos retornam HTTP 200,
com `sucesso: false` e a lista de erros encontrados.

### Interface

Os resultados da análise são apresentados em uma tabela
com as seguintes informações:

- Tipo do token.
- Lexema identificado.
- Linha.
- Coluna.

A aplicação também apresenta mensagens explicativas,
erros léxicos e a quantidade de tokens reconhecidos.

### Testes automatizados

Foram criados testes para verificar o funcionamento
do scanner, da API e da interface.

Testes do scanner:

```bash
docker compose exec backend python -m unittest discover -s tests -p test_scanner.py -v
```

Testes dos endpoints:

```bash
docker compose exec backend python -m unittest discover -s tests -p test_api_scanner.py -v
```

Todos os testes Python do backend:

```bash
docker compose exec backend python -m unittest discover -s tests -p "test_*.py" -v
```

Testes do frontend (PowerShell):

```powershell
docker run --rm -v "${PWD}/frontend:/app" -w /app node:22-alpine node --test tests/script.test.cjs
```

Os resultados das execuções são registrados em
`docs/REGISTRO_TESTES.md`.

### Limitações atuais

O CompilaRef reconhece apenas o subconjunto de Python
documentado nesta etapa.

O scanner não executa o programa, não verifica sua
estrutura sintática e não realiza análise semântica.

A indentação é ignorada pelo scanner atual, e algumas
construções da linguagem Python ainda não são suportadas.

A análise sintática foi desenvolvida na Etapa 4,
aproveitando os tokens produzidos pelo scanner.

## Etapa 4 — Análise sintática e AST

A [gramática EBNF e o formato da AST](docs/GRAMATICA.md) documentam o
subconjunto de Python, terminais, precedência, exemplos e limitações. O parser
descendente recursivo é manual e usa os tokens do scanner da Etapa 3; linhas e
indentação são inferidas das posições e do código original. Não há dependências
novas. Erros léxicos impedem a execução do parser. Erros sintáticos retornam
o primeiro diagnóstico com linha e coluna, sem interromper a aplicação.

Exemplo válido:

```python
resultado = 10 + 5 * 2
if resultado >= 20:
    classe = "alta"
else:
    classe = "baixa"
```

Exemplos inválidos: `resultado = 10 +` (operando ausente), `if True:`
(bloco ausente) e `else:` (sem `if`). A interface exibe tokens e uma AST
hierárquica expansível, ou o erro sintático localizado.

### Contrato de `POST /analisar`

O corpo permanece `{"codigo": "x = 2 + 3"}`. A resposta HTTP 200 preserva
`mensagem`, `recebido`, `codigo`, `sucesso`, `tokens` e `erros`, e acrescenta
`lexico: {sucesso, tokens, erros}` e `sintatico: {sucesso, ast, erros}`.
`sucesso` e `erros` na raiz continuam sendo os resultados **léxicos** para
compatibilidade. `sintatico.ast` é um nó `PROGRAMA` em JSON, com `tipo`,
`linha`, `coluna`, `linha_fim`, `coluna_fim`, `atributos` e `filhos`.
Em erro sintático, `ast` é `null` e cada erro traz `tipo`, `linha`, `coluna`,
`encontrado`, `esperado` e `mensagem`. Em erro léxico, `sintatico` contém
`ignorado: true`, `ast: null` e `erros: []`. Entrada inválida, vazia ou maior
que 10.000 caracteres recebe HTTP 400.

### Execução e testes

Com Docker Desktop ativo, execute `docker compose up -d --build` e abra
`http://localhost:8080`. Selecione o exemplo 4 e verifique os tokens e a
árvore. Envie `resultado = 10 +` para observar um diagnóstico.

```text
docker compose exec backend python -m unittest discover -s tests -p "test_*.py" -v
node --test frontend/tests/script.test.cjs
docker compose ps
```

Os testes de integração antigos exigem o backend ativo na porta 5000.
Veja [o registro de testes](docs/REGISTRO_TESTES.md). A análise semântica,
funções e execução não estão implementadas; a AST servirá de base para a
Etapa 5. A integração com Ollama é opcional e não integra esta versão.
