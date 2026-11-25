import unittest

from app import app


class TestAPIParser(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_valido_e_compatibilidade(self):
        resposta = self.cliente.post("/analisar", json={"codigo": "x = 2 + 3 * 4"})
        dados = resposta.get_json()
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(dados["tokens"]), 7)
        self.assertEqual(dados["tokens"], dados["lexico"]["tokens"])
        self.assertTrue(dados["sucesso"])
        self.assertTrue(dados["sintatico"]["sucesso"])
        self.assertEqual(dados["sintatico"]["ast"]["tipo"], "PROGRAMA")

    def test_erro_sintatico(self):
        dados = self.cliente.post("/analisar", json={"codigo": "x = 2 +"}).get_json()
        self.assertEqual(dados["erros"], [])  # campo legado: apenas erros léxicos
        self.assertFalse(dados["sintatico"]["sucesso"])
        self.assertIsNone(dados["sintatico"]["ast"])
        self.assertEqual(dados["sintatico"]["erros"][0]["linha"], 1)

    def test_erro_lexico_impede_parser(self):
        dados = self.cliente.post("/analisar", json={"codigo": "x = 2 @ 3"}).get_json()
        self.assertFalse(dados["lexico"]["sucesso"])
        self.assertTrue(dados["sintatico"]["ignorado"])
        self.assertIsNone(dados["sintatico"]["ast"])

    def test_entrada_invalida_e_limite(self):
        for codigo in ("", "   ", 42, "a" * 10001):
            with self.subTest(codigo=str(codigo)[:12]):
                self.assertEqual(self.cliente.post("/analisar", json={"codigo": codigo}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
