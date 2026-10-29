
# Registro de Testes — CompilaRef

## Etapa 2 — Interface Web e Entrada de Código-Fonte

Data: 28/10/2026

### 1. Testes do Backend

Ferramenta: Python unittest

Comando:
docker compose exec backend python -m unittest discover -s tests -p test_api.py -v

Funcionalidades verificadas:
- Funcionamento da rota /hello.
- Recebimento de código-fonte.
- Envio de expressões aritméticas.
- Validação de código vazio.
- Validação de espaços em branco.
- Tratamento de campos ausentes.
- Tratamento de tipos de dados inválidos.
- Tratamento de requisições inválidas.

Resultado: 8 testes aprovados.

### 2. Testes do Frontend

Ferramenta: Node.js (node:test)

Funcionalidades verificadas:
- Carregamento dos três exemplos.
- Edição do código-fonte.
- Validação de entrada vazia.
- Envio do código ao backend simulado.
- Tratamento de falhas de comunicação.
- Tratamento de respostas de erro.

Resultado: 6 testes aprovados.

### 3. Testes de Integração

Ferramenta: Python unittest e requisições HTTP.

Comando:
docker compose exec backend python -m unittest discover -s tests -p test_integracao.py -v

Funcionalidades verificadas:
- Disponibilidade do backend.
- Envio de código-fonte por HTTP.
- Tratamento de código vazio.
- Tratamento de dados inválidos.

Resultado: 4 testes aprovados.

### 4. Testes Manuais

Ambiente: Docker Compose

Verificações realizadas:
- Inicialização da aplicação.
- Acesso à interface em localhost:8080.
- Seleção de exemplos de Python.
- Edição do código-fonte.
- Envio do código ao backend.
- Exibição da resposta de recebimento.
- Acesso à rota /hello.

Resultado: funcionamento confirmado.

### 5. Resumo

Backend: 8 testes aprovados.
Frontend: 6 testes aprovados.
Integração: 4 testes aprovados.

Total: 18 testes automatizados aprovados.

### 6. Limitações

A aplicação ainda não realiza análise léxica,
sintática ou semântica.

Os testes automatizados do frontend utilizam
simulação da interface e da comunicação HTTP.

Testes automatizados completos em navegador
ainda não foram implementados.

Novos testes serão adicionados conforme
as próximas funcionalidades forem desenvolvidas.


---

# Etapa 3 — Análise Léxica

Data: 29/10/2026

## 1. Testes unitários do scanner

Arquivo: backend/tests/test_scanner.py

Ferramenta: Python unittest

Comando:
`docker compose exec backend python -m unittest discover -s tests -p test_scanner.py -v`

Funcionalidades verificadas:
- Reconhecimento de palavras reservadas.
- Identificação de identificadores.
- Reconhecimento de números inteiros e reais.
- Detecção de literais numéricos inválidos.
- Reconhecimento de strings.
- Detecção de strings não fechadas.
- Reconhecimento de operadores simples e compostos.
- Identificação de delimitadores.
- Tratamento de comentários.
- Tratamento de espaços em branco.
- Identificação de linha e coluna.
- Detecção de caracteres inválidos.
- Tratamento de código vazio.
- Tratamento de comentários isolados.
- Reconhecimento de tokens no final do arquivo.

Resultado: 15 testes aprovados.

## 2. Testes da API do scanner

Arquivo: backend/tests/test_api_scanner.py

Ferramenta: Python unittest

Comando:
`docker compose exec backend python -m unittest discover -s tests -p test_api_scanner.py -v`

Funcionalidades verificadas:
- Análise de código válido.
- Classificação dos tokens.
- Posição dos tokens.
- Identificação de caracteres inválidos.
- Continuação da análise após erros.
- Validação de entrada vazia.
- Validação de espaços em branco.
- Tratamento de requisições inválidas.
- Verificação do formato JSON retornado.

Resultado: 9 testes aprovados.

## 3. Testes do frontend

Arquivo: frontend/tests/script.test.cjs

Ferramenta: Node.js (node:test)

Funcionalidades verificadas:
- Carregamento dos três exemplos.
- Edição do código.
- Validação de entradas vazias.
- Exibição da tabela de tokens.
- Exibição de erros léxicos.
- Tratamento de falhas de comunicação.
- Tratamento de respostas HTTP inválidas.
- Exibição de resultados sem tokens.
- Limpeza dos resultados ao selecionar outro exemplo.

Resultado: 9 testes aprovados.

## 4. Testes de regressão

Foram mantidos os testes automatizados
das funcionalidades desenvolvidas anteriormente.

Testes anteriores da API: 8 aprovados.
Testes de integração HTTP: 4 aprovados.

As verificações incluem a rota /hello,
o recebimento de código-fonte, as validações
de entrada e a comunicação com o backend.

## 5. Testes manuais

Ambiente: Docker Compose

Funcionalidades verificadas:
- Inicialização da aplicação.
- Acesso à interface web.
- Seleção de exemplos.
- Envio de código-fonte.
- Exibição dos tokens.
- Exibição de linha e coluna.
- Identificação de erros léxicos.
- Tratamento de entrada vazia.

Resultado: funcionamento confirmado.

## 6. Resumo dos testes automatizados

| Categoria | Testes aprovados |
|---|---:|
| Scanner | 15 |
| API do scanner | 9 |
| API anterior | 8 |
| Integração HTTP | 4 |
| Frontend | 9 |
| Total | 45 |

## 7. Limitações

O scanner reconhece apenas o subconjunto
simplificado de Python definido no projeto.

Ainda não foram implementadas as análises
sintática e semântica.

Os testes automatizados do frontend utilizam
simulações do DOM e das respostas HTTP.

A implementação será ampliada nas próximas
etapas do desenvolvimento.
