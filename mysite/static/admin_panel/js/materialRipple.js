// materialRipple.js

export function addRippleEffect(element) {
    element.addEventListener('click', function (e) {
        // Crea un span para el efecto ripple
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');

        // Obtener la posición del clic y dimensiones del botón
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        // Establecer estilos para el efecto ripple
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        // Agregar el ripple al botón
        element.appendChild(ripple);

        // Eliminar el ripple después de la animación
        ripple.addEventListener('animationend', () => {
            ripple.remove();
        });
    });
}

// Función para aplicar el efecto a todos los botones con la clase 'btn'
export function applyRippleToButtons() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((button) => {
        addRippleEffect(button);
    });
}

export function applyRippleToNavLink(){
    const buttons = document.querySelectorAll('.nav-link')
    buttons.forEach((button) => {
        addRippleEffect(button)
    });
}