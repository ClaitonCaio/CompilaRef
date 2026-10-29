
import unittest
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

URL = "http://127.0.0.1:5000"


class TestIntegracao(unittest.TestCase):

    def enviar_codigo(self, dados):
        requisicao = Request(
            URL + "/analisar",
            data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        return urlopen(requisicao, timeout=10)

    def test_backend_disponivel(self):
        with urlopen(URL + "/hello", timeout=10) as resposta:
            self.assertEqual(resposta.status, 200)

            dados = json.load(resposta)
            self.assertEqual(dados["message"], "Hello, World!")

    def test_envio_codigo(self):
        with self.enviar_codigo({"codigo": "idade = 20"}) as resposta:
            self.assertEqual(resposta.status, 200)

            dados = json.load(resposta)
            self.assertTrue(dados["recebido"])
            self.assertEqual(dados["codigo"], "idade = 20")

    def test_codigo_vazio(self):
        with self.assertRaises(HTTPError) as erro:
            self.enviar_codigo({"codigo": ""})

        self.assertEqual(erro.exception.code, 400)
        erro.exception.close()

    def test_requisicao_invalida(self):
        with self.assertRaises(HTTPError) as erro:
            self.enviar_codigo({"codigo": 123})

        self.assertEqual(erro.exception.code, 400)
        erro.exception.close()


if __name__ == "__main__":
    unittest.main()
