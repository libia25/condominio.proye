function actualizarDocumento() {
    const nacionalidad = document.getElementById('id_nacionalidad').value;
    const documentoInput = document.getElementById('id_documento_identidad');
    if (nacionalidad === 'V') {
        documentoInput.value = 'V-'; // Prefijo para venezolano
    } else if (nacionalidad === 'E') {
        documentoInput.value = 'E-'; // Prefijo para extranjero
    } else {
        documentoInput.value = ''; // Limpiar si no hay selección
    }
}