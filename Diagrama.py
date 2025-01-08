from graphviz import Digraph

# Reintentar el proceso de generación del diagrama de flujo para el residente con login y dashboard

flowchart = Digraph('Proceso de Gestión de Propiedades (Con Login y Dashboard)', format='png')

flowchart.attr(rankdir='TB', size='8,10')



# Nodos del diagrama de flujo

flowchart.node('Inicio', 'Inicio', shape='oval')

flowchart.node('Registro', 'Registro de Usuario (Residente)', shape='rectangle')

flowchart.node('Login', 'Login', shape='rectangle')

flowchart.node('Dashboard', 'Dashboard del Residente', shape='rectangle')

flowchart.node('VerFacturas', 'Ver Facturas', shape='rectangle')

flowchart.node('RealizarPago', 'Realizar Pago', shape='rectangle')

flowchart.node('Notificar', 'Recibir Notificaciones', shape='rectangle')

flowchart.node('MovimientoPago', 'Registrar Movimiento de Pago', shape='rectangle')

flowchart.node('HistorialCambio', 'Registrar en Historial de Cambios', shape='rectangle')

flowchart.node('Fin', 'Fin', shape='oval')



# Conexiones del diagrama

flowchart.edge('Inicio', 'Registro')

flowchart.edge('Registro', 'Login')

flowchart.edge('Login', 'Dashboard')

flowchart.edge('Dashboard', 'VerFacturas')

flowchart.edge('Dashboard', 'RealizarPago')

flowchart.edge('Dashboard', 'Notificar')

flowchart.edge('RealizarPago', 'MovimientoPago')

flowchart.edge('MovimientoPago', 'HistorialCambio')

flowchart.edge('HistorialCambio', 'Fin')



# Renderizar el diagrama de flujo

flowchart_filepath_login = 'diagrama_flujo_residente_login_dashboard'

flowchart.render(flowchart_filepath_login, cleanup=True)



flowchart_filepath_login + '.png'