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
            console.log("Usuário logado, enviando dados...")
        }

	})
}