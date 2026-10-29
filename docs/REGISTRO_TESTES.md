
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
