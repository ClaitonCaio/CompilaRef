
document.addEventListener("DOMContentLoaded", () => {

    const codigo = document.getElementById("codigo");
    const exemplos = document.getElementById("exemplos");
    const botao = document.getElementById("analisar");
    const mensagem = document.getElementById("mensagem");
    const resultado = document.getElementById("resultado");

    // Exemplos em Python simplificado
    const programas = {
        "1": "idade = 20",
        "2": "resultado = 10 + 5",
        "3": "total = (10 + 5) * 2"
    };

    mensagem.textContent = "Insira um código ou selecione um exemplo.";

    // Carregar exemplos no editor
    exemplos.addEventListener("change", () => {
        const exemplo = programas[exemplos.value];

        if (exemplo) {
            codigo.value = exemplo;
            mensagem.textContent = "Exemplo carregado. Você pode editá-lo.";
            resultado.textContent = "Nenhuma análise solicitada.";
        }
    });

    // Solicitar análise ao backend
    botao.addEventListener("click", async () => {

        const fonte = codigo.value;

        // Verificar entrada vazia
        if (!fonte.trim()) {
            mensagem.textContent = "Informe um código-fonte antes de solicitar a análise.";
            mensagem.style.color = "#b91c1c";
            resultado.textContent = "Nenhum código enviado.";
            codigo.focus();
            return;
        }

        botao.disabled = true;
        mensagem.textContent = "Enviando código...";
        mensagem.style.color = "#333";
        resultado.textContent = "Aguardando resposta do servidor...";

        try {
            const endereco = `${window.location.protocol}//${window.location.hostname}:5000/analisar`;

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

            if (!resposta.ok) {
                mensagem.textContent = dados.mensagem || "Não foi possível processar a solicitação.";
                mensagem.style.color = "#b91c1c";
                resultado.textContent = "Verifique os dados enviados.";
                return;
            }

            mensagem.textContent = dados.mensagem || "Código recebido com sucesso.";
            mensagem.style.color = "#15803d";

            resultado.textContent = "Código enviado:\n\n" + fonte;

        } catch (erro) {
            mensagem.textContent = "Não foi possível comunicar com o servidor.";
            mensagem.style.color = "#b91c1c";
            resultado.textContent = "Verifique a conexão e tente novamente.";
        } finally {
            botao.disabled = false;
        }
    });
});
