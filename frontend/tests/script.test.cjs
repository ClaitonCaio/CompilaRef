
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const script = fs.readFileSync(
    path.join(__dirname, "..", "script.js"),
    "utf8"
);

// Simula os elementos HTML da interface
function criarElemento() {
    let texto = "";

    return {
        value: "",
        disabled: false,
        hidden: false,
        style: {},
        children: [],
        eventos: {},

        get textContent() {
            return texto;
        },

        set textContent(valor) {
            texto = String(valor);
            this.children = [];
        },

        appendChild(elemento) {
            this.children.push(elemento);
        },

        addEventListener(nome, funcao) {
            this.eventos[nome] = funcao;
        },

        focus() {
            this.focado = true;
        }
    };
}

// Prepara a interface para os testes
function prepararInterface(respostaFetch) {
    const ids = [
        "codigo",
        "exemplos",
        "analisar",
        "mensagem",
        "resultado",
        "corpo-tokens",
        "secao-erros",
        "lista-erros"
    ];

    const elementos = {};

    ids.forEach(id => {
        elementos[id] = criarElemento();
    });

    elementos["secao-erros"].hidden = true;

    let inicializar;

    const document = {
        addEventListener(nome, funcao) {
            if (nome === "DOMContentLoaded") {
                inicializar = funcao;
            }
        },

        getElementById(id) {
            return elementos[id];
        },

        createElement() {
            return criarElemento();
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
        fetch: respostaFetch || (async () => {
            throw new Error("Servidor indisponível");
        })
    });

    inicializar();

    return elementos;
}

// TESTE 1
test("Carrega os tres exemplos de Python", () => {
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

// TESTE 2
test("Permite editar o codigo", () => {
    const tela = prepararInterface();

    tela.codigo.value = "numero = 100";

    assert.equal(tela.codigo.value, "numero = 100");
});

// TESTE 3
test("Impede envio de codigo vazio ou espacos", async () => {
    let chamadas = 0;

    const tela = prepararInterface(async () => {
        chamadas++;
    });

    for (const entrada of ["", "   ", "\n\t"]) {
        tela.codigo.value = entrada;

        await tela.analisar.eventos.click();

        assert.match(
            tela.mensagem.textContent,
            /Informe um código-fonte/
        );
    }

    assert.equal(chamadas, 0);
});

// TESTE 4
test("Envia codigo e exibe os tokens na tabela", async () => {
    const tela = prepararInterface(async () => ({
        ok: true,

        async json() {
            return {
                mensagem: "Análise léxica concluída com sucesso!",
                sucesso: true,
                tokens: [
                    {
                        tipo: "IDENTIFICADOR",
                        lexema: "idade",
                        linha: 1,
                        coluna: 1
                    },
                    {
                        tipo: "OPERADOR",
                        lexema: "=",
                        linha: 1,
                        coluna: 7
                    },
                    {
                        tipo: "LITERAL_INTEIRO",
                        lexema: "20",
                        linha: 1,
                        coluna: 9
                    }
                ],
                erros: []
            };
        }
    }));

    tela.codigo.value = "idade = 20";

    await tela.analisar.eventos.click();

    const linhas = tela["corpo-tokens"].children;

    assert.equal(linhas.length, 3);

    assert.equal(
        linhas[0].children[0].textContent,
        "IDENTIFICADOR"
    );

    assert.equal(
        linhas[0].children[1].textContent,
        "idade"
    );

    assert.equal(
        linhas[0].children[2].textContent,
        "1"
    );

    assert.equal(
        linhas[0].children[3].textContent,
        "1"
    );

    assert.match(
        tela.mensagem.textContent,
        /sucesso/
    );

    assert.equal(tela.analisar.disabled, false);
});

// TESTE 5
test("Exibe erros lexicos e continua mostrando tokens", async () => {
    const tela = prepararInterface(async () => ({
        ok: true,

        async json() {
            return {
                mensagem: "Análise concluída com erros léxicos.",
                sucesso: false,
                tokens: [
                    {
                        tipo: "IDENTIFICADOR",
                        lexema: "idade",
                        linha: 1,
                        coluna: 1
                    },
                    {
                        tipo: "LITERAL_INTEIRO",
                        lexema: "20",
                        linha: 1,
                        coluna: 9
                    }
                ],
                erros: [
                    {
                        tipo: "ERRO_LEXICO",
                        lexema: "@",
                        linha: 1,
                        coluna: 7,
                        mensagem: "Caractere não reconhecido: '@'"
                    }
                ]
            };
        }
    }));

    tela.codigo.value = "idade @ 20";

    await tela.analisar.eventos.click();

    assert.equal(
        tela["corpo-tokens"].children.length,
        2
    );

    assert.equal(
        tela["secao-erros"].hidden,
        false
    );

    assert.match(
        tela["lista-erros"].children[0].textContent,
        /Linha 1, coluna 7/
    );

    assert.match(
        tela["lista-erros"].children[0].textContent,
        /@/
    );
});

// TESTE 6
test("Mostra mensagem quando servidor falha", async () => {
    const tela = prepararInterface(async () => {
        throw new Error("Falha de conexão");
    });

    tela.codigo.value = "idade = 20";

    await tela.analisar.eventos.click();

    assert.match(
        tela.mensagem.textContent,
        /Não foi possível comunicar/
    );

    assert.equal(tela.analisar.disabled, false);
});

// TESTE 7
test("Trata resposta HTTP de erro", async () => {
    const tela = prepararInterface(async () => ({
        ok: false,

        async json() {
            return {
                mensagem: "Requisição inválida."
            };
        }
    }));

    tela.codigo.value = "idade = 20";

    await tela.analisar.eventos.click();

    assert.equal(
        tela.mensagem.textContent,
        "Requisição inválida."
    );

    assert.equal(tela.analisar.disabled, false);
});

// TESTE 8
test("Mostra mensagem quando nao existem tokens", async () => {
    const tela = prepararInterface(async () => ({
        ok: true,

        async json() {
            return {
                mensagem: "Análise léxica concluída com sucesso!",
                sucesso: true,
                tokens: [],
                erros: []
            };
        }
    }));

    tela.codigo.value = "# comentario";

    await tela.analisar.eventos.click();

    const linhas = tela["corpo-tokens"].children;

    assert.equal(linhas.length, 1);

    assert.match(
        linhas[0].children[0].textContent,
        /Nenhum token identificado/
    );
});

// TESTE 9
test("Limpa resultados ao selecionar outro exemplo", async () => {
    const tela = prepararInterface(async () => ({
        ok: true,

        async json() {
            return {
                mensagem: "Análise concluída com erros léxicos.",
                sucesso: false,
                tokens: [
                    {
                        tipo: "IDENTIFICADOR",
                        lexema: "idade",
                        linha: 1,
                        coluna: 1
                    }
                ],
                erros: [
                    {
                        linha: 1,
                        coluna: 7,
                        mensagem: "Caractere não reconhecido."
                    }
                ]
            };
        }
    }));

    tela.codigo.value = "idade @";

    await tela.analisar.eventos.click();

    tela.exemplos.value = "2";
    tela.exemplos.eventos.change();

    assert.equal(
        tela.codigo.value,
        "resultado = 10 + 5"
    );

    assert.equal(
        tela["corpo-tokens"].children.length,
        0
    );

    assert.equal(
        tela["secao-erros"].hidden,
        true
    );
});
