
import unittest
from app import app


class TestCompilaRef(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_hello_world(self):
        resposta = self.cliente.get("/hello")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.get_json()["message"],
            "Hello, World!"
        )

    def test_codigo_valido(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "idade = 20"}
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(
            resposta.get_json()["recebido"]
        )

    def test_codigo_aritmetico(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "resultado = 10 + 5"}
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.get_json()["codigo"],
            "resultado = 10 + 5"
        )

    def test_codigo_vazio(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": ""}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_codigo_apenas_espacos(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": "    "}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_campo_ausente(self):
        resposta = self.cliente.post(
            "/analisar",
            json={}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_codigo_invalido(self):
        resposta = self.cliente.post(
            "/analisar",
            json={"codigo": 123}
        )

        self.assertEqual(resposta.status_code, 400)

    def test_requisicao_invalida(self):
        resposta = self.cliente.post(
            "/analisar",
            data="texto invalido",
            content_type="text/plain"
        )

        self.assertEqual(resposta.status_code, 400)


if __name__ == "__main__":
    unittest.main()
