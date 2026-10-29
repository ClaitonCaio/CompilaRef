
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const script = fs.readFileSync(
    path.join(__dirname, "..", "script.js"),
    "utf8"
);

function prepararInterface(respostaFetch) {
    function elemento() {
        return {
            value: "",
            textContent: "",
            disabled: false,
            style: {},
            eventos: {},
            addEventListener(nome, funcao) {
                this.eventos[nome] = funcao;
            },
            focus() {}
        };
    }

    const elementos = {
        codigo: elemento(),
        exemplos: elemento(),
        analisar: elemento(),
        mensagem: elemento(),
        resultado: elemento()
    };

    let inicializar;

    const document = {
        addEventListener(nome, funcao) {
            if (nome === "DOMContentLoaded") {
                inicializar = funcao;
            }
        },
        getElementById(id) {
            return elementos[id];
        }
    };

    const window = {
        location: {
            protocol: "http:",
            hostname: "localhost"
        }
    };

    vm.runInNewContext(script, {
        document,
        window,
        fetch: respostaFetch
    });

    inicializar();
    return elementos;
}

test("Carrega os tres exemplos", () => {
    const tela = prepararInterface();

    const exemplos = {
        "1": "idade = 20",
        "2": "resultado = 10 + 5",
        "3": "total = (10 + 5) * 2"
    };

    for (const [numero, codigo] of Object.entries(exemplos)) {
        tela.exemplos.value = numero;
        tela.exemplos.eventos.change();

        assert.equal(tela.codigo.value, codigo);
    }
});

test("Permite editar o codigo", () => {
    const tela = prepararInterface();

    tela.codigo.value = "numero = 100";

    assert.equal(tela.codigo.value, "numero = 100");
});

test("Impede o envio de codigo vazio", async () => {
    let enviou = false;

    const tela = prepararInterface(async () => {
        enviou = true;
    });

    tela.codigo.value = "   ";
    await tela.analisar.eventos.click();

    assert.equal(enviou, false);
    assert.match(tela.mensagem.textContent, /Informe um código/);
});

test("Envia o codigo ao backend", async () => {
    let dadosEnviados;

    const tela = prepararInterface(async (url, opcoes) => {
        dadosEnviados = JSON.parse(opcoes.body);

        return {
            ok: true,
            async json() {
                return {
                    mensagem: "Código recebido com sucesso!",
                    recebido: true
                };
            }
        };
    });

    tela.codigo.value = "idade = 20";
    await tela.analisar.eventos.click();

    assert.equal(dadosEnviados.codigo, "idade = 20");
    assert.match(tela.mensagem.textContent, /sucesso/);
    assert.equal(tela.analisar.disabled, false);
});

test("Mostra erro quando o servidor falha", async () => {
    const tela = prepararInterface(async () => {
        throw new Error("Servidor indisponivel");
    });

    tela.codigo.value = "idade = 20";
    await tela.analisar.eventos.click();

    assert.match(
        tela.mensagem.textContent,
        /Não foi possível comunicar/
    );
    assert.equal(tela.analisar.disabled, false);
});

test("Mostra erro quando o backend rejeita a entrada", async () => {
    const tela = prepararInterface(async () => ({
        ok: false,
        async json() {
            return { mensagem: "Requisição inválida." };
        }
    }));

    tela.codigo.value = "idade = 20";
    await tela.analisar.eventos.click();

    assert.equal(tela.mensagem.textContent, "Requisição inválida.");
    assert.equal(tela.analisar.disabled, false);
});
