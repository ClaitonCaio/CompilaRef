# Gramática da Etapa 4 — Python simplificado

O símbolo inicial é `programa`. Esta é uma linguagem didática inspirada em Python,
não um parser para Python completo. Cada comando ocupa uma linha lógica; linhas
vazias e comentários são ignorados. Blocos usam indentação por espaços ou tabs
(tab equivale a quatro espaços). O recuo deve ser consistente em cada bloco.

## EBNF

```ebnf
programa       = { comando } ;
comando        = atribuicao | condicional | repeticao ;
atribuicao     = IDENTIFICADOR, "=", expressao, FIM_LINHA ;
condicional    = "if", expressao, ":", FIM_LINHA, bloco,
                 [ "else", ":", FIM_LINHA, bloco ] ;
repeticao      = "while", expressao, ":", FIM_LINHA, bloco ;
bloco          = INDENT, comando, { comando }, DEDENT ;
expressao      = disjuncao ;
disjuncao      = conjuncao, { "or", conjuncao } ;
conjuncao      = negacao, { "and", negacao } ;
negacao        = "not", negacao | comparacao ;
comparacao     = soma, { ( "==" | "!=" | "<" | ">" | "<=" | ">=" ), soma } ;
soma           = produto, { ( "+" | "-" ), produto } ;
produto        = unario, { ( "*" | "/" ), unario } ;
unario         = ( "+" | "-" ), unario | primario ;
primario       = IDENTIFICADOR | LITERAL_INTEIRO | LITERAL_REAL |
                 LITERAL_STRING | "True" | "False" | "(", expressao, ")" ;
```

`FIM_LINHA`, `INDENT` e `DEDENT` são limites estruturais inferidos pelo parser
das linhas e posições do código original; o scanner da Etapa 3 não os emite.
As demais palavras entre aspas são lexemas dos tokens `OPERADOR`,
`DELIMITADOR` e `PALAVRA_RESERVADA` do scanner. `IDENTIFICADOR` e os três
`LITERAL_*` correspondem diretamente às categorias léxicas. Não houve alteração
nos tokens já produzidos pelo scanner.

Os não terminais são os nomes à esquerda das produções. A precedência, da
maior para a menor, é: parênteses, unários `+`/`-`, `*`/`/`, `+`/`-`,
comparações, `not`, `and`, `or`. Operadores binários de mesmo nível associam
à esquerda. A implementação aceita `not` repetido (`not not x`) e comparações
encadeadas como expressão binária à esquerda; isso não reproduz a semântica
especial das comparações encadeadas de Python.

## Exemplos

Válido:

```python
resultado = 10 + 5 * 2
if resultado >= 20:
    categoria = "alto"
else:
    categoria = "baixo"
```

Inválidos: `resultado = 10 +` (falta operando), `if True:` sem bloco
indentado, `else:` sem `if`, `x = (2 + 3` (falta `)`) e
`if True` (falta `:`). O parser aponta o primeiro erro sintático, com linha,
coluna, encontrado e esperado; não há recuperação de múltiplos erros.

## AST

Cada nó é um objeto JSON com `tipo`, `linha`, `coluna`, `linha_fim`,
`coluna_fim` (limite final exclusivo), `atributos` e `filhos`. Os tipos são
`PROGRAMA`, `BLOCO`, `ATRIBUICAO`, `CONDICIONAL`, `REPETICAO`,
`IDENTIFICADOR`, `LITERAL`, `OPERACAO_BINARIA`, `OPERACAO_UNARIA` e
`AGRUPAMENTO`. `ATRIBUICAO` tem filhos identificador e expressão;
`CONDICIONAL` tem condição, bloco verdadeiro e bloco alternativo opcional;
`REPETICAO` tem condição e bloco. Operações guardam `operador`, identificadores
guardam `nome` e literais guardam `valor` e `categoria`.

Em `x = 10 + 5 * 2`, a atribuição contém `OPERACAO_BINARIA(+)`, cujo filho
direito é `OPERACAO_BINARIA(*)`. A árvore de derivação conteria também
não terminais intermediários e pontuação. Esta interface exibe a AST, não a
árvore de derivação. `AGRUPAMENTO` conserva a intenção dos parênteses na AST.

## Estratégia e limites

O parser descendente recursivo em `backend/parser.py` foi escrito manualmente
em Python, sem gerador ou biblioteca adicional. A precedência é aplicada por
níveis numéricos durante a leitura de expressões. A estratégia facilita seguir
as regras e criar diagnósticos didáticos. O scanner da Etapa 3 continua sendo
usado sem modificação. Erros léxicos impedem a execução do parser, evitando
diagnósticos sobre uma sequência incompleta de tokens.

Não há declarações de tipos, funções, chamadas, listas, `for`, `return`,
atribuição composta, instruções na mesma linha do `if`, continuação de linha,
semântica de variáveis ou execução. Estas últimas ficam para etapas posteriores.
