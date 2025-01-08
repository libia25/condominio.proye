 // Función para descargar como XML
 document.getElementById('downloadXML').addEventListener('click', function() {
    const xmlData = `<?xml version="1.0" encoding="UTF-8"?>
<historial_pagos>
{% for pago in pagos %}
<pago>
    <fecha>{{ pago.fecha_emision }}</fecha>
    <monto_pagado>{{ pago.monto_pagado }}</monto_pagado>
    <estado>{{ pago.estado }}</estado>
    <metodo_pago>{{ pago.metodo_pago }}</metodo_pago>
</pago>
{% endfor %}
</historial_pagos>`;

    // Crear un archivo Blob con el contenido XML
    const blob = new Blob([xmlData], { type: 'application/xml' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'historial_pagos.xml';
    link.click();
});

// Función para descargar como PDF
document.getElementById('downloadPDF').addEventListener('click', function() {
    const { jsPDF } = window.jspdf;

    // Verificar si jsPDF está cargado correctamente
    if (typeof jsPDF === 'undefined') {
        alert('jsPDF no está cargado correctamente');
        return;
    }

    const doc = new jsPDF();
    doc.setFontSize(20);
    doc.text('Historial de Pagos', 20, 20);

    // Obtener los datos de la tabla
    const table = document.getElementById('pagosTable');
    const rows = table.getElementsByTagName('tr');
    const data = [];

    // Recopilar los datos de la tabla
    for (let i = 1; i < rows.length; i++) { // Empezamos desde 1 para omitir la cabecera
        const cols = rows[i].getElementsByTagName('td');
        data.push([
            cols[0].innerText, // Fecha
            cols[1].innerText, // Monto Pagado
            cols[2].innerText, // Estado
            cols[3].innerText  // Método de Pago
        ]);
    }

    // Agregar la tabla al PDF usando autoTable
    doc.autoTable({
        head: [['Fecha', 'Monto Pagado', 'Estado', 'Método de Pago']],
        body: data
    });

    // Descargar el PDF
    doc.save('historial_pagos.pdf');
});