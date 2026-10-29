
# Analisador léxico do CompilaRef
# Linguagem: Python simplificado

PALAVRAS_RESERVADAS = {
    "if", "else", "while", "and",
    "or", "not", "True", "False"
}

OPERADORES = {
    "+", "-", "*", "/", "=",
    "==", "!=", "<", ">", "<=", ">="
}

DELIMITADORES = {"(", ")", ":", ","}


def analisar_lexico(codigo):
    tokens = []
    erros = []

    # Padroniza as quebras de linha
    codigo = codigo.replace("\r\n", "\n").replace("\r", "\n")

    posicao = 0
    linha = 1
    coluna = 1

    def avancar():
        nonlocal posicao, linha, coluna

        caractere = codigo[posicao]
        posicao += 1

        if caractere == "\n":
            linha += 1
            coluna = 1
        else:
            coluna += 1

        return caractere

    def adicionar_token(tipo, lexema, lin, col):
        tokens.append({
            "tipo": tipo,
            "lexema": lexema,
            "linha": lin,
            "coluna": col
        })

    def adicionar_erro(lexema, lin, col, mensagem):
        erros.append({
            "tipo": "ERRO_LEXICO",
            "lexema": lexema,
            "linha": lin,
            "coluna": col,
            "mensagem": mensagem
        })

    while posicao < len(codigo):
        caractere = codigo[posicao]

        # Ignorar espaços, tabulações e quebras de linha
        if caractere.isspace():
            avancar()
            continue

        # Ignorar comentários iniciados por #
        if caractere == "#":
            while (
                posicao < len(codigo)
                and codigo[posicao] != "\n"
            ):
                avancar()
            continue

        linha_inicio = linha
        coluna_inicio = coluna
        inicio = posicao

        # Reconhecimento de identificadores e palavras reservadas
        if caractere.isalpha() or caractere == "_":
            while (
                posicao < len(codigo)
                and (
                    codigo[posicao].isalnum()
                    or codigo[posicao] == "_"
                )
            ):
                avancar()

            lexema = codigo[inicio:posicao]

            if lexema in PALAVRAS_RESERVADAS:
                tipo = "PALAVRA_RESERVADA"
            else:
                tipo = "IDENTIFICADOR"

            adicionar_token(
                tipo, lexema, linha_inicio, coluna_inicio
            )
            continue

        # Reconhecimento de números inteiros e reais
        if caractere.isdigit():
            while (
                posicao < len(codigo)
                and codigo[posicao].isdigit()
            ):
                avancar()

            tipo = "LITERAL_INTEIRO"
            numero_invalido = False

            if (
                posicao < len(codigo)
                and codigo[posicao] == "."
            ):
                avancar()

                if (
                    posicao < len(codigo)
                    and codigo[posicao].isdigit()
                ):
                    tipo = "LITERAL_REAL"

                    while (
                        posicao < len(codigo)
                        and codigo[posicao].isdigit()
                    ):
                        avancar()
                else:
                    numero_invalido = True

            # Detectar sequências como 123abc
            if (
                posicao < len(codigo)
                and (
                    codigo[posicao].isalpha()
                    or codigo[posicao] == "_"
                )
            ):
                numero_invalido = True

                while (
                    posicao < len(codigo)
                    and (
                        codigo[posicao].isalnum()
                        or codigo[posicao] == "_"
                    )
                ):
                    avancar()

            lexema = codigo[inicio:posicao]

            if numero_invalido:
                adicionar_erro(
                    lexema,
                    linha_inicio,
                    coluna_inicio,
                    f"Literal numérico inválido: '{lexema}'"
                )
            else:
                adicionar_token(
                    tipo, lexema, linha_inicio, coluna_inicio
                )
            continue

        # Reconhecimento de strings
        if caractere in ('"', "'"):
            aspas = caractere
            avancar()
            fechada = False

            while posicao < len(codigo):
                atual = codigo[posicao]

                if atual == "\n":
                    break

                if atual == "\\":
                    avancar()

                    if (
                        posicao < len(codigo)
                        and codigo[posicao] != "\n"
                    ):
                        avancar()
                    continue

                if atual == aspas:
                    avancar()
                    fechada = True
                    break

                avancar()

            lexema = codigo[inicio:posicao]

            if fechada:
                adicionar_token(
                    "LITERAL_STRING",
                    lexema,
                    linha_inicio,
                    coluna_inicio
                )
            else:
                adicionar_erro(
                    lexema,
                    linha_inicio,
                    coluna_inicio,
                    "String não fechada corretamente."
                )
            continue

        # Operadores compostos têm prioridade
        if posicao + 1 < len(codigo):
            operador_duplo = codigo[posicao:posicao + 2]

            if operador_duplo in OPERADORES:
                avancar()
                avancar()

                adicionar_token(
                    "OPERADOR",
                    operador_duplo,
                    linha_inicio,
                    coluna_inicio
                )
                continue

        # Operadores simples
        if caractere in OPERADORES:
            avancar()

            adicionar_token(
                "OPERADOR",
                caractere,
                linha_inicio,
                coluna_inicio
            )
            continue

        # Delimitadores
        if caractere in DELIMITADORES:
            avancar()

            adicionar_token(
                "DELIMITADOR",
                caractere,
                linha_inicio,
                coluna_inicio
            )
            continue

        # Caracteres não reconhecidos
        adicionar_erro(
            caractere,
            linha_inicio,
            coluna_inicio,
            f"Caractere não reconhecido: '{caractere}'"
        )

        avancar()

    return {
        "sucesso": len(erros) == 0,
        "tokens": tokens,
        "erros": erros
    }
