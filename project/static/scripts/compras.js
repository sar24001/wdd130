document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const productName = this.parentElement.querySelector('.product-name').textContent;
        alert(`¡${productName} añadido al carrito!`);
    });
});
