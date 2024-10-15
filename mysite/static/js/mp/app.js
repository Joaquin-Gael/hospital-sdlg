// npm install mercadopago express cors

const mp = new MercadoPago('APP_USR-b71e6b99-dc4c-4986-b0ed-622fb2717f4c', {
    // Lenguaje en el que funcionara la integración.
    locale: "es-AR",
});

// Seleccionamos el objeto que contiene el ID "checkout-btn" y añadimos un evento al momento que el usuario haga click en el boton.
document.getElementById("checkout-btn").addEventListener("click", async ()=>{
    try{
        const orderData = {
            //Pedimos de manera dinamica los datos del producto con un query selector, el cual tomara el objeto que tenga la clase "nameService" el texto del mismo.
            title: document.querySelector(".nameService").innerText,
            price: 10
        };
    
        // Envia al servidor la información del producto (await para manejar asincronía)
        const response = await fetch("http://127.0.0.1:8000/create_preference",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // Convertimos JSON a String para evitar conflictos
            body: JSON.stringify(orderData)
        });

        // Obtenemos la preferencia y su ID. La función creara el boton de compra apartir de los datos que ha recibido mediante ese ID.
        const preference = await response.json();
        createCheckoutButton(preference.id);
    } catch(error){
        alert("Error: ");
    }
});

const createCheckoutButton = (preferenceId) => {
    const brickBuilders = mp.bricks();

    /* Creamos una función que va a montar un wallet al objeto que tenga asignada el ID "wallet-container" y lo inicializa con el
    preferenceID
    */
    const renderComponent = async () => {
        // Evitamos que el usuario cree otro boton para pagar con MercadoPago (Métodos de MercadoPago)
        if (window.checkoutButton) window.checkoutButton.unmount();
        window.checkoutButton = await bricksBuilder.create("wallet", "wallet-container", {
            inizialization: {
                preferenceId: preferenceId,
            },
        });
    };

    renderComponent();

}