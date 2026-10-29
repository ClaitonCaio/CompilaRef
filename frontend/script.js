
document.addEventListener("DOMContentLoaded", () => {

    const codigo = document.getElementById("codigo");
    const exemplos = document.getElementById("exemplos");
    const botao = document.getElementById("analisar");
    const mensagem = document.getElementById("mensagem");
    const resultado = document.getElementById("resultado");

    // Elementos da Etapa 3
    const corpoTokens = document.getElementById("corpo-tokens");
    const secaoErros = document.getElementById("secao-erros");
    const listaErros = document.getElementById("lista-erros");

    // Exemplos em Python simplificado
    const programas = {
        "1": "idade = 20",
        "2": "resultado = 10 + 5",
        "3": "total = (10 + 5) * 2"
    };

    mensagem.textContent = "Insira um código ou selecione um exemplo.";

    // Limpar a tabela de tokens
    function limparTabela() {
        if (!corpoTokens) return;

        corpoTokens.textContent = "";
    }

    // Exibir os tokens encontrados
    function mostrarTokens(tokens) {
        if (!corpoTokens) return;

        limparTabela();

        if (tokens.length === 0) {
            const linha = document.createElement("tr");
            const celula = document.createElement("td");

            celula.colSpan = 4;
            celula.textContent = "Nenhum token identificado.";

            linha.appendChild(celula);
            corpoTokens.appendChild(linha);
            return;
        }

        tokens.forEach(token => {
            const linha = document.createElement("tr");

            const valores = [
                token.tipo,
                token.lexema,
                token.linha,
                token.coluna
            ];

            valores.forEach(valor => {
                const celula = document.createElement("td");

                celula.textContent = String(valor);
                linha.appendChild(celula);
            });

            corpoTokens.appendChild(linha);
        });
    }

    // Exibir os erros léxicos
    function mostrarErros(erros) {
        if (!secaoErros || !listaErros) return;

        listaErros.textContent = "";

        if (erros.length === 0) {
            secaoErros.hidden = true;
            return;
        }

        secaoErros.hidden = false;

        erros.forEach(erro => {
            const item = document.createElement("li");

            item.textContent =
                `Linha ${erro.linha}, coluna ${erro.coluna}: ${erro.mensagem}`;

            listaErros.appendChild(item);
        });
    }

    // Carregar os exemplos no editor
    exemplos.addEventListener("change", () => {
        const exemplo = programas[exemplos.value];

        if (exemplo) {
            codigo.value = exemplo;

            mensagem.textContent =
                "Exemplo carregado. Você pode editá-lo.";

            mensagem.style.color = "#333";

            resultado.textContent =
                "Nenhuma análise solicitada.";

            limparTabela();
            mostrarErros([]);
        }
    });

    // Executar análise léxica
    botao.addEventListener("click", async () => {

        const fonte = codigo.value;

        // Verificar código vazio
        if (!fonte.trim()) {
            mensagem.textContent =
                "Informe um código-fonte antes de solicitar a análise.";

            mensagem.style.color = "#b91c1c";

            resultado.textContent = "Nenhum código enviado.";

            limparTabela();
            mostrarErros([]);

            codigo.focus();
            return;
        }

        // Preparar a interface
        botao.disabled = true;

        mensagem.textContent = "Executando análise léxica...";
        mensagem.style.color = "#333";

        resultado.textContent =
            "Aguardando resposta do servidor...";

        limparTabela();
        mostrarErros([]);

        try {
            const endereco =
                `${window.location.protocol}//${window.location.hostname}:5000/analisar`;

            // Enviar o código para o backend
            const resposta = await fetch(endereco, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    codigo: fonte
                })
            });

            const dados = await resposta.json();

            // Tratar requisição rejeitada
            if (!resposta.ok) {
                mensagem.textContent =
                    dados.mensagem ||
                    "Não foi possível processar a solicitação.";

                mensagem.style.color = "#b91c1c";

                resultado.textContent =
                    "Verifique os dados enviados.";

                return;
            }

            // Receber tokens e erros
            const tokens = Array.isArray(dados.tokens)
                ? dados.tokens
                : [];

            const erros = Array.isArray(dados.erros)
                ? dados.erros
                : [];

            // Preencher a tabela
            mostrarTokens(tokens);

            // Apresentar os erros
            mostrarErros(erros);

            // Mostrar o resultado da análise
            if (dados.sucesso === false || erros.length > 0) {
                mensagem.textContent =
                    dados.mensagem ||
                    "Análise concluída com erros léxicos.";

                mensagem.style.color = "#b91c1c";
            } else {
                mensagem.textContent =
                    dados.mensagem ||
                    "Análise léxica concluída com sucesso!";

                mensagem.style.color = "#15803d";
            }

            // Mostrar o código original e a contagem
            resultado.textContent =
                "Código enviado:\n\n" +
                fonte +
                "\n\nTotal de tokens: " +
                tokens.length;

        } catch (erro) {

            mensagem.textContent =
                "Não foi possível comunicar com o servidor.";

            mensagem.style.color = "#b91c1c";

            resultado.textContent =
                "Verifique a conexão e tente novamente.";

            limparTabela();
            mostrarErros([]);

        } finally {
            botao.disabled = false;
        }
    });
});
