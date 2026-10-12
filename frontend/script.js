fetch("http://localhost:5000/hello")
    .then(response => response.json())
    .then(data => {
        document.getElementById("mensagem").innerText = data.message;
    })
    .catch(() => {
        document.getElementById("mensagem").innerText =
            "Erro ao conectar com o backend.";
    });