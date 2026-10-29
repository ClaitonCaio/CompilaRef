
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Rota da primeira etapa
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, World!"})


# Rota para receber o código-fonte
@app.route("/analisar", methods=["POST"])
def analisar():

    # Receber os dados enviados pelo frontend
    dados = request.get_json(silent=True)

    # Verificar se a requisição contém um objeto JSON
    if not isinstance(dados, dict):
        return jsonify({
            "mensagem": "Requisição inválida.",
            "recebido": False
        }), 400

    codigo = dados.get("codigo")

    # Verificar se o campo é um texto
    if not isinstance(codigo, str):
        return jsonify({
            "mensagem": "O código-fonte deve ser um texto.",
            "recebido": False
        }), 400

    # Verificar se o código está vazio
    if not codigo.strip():
        return jsonify({
            "mensagem": "Informe um código-fonte antes de solicitar a análise.",
            "recebido": False
        }), 400

    # Confirmar o recebimento do código
    return jsonify({
        "mensagem": "Código recebido com sucesso!",
        "recebido": True,
        "codigo": codigo
    }), 200


# Iniciar o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
