// Verifica si el usuario ya ha visitado el dashboard
window.onload = function() {
    // Si el usuario ya ha visitado el dashboard, redirige a base.html
    if (localStorage.getItem("visitedDashboard") === "true") {
        // Redirige a base.html
        window.location.href = "index"; // Cambia a la ruta correcta si es necesario
    } else {
        // Si no ha visitado el dashboard, marca que lo ha hecho
        localStorage.setItem("visitedDashboard", "true");
    }
};

// Si el usuario se va del dashboard (por ejemplo, cierra la ventana o cambia de página),
// se puede agregar lógica para borrar el registro (si lo deseas).
window.onbeforeunload = function() {
    // Borrar la marca de "visitedDashboard" si deseas resetearlo cuando salga
    // localStorage.removeItem("visitedDashboard");
};