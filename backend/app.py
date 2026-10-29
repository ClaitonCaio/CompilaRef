
from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import analisar_lexico

app = Flask(__name__)
CORS(app)


# Rota mantida da Etapa 1
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Hello, World!"
    })


# Rota de análise do código-fonte
@app.route("/analisar", methods=["POST"])
def analisar():

    dados = request.get_json(silent=True)

    # Verificar requisição inválida
    if not isinstance(dados, dict):
        return jsonify({
            "mensagem": "Requisição inválida.",
            "recebido": False
        }), 400

    codigo = dados.get("codigo")

    # Verificar o tipo da entrada
    if not isinstance(codigo, str):
        return jsonify({
            "mensagem": "O código-fonte deve ser um texto.",
            "recebido": False
        }), 400

    # Verificar código vazio ou apenas espaços
    if not codigo.strip():
        return jsonify({
            "mensagem": "Informe um código-fonte antes de solicitar a análise.",
            "recebido": False
        }), 400

    # Executar o scanner
    resultado = analisar_lexico(codigo)

    # Verificar se houve erros léxicos
    if resultado["sucesso"]:
        mensagem = "Análise léxica concluída com sucesso!"
    else:
        mensagem = "Análise concluída com erros léxicos."

    # Retornar os resultados para o frontend
    return jsonify({
        "mensagem": mensagem,
        "recebido": True,
        "codigo": codigo,
        "sucesso": resultado["sucesso"],
        "tokens": resultado["tokens"],
        "erros": resultado["erros"]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
