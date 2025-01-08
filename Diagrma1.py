from graphviz import Digraph

# Crear el diagrama de flujo para el login de usuario con redirección al registro si el usuario no existe
flowchart = Digraph('Proceso de Login de Usuario con Registro', format='png')

# Atributos del diagrama
flowchart.attr(rankdir='TB', size='8,10')

# Nodos del diagrama
flowchart.node('Inicio', 'Inicio', shape='oval')
flowchart.node('FormularioLogin', 'Ingreso de Usuario y Contraseña', shape='rectangle')
flowchart.node('UsuarioExiste', '¿Usuario Existe?', shape='diamond')
flowchart.node('ContraseñaCorrecta', '¿Contraseña Correcta?', shape='diamond')
flowchart.node('AccederDashboard', 'Acceder al Dashboard', shape='rectangle')
flowchart.node('ErrorUsuario', 'Error: Usuario No Existe, Registrarse', shape='rectangle')
flowchart.node('ErrorContraseña', 'Error: Contraseña Incorrecta', shape='rectangle')
flowchart.node('RegistroUsuario', 'Registro de Usuario', shape='rectangle')
flowchart.node('Fin', 'Fin', shape='oval')

# Conexiones del diagrama
flowchart.edge('Inicio', 'FormularioLogin')
flowchart.edge('FormularioLogin', 'UsuarioExiste')
flowchart.edge('UsuarioExiste', 'ErrorUsuario', label='No')
flowchart.edge('ErrorUsuario', 'RegistroUsuario', label='Registrarse')
flowchart.edge('RegistroUsuario', 'FormularioLogin', label='Regresar al Login')
flowchart.edge('UsuarioExiste', 'ContraseñaCorrecta', label='Sí')
flowchart.edge('ContraseñaCorrecta', 'ErrorContraseña', label='No')
flowchart.edge('ErrorContraseña', 'FormularioLogin', label='Reintentar')
flowchart.edge('ContraseñaCorrecta', 'AccederDashboard', label='Sí')
flowchart.edge('AccederDashboard', 'Fin')

# Renderizar y guardar el diagrama
flowchart_filepath_login = 'diagrama_flujo_login_usuario_con_registro'
flowchart.render(flowchart_filepath_login, cleanup=True)

flowchart_filepath_login + '.png'