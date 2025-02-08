let cartItems = 0;
const cartCount = document.getElementById('cartCount');

function addToCart() {
    cartItems++;
    cartCount.textContent = cartItems;
    cartCount.classList.add('show');
    setTimeout(() => cartCount.classList.remove('show'), 300);
}

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
}

