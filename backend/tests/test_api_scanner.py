
import unittest
from app import app


class TestAPIScanner(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_analise_valida(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade = 20"}
        )

        dados = resposta.get_json()

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(dados["sucesso"])
        self.assertTrue(dados["recebido"])
        self.assertEqual(len(dados["tokens"]), 3)
        self.assertEqual(dados["erros"], [])

    def test_classificacao_tokens(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "resultado = 10 + 5"}
        )

        tokens = resposta.get_json()["tokens"]

        tipos = [token["tipo"] for token in tokens]

        self.assertEqual(tipos, [
            "IDENTIFICADOR",
            "OPERADOR",
            "LITERAL_INTEIRO",
            "OPERADOR",
            "LITERAL_INTEIRO"
        ])

    def test_posicao_tokens(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade = 20\n  total = 5"}
        )

        tokens = resposta.get_json()["tokens"]

        self.assertEqual(tokens[0]["linha"], 1)
        self.assertEqual(tokens[0]["coluna"], 1)
        self.assertEqual(tokens[3]["linha"], 2)
        self.assertEqual(tokens[3]["coluna"], 3)

    def test_caractere_invalido(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade @ 20"}
        )

        dados = resposta.get_json()

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(dados["sucesso"])
        self.assertEqual(len(dados["erros"]), 1)
        self.assertEqual(dados["erros"][0]["lexema"], "@")

    def test_continua_apos_erro(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade @ 20"}
        )

        dados = resposta.get_json()
        lexemas = [t["lexema"] for t in dados["tokens"]]

        self.assertIn("idade", lexemas)
        self.assertIn("20", lexemas)

    def test_codigo_vazio(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": ""}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_apenas_espacos(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "   "}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_requisicao_invalida(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": 123}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_formato_resposta(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade = 20"}
        )

        dados = resposta.get_json()

        for campo in [
            "mensagem", "recebido", "codigo",
            "sucesso", "tokens", "erros"
        ]:
            self.assertIn(campo, dados)

        for campo in ["tipo", "lexema", "linha", "coluna"]:
            self.assertIn(campo, dados["tokens"][0])


if __name__ == "__main__":
    unittest.main()
