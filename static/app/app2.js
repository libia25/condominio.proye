// Limpiar el historial al salir de la página
window.onload = function() {
    history.pushState(null, document.title, location.href);
    window.addEventListener('popstate', function () {
        history.pushState(null, document.title, location.href);
    });
};
