
# Escopo Léxico — CompilaRef

## Linguagem utilizada

O CompilaRef utiliza um subconjunto simplificado da
linguagem Python, com foco no ensino de análise léxica
para estudantes iniciantes da disciplina de Compiladores.

O analisador léxico será responsável por reconhecer
os elementos do código-fonte e classificá-los em tokens.

## Categorias reconhecidas

| Categoria | Exemplos |
|---|---|
| Palavras reservadas | if, else, while, and, or, not, True, False |
| Identificadores | idade, numero, resultado, _valor1 |
| Números inteiros | 10, 20, 100 |
| Números reais | 3.14, 10.5 |
| Strings | "Olá", 'Python' |
| Operadores aritméticos | +, -, *, / |
| Operador de atribuição | = |
| Operadores relacionais | ==, !=, <, >, <=, >= |
| Delimitadores | (, ), :, , |
| Comentários | # comentário |

## Regras de reconhecimento

### Identificadores

Devem começar com uma letra ou sublinhado (_).
Os demais caracteres podem conter letras,
números ou sublinhados.

Exemplos válidos:
- idade
- numero1
- _resultado

### Literais

O scanner reconhecerá:
- Números inteiros.
- Números reais com ponto decimal.
- Strings entre aspas simples ou duplas.

### Operadores

Os operadores serão reconhecidos individualmente.
Operadores compostos, como == e >=, deverão ser
reconhecidos como um único token.

### Comentários

Comentários começam com # e continuam até o
final da linha. Eles serão ignorados pelo scanner.

### Espaços em branco

Espaços, tabulações e quebras de linha serão
ignorados na geração de tokens.

As quebras de linha serão consideradas para
identificar a posição dos elementos no código.

### Erros léxicos

Caracteres e sequências não reconhecidos
deverão gerar mensagens de erro.

Cada erro deverá informar:
- O elemento inválido.
- A linha.
- A coluna.
- Uma explicação do problema.

O scanner deverá continuar a análise sempre
que possível, permitindo identificar outros erros.

## Limitações

O CompilaRef não pretende reconhecer toda a
linguagem Python.

Nesta versão, não serão implementadas:
- Análise sintática.
- Análise semântica.
- Execução do código-fonte.
- Geração de código.
- Todas as construções da linguagem Python.

Essas funcionalidades poderão ser consideradas
nas próximas etapas do projeto.
