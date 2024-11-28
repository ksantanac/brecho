var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)

        console.log("USER:", user)
        if(user === "AnonymousUser"){
            console.log("Usuário não logado.")
        }else{
            updateUserOrder(productId, action)
        }

	})
}

function updateUserOrder(productId, action) {
    // Exibe no console uma mensagem indicando que os dados estão sendo enviados
    console.log("Usuário logado, enviando dados...")

    // Define a URL do endpoint que será chamado
    var url = '/update_item/'

    // Faz uma solicitação HTTP POST para a URL definida
    fetch(url, {
        method: 'POST', // Método HTTP usado para enviar dados ao servidor
        headers: {
            'Content-Type': 'application/json', // Indica que o conteúdo é JSON
            'X-CSRFToken': csrftoken // Token CSRF para evitar ataques de CSRF
        },
        body: JSON.stringify({'productId': productId, 'action': action}) 
        // Converte os dados do produto e da ação em uma string JSON e os inclui no corpo da solicitação
    })

    // Lida com a resposta da solicitação
    .then((response) => {
        // Retorna a resposta como JSON para a próxima etapa
        return response.json()
    })

    .then((data) => {
        // Exibe os dados retornados pelo servidor no console
        console.log('data:', data)
        console.log('Reloading the page...')
        location.reload()
    })
}