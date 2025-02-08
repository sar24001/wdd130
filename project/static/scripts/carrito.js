

async function guardar_producto(id_producto, stock) {


    console.log(id_producto);
    console.log(stock);
    await axios.post('/producto_carrito',
        {producto_id: id_producto,
            cantidad: stock})
        .then(response => {
            console.log("Mostrando modal");

        })
        .catch(error => {
            console.error("Error al guardar el carrito:", error.response ? error.response.data : error);
        });
}
