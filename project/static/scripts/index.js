const vetIcons = [
    '🐾', '🐶', '🐱', '💉', '🩺', '🦴', '🐰', '🐦', '🐠', '🐹'
];

function createIcon() {
    const icon = document.createElement('div');
    icon.classList.add('vet-icon');
    icon.textContent = vetIcons[Math.floor(Math.random() * vetIcons.length)];
    icon.style.left = Math.random() * 100 + 'vw';
    icon.style.top = Math.random() * 100 + 'vh';
    icon.style.fontSize = Math.random() * (30 - 10) + 10 + 'px';
    document.body.appendChild(icon);

    const duration = Math.random() * (15 - 5) + 5;
    const direction = Math.random() < 0.5 ? 1 : -1;

    function moveIcon() {
        const currentTop = parseFloat(icon.style.top);
        icon.style.top = (currentTop + direction * 0.5) + 'vh';

        if (currentTop < -10 || currentTop > 110) {
            document.body.removeChild(icon);
            createIcon();
        } else {
            requestAnimationFrame(moveIcon);
        }
    }

    moveIcon();

    setTimeout(() => {
        if (document.body.contains(icon)) {
            document.body.removeChild(icon);
            createIcon();
        }
    }, duration * 1000);
}

// Create initial set of icons
for (let i = 0; i < 20; i++) {
    createIcon();
}

document.addEventListener('DOMContentLoaded', (event) => {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    // Cerrar el menú al hacer clic en un enlace
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });
});
