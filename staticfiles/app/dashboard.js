document.addEventListener("DOMContentLoaded", function() {
    function hideAllSections() {
        const sections = document.querySelectorAll('.section-content');
        sections.forEach(section => section.style.display = 'none');
    }

    // Mostrar y ocultar secciones
    document.getElementById("pagos-link").addEventListener("click", function() {
        hideAllSections();
        document.getElementById("pagos").style.display = "block";
    });

    document.getElementById("servicios-link").addEventListener("click", function() {
        hideAllSections();
        document.getElementById("servicios").style.display = "block";
    });

    document.getElementById("facturas-link").addEventListener("click", function() {
        hideAllSections();
        document.getElementById("facturas").style.display = "block";
    });

    document.getElementById("mantenimientos-link").addEventListener("click", function() {
        hideAllSections();
        document.getElementById("mantenimientos").style.display = "block";
    });

    // Mostrar formulario de actualización de perfil
    document.getElementById("profile-button").addEventListener("click", function() {
        var form = document.getElementById("update-profile-form");
        form.style.display = form.style.display === "none" ? "block" : "none";
    });

    // Mostrar Movimientos de Pago
    document.getElementById('movimientos_pago-link').addEventListener('click', function () {
        hideAllSections();
        document.getElementById('movimientos_pago').style.display = 'block';
    });
});

