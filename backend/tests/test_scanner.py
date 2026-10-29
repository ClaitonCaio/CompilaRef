
import unittest
from scanner import analisar_lexico


class TestScanner(unittest.TestCase):

    def test_palavras_reservadas(self):
        palavras = [
            "if", "else", "while", "and",
            "or", "not", "True", "False"
        ]

        for palavra in palavras:
            with self.subTest(palavra=palavra):
                resultado = analisar_lexico(palavra)

                self.assertTrue(resultado["sucesso"])
                self.assertEqual(
                    resultado["tokens"][0]["tipo"],
                    "PALAVRA_RESERVADA"
                )

    def test_identificadores(self):
        codigo = "idade numero1 _resultado"
        resultado = analisar_lexico(codigo)

        self.assertEqual(len(resultado["tokens"]), 3)

        for token in resultado["tokens"]:
            self.assertEqual(token["tipo"], "IDENTIFICADOR")

    def test_numeros_inteiros_e_reais(self):
        resultado = analisar_lexico("10 25 3.14 10.5")

        tipos = [t["tipo"] for t in resultado["tokens"]]

        self.assertEqual(tipos, [
            "LITERAL_INTEIRO",
            "LITERAL_INTEIRO",
            "LITERAL_REAL",
            "LITERAL_REAL"
        ])

    def test_numeros_invalidos(self):
        for codigo in ["123abc", "12."]:
            with self.subTest(codigo=codigo):
                resultado = analisar_lexico(codigo)

                self.assertFalse(resultado["sucesso"])
                self.assertGreater(len(resultado["erros"]), 0)

    def test_strings(self):
        resultado = analisar_lexico(
            """nome = "Python"
mensagem = 'Ola'"""
        )

        strings = [
            t for t in resultado["tokens"]
            if t["tipo"] == "LITERAL_STRING"
        ]

        self.assertEqual(len(strings), 2)
        self.assertTrue(resultado["sucesso"])

    def test_string_nao_fechada(self):
        resultado = analisar_lexico('nome = "Python')

        self.assertFalse(resultado["sucesso"])
        self.assertEqual(len(resultado["erros"]), 1)
        self.assertIn(
            "String não fechada",
            resultado["erros"][0]["mensagem"]
        )

    def test_operadores(self):
        operadores = [
            "+", "-", "*", "/", "=",
            "==", "!=", "<", ">", "<=", ">="
        ]

        for operador in operadores:
            with self.subTest(operador=operador):
                resultado = analisar_lexico(operador)

                self.assertTrue(resultado["sucesso"])
                self.assertEqual(len(resultado["tokens"]), 1)
                self.assertEqual(
                    resultado["tokens"][0]["lexema"],
                    operador
                )
                self.assertEqual(
                    resultado["tokens"][0]["tipo"],
                    "OPERADOR"
                )

    def test_delimitadores(self):
        resultado = analisar_lexico("( ) : ,")

        self.assertEqual(len(resultado["tokens"]), 4)

        for token in resultado["tokens"]:
            self.assertEqual(token["tipo"], "DELIMITADOR")

    def test_comentarios(self):
        codigo = """idade = 20 # comentario
resultado = 10"""

        resultado = analisar_lexico(codigo)

        lexemas = [t["lexema"] for t in resultado["tokens"]]

        self.assertNotIn("#", lexemas)
        self.assertNotIn("comentario", lexemas)
        self.assertIn("resultado", lexemas)
        self.assertTrue(resultado["sucesso"])

    def test_espacos_em_branco(self):
        resultado = analisar_lexico("   idade   =   20   ")

        self.assertEqual(len(resultado["tokens"]), 3)
        self.assertTrue(resultado["sucesso"])

    def test_linha_e_coluna(self):
        codigo = "idade = 20\n  total = 5"
        resultado = analisar_lexico(codigo)

        primeiro = resultado["tokens"][0]
        self.assertEqual(primeiro["linha"], 1)
        self.assertEqual(primeiro["coluna"], 1)

        segundo = resultado["tokens"][3]
        self.assertEqual(segundo["lexema"], "total")
        self.assertEqual(segundo["linha"], 2)
        self.assertEqual(segundo["coluna"], 3)

    def test_caractere_invalido(self):
        resultado = analisar_lexico("idade @ 20")

        self.assertFalse(resultado["sucesso"])
        self.assertEqual(len(resultado["erros"]), 1)

        erro = resultado["erros"][0]

        self.assertEqual(erro["lexema"], "@")
        self.assertEqual(erro["linha"], 1)
        self.assertEqual(erro["coluna"], 7)

        # O scanner deve continuar após o erro
        lexemas = [t["lexema"] for t in resultado["tokens"]]
        self.assertIn("20", lexemas)

    def test_codigo_vazio(self):
        resultado = analisar_lexico("")

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["tokens"], [])
        self.assertEqual(resultado["erros"], [])

    def test_apenas_comentario(self):
        resultado = analisar_lexico("# apenas comentario")

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["tokens"], [])

    def test_token_final_sem_quebra_de_linha(self):
        resultado = analisar_lexico("resultado")

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(len(resultado["tokens"]), 1)
        self.assertEqual(
            resultado["tokens"][0]["lexema"],
            "resultado"
        )


if __name__ == "__main__":
    unittest.main()
