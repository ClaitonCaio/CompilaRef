
from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import analisar_lexico
from parser import analisar_sintatico

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

    if len(codigo) > 10000:
        return jsonify({
            "mensagem": "O código deve ter no máximo 10.000 caracteres.",
            "recebido": False
        }), 400

    # Executar o scanner
    resultado = analisar_lexico(codigo)
    sintatico = (analisar_sintatico(resultado["tokens"], codigo)
                 if resultado["sucesso"] else
                 {"sucesso": False, "ast": None, "erros": [], "ignorado": True})

    # Verificar se houve erros léxicos
    if resultado["sucesso"] and sintatico["sucesso"]:
        mensagem = "Análises léxica e sintática concluídas com sucesso!"
    elif resultado["sucesso"]:
        mensagem = "Análise sintática concluída com erro."
    else:
        mensagem = "Análise concluída com erros léxicos."

    # Retornar os resultados para o frontend
    return jsonify({
        "mensagem": mensagem,
        "recebido": True,
        "codigo": codigo,
        "sucesso": resultado["sucesso"],
        "tokens": resultado["tokens"],
        "erros": resultado["erros"],
        "lexico": resultado,
        "sintatico": sintatico
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
