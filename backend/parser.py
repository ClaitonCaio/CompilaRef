"""Parser descendente recursivo para o subconjunto didático de Python.

O scanner fornece os tokens. A indentação é obtida das posições e das linhas
originais, pois a Etapa 3 não emite tokens INDENT/DEDENT ou NEWLINE.
"""


class ErroSintatico(Exception):
    def __init__(self, token, esperado, mensagem=None):
        self.token = token
        self.esperado = esperado if isinstance(esperado, list) else [esperado]
        encontrado = token["lexema"] if token else "fim do código"
        self.dados = {
            "tipo": "ERRO_SINTATICO",
            "linha": token["linha"] if token else 1,
            "coluna": token["coluna"] if token else 1,
            "encontrado": encontrado,
            "esperado": self.esperado,
            "mensagem": mensagem or
            f"Era esperado {', '.join(self.esperado)}, mas foi encontrado '{encontrado}'.",
        }
        super().__init__(self.dados["mensagem"])


def no(tipo, inicio, filhos=None, **atributos):
    filhos = filhos or []
    fim = filhos[-1] if filhos else inicio
    return {
        "tipo": tipo,
        "linha": inicio["linha"], "coluna": inicio["coluna"],
        "linha_fim": fim.get("linha_fim", fim["linha"]),
        "coluna_fim": fim.get("coluna_fim", fim["coluna"] + len(fim.get("lexema", ""))),
        "atributos": atributos, "filhos": filhos,
    }


class Expressoes:
    PRECEDENCIA = {"or": 1, "and": 2, "==": 3, "!=": 3, "<": 3,
                   ">": 3, "<=": 3, ">=": 3, "+": 4, "-": 4,
                   "*": 5, "/": 5}

    def __init__(self, tokens, fim):
        self.tokens = tokens
        self.fim = fim
        self.i = 0

    def atual(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else self.fim

    def avancar(self):
        token = self.atual()
        self.i += 1
        return token

    def exigir(self, lexema):
        token = self.atual()
        if token["lexema"] != lexema or self.i >= len(self.tokens):
            raise ErroSintatico(token, repr(lexema))
        return self.avancar()

    def expressao(self, minimo=1):
        token = self.atual()
        if self.i >= len(self.tokens):
            raise ErroSintatico(token, "uma expressão", "Falta uma expressão ou operando.")
        if token["lexema"] in ("-", "+", "not"):
            self.avancar()
            filho = self.expressao(6 if token["lexema"] != "not" else 3)
            esquerda = no("OPERACAO_UNARIA", token, [filho], operador=token["lexema"])
        elif token["lexema"] == "(":
            self.avancar()
            esquerda = self.expressao()
            fechamento = self.exigir(")")
            esquerda = no("AGRUPAMENTO", token, [esquerda])
            esquerda["linha_fim"] = fechamento["linha"]
            esquerda["coluna_fim"] = fechamento["coluna"] + 1
        elif token["tipo"] in ("IDENTIFICADOR", "LITERAL_INTEIRO", "LITERAL_REAL",
                                "LITERAL_STRING") or token["lexema"] in ("True", "False"):
            self.avancar()
            tipo = "IDENTIFICADOR" if token["tipo"] == "IDENTIFICADOR" else "LITERAL"
            esquerda = no(tipo, token, nome=token["lexema"] if tipo == "IDENTIFICADOR" else None,
                          valor=token["lexema"] if tipo == "LITERAL" else None,
                          categoria=token["tipo"])
        else:
            raise ErroSintatico(token, "identificador, literal ou '('")

        while self.i < len(self.tokens):
            operador = self.atual()["lexema"]
            precedencia = self.PRECEDENCIA.get(operador, 0)
            if precedencia < minimo:
                break
            op = self.avancar()
            direita = self.expressao(precedencia + 1)  # associatividade à esquerda
            esquerda = no("OPERACAO_BINARIA", esquerda, [esquerda, direita], operador=op["lexema"])
        return esquerda


class Parser:
    def __init__(self, tokens, codigo):
        self.linhas = []
        linhas_codigo = codigo.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        for token in tokens:
            if not self.linhas or self.linhas[-1]["numero"] != token["linha"]:
                texto = linhas_codigo[token["linha"] - 1]
                prefixo = texto[:len(texto) - len(texto.lstrip(" \t"))]
                self.linhas.append({"numero": token["linha"], "indent": len(prefixo.expandtabs(4)),
                                   "tokens": []})
            self.linhas[-1]["tokens"].append(token)
        self.i = 0
        self.eof = {"linha": len(linhas_codigo), "coluna": len(linhas_codigo[-1]) + 1,
                    "lexema": "fim do código"}

    def parse(self):
        filhos = self.bloco(0)
        return no("PROGRAMA", {"linha": 1, "coluna": 1, "lexema": ""}, filhos)

    def bloco(self, indent):
        filhos = []
        while self.i < len(self.linhas):
            linha = self.linhas[self.i]
            token = linha["tokens"][0]
            if linha["indent"] < indent:
                break
            if linha["indent"] > indent:
                raise ErroSintatico(token, f"indentação de {indent} espaços",
                                    "Indentação inesperada nesta linha.")
            self.i += 1
            primeiro = token["lexema"]
            if primeiro == "else":
                raise ErroSintatico(token, "if", "'else' sem um 'if' correspondente.")
            if primeiro in ("if", "while"):
                filhos.append(self.controle(linha, indent, primeiro))
            else:
                filhos.append(self.comando(linha["tokens"]))
        return filhos

    def suite(self, linha, indent):
        proxima = self.linhas[self.i] if self.i < len(self.linhas) else None
        if not proxima or proxima["indent"] <= indent:
            token = proxima["tokens"][0] if proxima else self.eof
            raise ErroSintatico(token, "bloco indentado",
                                "Era esperado um bloco indentado após ':'.")
        return no("BLOCO", linha["tokens"][0], self.bloco(proxima["indent"]))

    def controle(self, linha, indent, palavra):
        tokens = linha["tokens"]
        if tokens[-1]["lexema"] != ":":
            raise ErroSintatico(self.linhas[self.i]["tokens"][0] if self.i < len(self.linhas) else self.eof,
                                "':'", f"Falta ':' após a condição de '{palavra}'.")
        exp = Expressoes(tokens[1:-1], tokens[-1])
        condicao = exp.expressao()
        if exp.i < len(exp.tokens):
            raise ErroSintatico(exp.atual(), "fim da condição")
        filhos = [condicao, self.suite(linha, indent)]
        if palavra == "if" and self.i < len(self.linhas):
            seguinte = self.linhas[self.i]
            if seguinte["indent"] == indent and seguinte["tokens"][0]["lexema"] == "else":
                self.i += 1
                if len(seguinte["tokens"]) != 2 or seguinte["tokens"][1]["lexema"] != ":":
                    raise ErroSintatico(seguinte["tokens"][-1], "':' após else")
                filhos.append(self.suite(seguinte, indent))
        return no("CONDICIONAL" if palavra == "if" else "REPETICAO", tokens[0], filhos)

    def comando(self, tokens):
        if tokens[0]["tipo"] != "IDENTIFICADOR":
            raise ErroSintatico(tokens[0], "identificador ou if/while")
        if len(tokens) < 2 or tokens[1]["lexema"] != "=":
            token = tokens[1] if len(tokens) > 1 else self.proximo(tokens[0])
            raise ErroSintatico(token, "'='", "Era esperado '=' após o identificador.")
        exp = Expressoes(tokens[2:], self.proximo(tokens[-1]))
        valor = exp.expressao()
        if exp.i < len(exp.tokens):
            raise ErroSintatico(exp.atual(), "fim da expressão")
        nome = no("IDENTIFICADOR", tokens[0], nome=tokens[0]["lexema"])
        return no("ATRIBUICAO", tokens[0], [nome, valor])

    def proximo(self, token):
        if self.i < len(self.linhas):
            return self.linhas[self.i]["tokens"][0]
        return {"linha": token["linha"], "coluna": token["coluna"] + len(token["lexema"]),
                "lexema": "fim do código"}


def analisar_sintatico(tokens, codigo):
    try:
        return {"sucesso": True, "ast": Parser(tokens, codigo).parse(), "erros": []}
    except ErroSintatico as erro:
        return {"sucesso": False, "ast": None, "erros": [erro.dados]}
    except RecursionError:
        return {"sucesso": False, "ast": None, "erros": [{
            "tipo": "ERRO_SINTATICO", "linha": 1, "coluna": 1,
            "encontrado": "expressão muito aninhada", "esperado": ["expressão mais simples"],
            "mensagem": "A expressão contém níveis demais de aninhamento. Simplifique os parênteses ou operadores."
        }]}
