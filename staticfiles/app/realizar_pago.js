document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('pago-form');
    const mensajeDiv = document.getElementById('mensaje');

    form.addEventListener('submit', function (event) {
      event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario

      // Obtener los valores ingresados por el usuario
      const departamentoNumero = document.getElementById('departamento-numero').value;
      const usuarioNombre = document.getElementById('usuario-nombre').value;
      const montoTotal = parseFloat(document.getElementById('monto-total').value);
      const estadoPago = document.getElementById('estado-pago').value;
      const fechaEmision = document.getElementById('fecha-emision').value;
      const fechaVencimiento = document.getElementById('fecha-vencimiento').value;
      const montoPagado = parseFloat(document.getElementById('monto').value);

      // Validar que el monto a pagar no sea mayor al monto total de la factura
      if (montoPagado <= 0) {
        mensajeDiv.innerHTML = '<div class="alert alert-danger">El monto debe ser mayor a 0.</div>';
        return;
      }

      if (montoPagado > montoTotal) {
        mensajeDiv.innerHTML = '<div class="alert alert-danger">El monto no puede ser mayor al monto total de la factura.</div>';
        return;
      }

      // Simular el pago exitoso
      mensajeDiv.innerHTML = '<div class="alert alert-success">Pago realizado exitosamente.</div>';

      // Aquí puedes enviar los datos al servidor para procesar el pago, si fuera necesario
      // Por ejemplo, utilizando fetch o AJAX:
      // fetch('/ruta-del-servidor', {
      //   method: 'POST',
      //   body: JSON.stringify({ departamentoNumero, usuarioNombre, montoTotal, estadoPago, fechaEmision, fechaVencimiento, montoPagado })
      // }).then(response => {
      //   if (response.ok) {
      //     mensajeDiv.innerHTML = '<div class="alert alert-success">Pago procesado correctamente.</div>';
      //   } else {
      //     mensajeDiv.innerHTML = '<div class="alert alert-danger">Error al procesar el pago.</div>';
      //   }
      // }).catch(error => {
      //   mensajeDiv.innerHTML = '<div class="alert alert-danger">Hubo un error en el proceso.</div>';
      // });
    });
});