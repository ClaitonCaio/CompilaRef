import unittest

from scanner import analisar_lexico
from parser import analisar_sintatico


def analisar(codigo):
    lexico = analisar_lexico(codigo)
    assert lexico["sucesso"], lexico["erros"]
    return analisar_sintatico(lexico["tokens"], codigo)


class TestParser(unittest.TestCase):
    def test_precedencia(self):
        ast = analisar("resultado = 10 + 5 * 2")["ast"]
        expressao = ast["filhos"][0]["filhos"][1]
        self.assertEqual(expressao["atributos"]["operador"], "+")
        self.assertEqual(expressao["filhos"][1]["atributos"]["operador"], "*")
        self.assertEqual((expressao["linha"], expressao["coluna"]), (1, 13))

    def test_associatividade_e_parenteses(self):
        expr = analisar("x = 20 - 5 - 3")["ast"]["filhos"][0]["filhos"][1]
        self.assertEqual(expr["filhos"][0]["atributos"]["operador"], "-")
        expr = analisar("x = (10 + 5) * 2")["ast"]["filhos"][0]["filhos"][1]
        self.assertEqual(expr["atributos"]["operador"], "*")
        self.assertEqual(expr["filhos"][0]["tipo"], "AGRUPAMENTO")

    def test_blocos_aninhados(self):
        codigo = "x = 1\nif x > 0:\n    while x < 3:\n        x = x + 1\nelse:\n    x = 0"
        resultado = analisar(codigo)
        self.assertTrue(resultado["sucesso"])
        condicional = resultado["ast"]["filhos"][1]
        self.assertEqual(condicional["tipo"], "CONDICIONAL")
        self.assertEqual(condicional["filhos"][1]["filhos"][0]["tipo"], "REPETICAO")
        self.assertEqual(condicional["filhos"][2]["filhos"][0]["linha"], 6)

    def test_literais_logica_e_comentarios(self):
        resultado = analisar("# comentário\nativo = True\nif not ativo or 2 <= 3:\n    nome = 'Ana'")
        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["ast"]["filhos"][0]["linha"], 2)

    def test_erros(self):
        casos = [
            ("x = 2 +", "uma expressão"),
            ("if True:\nx = 1", "bloco indentado"),
            ("else:\n    x = 1", "if"),
            ("if True\n    x = 1", "':'"),
            ("x = (2 + 3", "')'"),
            ("x = 1\n    y = 2", "indentação"),
            ("x = 1 2", "fim da expressão"),
        ]
        for codigo, esperado in casos:
            with self.subTest(codigo=codigo):
                resultado = analisar(codigo)
                self.assertFalse(resultado["sucesso"])
                self.assertIsNone(resultado["ast"])
                self.assertIn(esperado, " ".join(resultado["erros"][0]["esperado"]))
                self.assertGreaterEqual(resultado["erros"][0]["coluna"], 1)

    def test_sem_comandos(self):
        self.assertEqual(analisar("# apenas comentário")["ast"]["filhos"], [])


if __name__ == "__main__":
    unittest.main()
