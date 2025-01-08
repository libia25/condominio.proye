document.addEventListener("DOMContentLoaded", function() {
    // Mostrar y ocultar las secciones
    const verPagosLink = document.getElementById('ver-pagos-link');
    const movimientosPagoLink = document.getElementById('movimientos-pago-link');
    const facturasLink = document.getElementById('facturas-link');
    const mantenimientosLink = document.getElementById('mantenimientos-link');
    const facturaspagrecentLink = document.getElementById('facturaspagrecent-link');

    const pagosListado = document.getElementById('pagos-listado');
    const movimientosPago = document.getElementById('movimientos_pago');
    const facturas = document.getElementById('facturas');
    const mantenimientos = document.getElementById('mantenimientos');
    const facturaspagrecent = document.getElementById('facturas-pagadas-recent')

    // Función para ocultar todas las secciones
    function ocultarSecciones() {
        pagosListado.style.display = 'none';
        movimientosPago.style.display = 'none';
        facturas.style.display = 'none';
        mantenimientos.style.display = 'none';
        facturaspagrecent.style.display = 'none';

    }

    // Mostrar la sección de Pagos
    verPagosLink.addEventListener('click', function() {
        ocultarSecciones();
        pagosListado.style.display = 'block';
    });

    // Mostrar la sección de Movimientos de Pago
    movimientosPagoLink.addEventListener('click', function() {
        ocultarSecciones();
        movimientosPago.style.display = 'block';
    });
    // Mostrar la sección de Facturas
    facturasLink.addEventListener('click', function() {
        ocultarSecciones();
        facturas.style.display = 'block';
    });

    // Mostrar la sección de Mantenimientos
    mantenimientosLink.addEventListener('click', function() {
        ocultarSecciones();
        mantenimientos.style.display = 'block';
    });

    facturaspagrecentLink.addEventListener('click', function() {
        ocultarSecciones();
        mantenimientos.style.display = 'block';
    });
});