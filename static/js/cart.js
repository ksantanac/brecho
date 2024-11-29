var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)

        console.log("USER:", user)
        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }

	})
}

function addCookieItem(productId, action){
    console.log("Usuário não logado...")

    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity' : 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item.')
            delete cart[productId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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

// var updateBtns = document.getElementsByClassName('update-cart');

// // Adiciona evento de clique a cada botão "update-cart"
// for (let i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function () {
//         // Obtém os valores de data-* do botão clicado
//         var productId = this.dataset.product;
//         var action = this.dataset.action;

//         console.log('Produto ID:', productId, 'Ação:', action);
//         console.log("Usuário:", user);

//         // Verifica se o usuário é anônimo
//         if (user === 'AnonymousUser') {
//             alert("Você precisa estar logado para adicionar itens ao carrinho ou finalizar a compra!");
//             window.location.href = '/login/'; // Redireciona para a página de login
//         } else {
//             // Atualiza o pedido do usuário logado
//             updateUserOrder(productId, action);
//         }
//     });
// }

// // Função para atualizar o pedido do usuário logado
// function updateUserOrder(productId, action) {
//     console.log("Usuário autenticado, enviando dados para o backend...");

//     var url = '/update_item/';

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         body: JSON.stringify({ 'productId': productId, 'action': action })
//     })
//         .then((response) => {
//             return response.json();
//         })
//         .then((data) => {
//             console.log('Resposta do servidor:', data);
//             location.reload();
//         });
// }
