# consultorio
Sistema de gestion de consultorio


El programa es una herramienta de gestión de historias clínicas diseñada y orientada a facilitar la tarea en los consultorios médicos a la hora de realizar pericias. Su principal objetivo es organizar la información de diversos pacientes, incluyendo datos personales, antecedentes médicos, detalles de accidentes y tratamiento, así como la gestión de archivos asociados. Todo esto se maneja mediante una interfaz gráfica desarrollada con Tkinter.
Este comienza su ejecución configurando la base de datos mediante la función setup_database. Esta función asegura la existencia de la base de datos consultorio.db en el directorio del programa y crea la tabla consultorio si no existe. Esta tabla incluye múltiples campos para almacenar información médica, personal y legal de los pacientes. La configuración de la base de datos se realiza al inicio del programa, dentro del bloque principal if __name__ == "__main__", garantizando que el entorno esté listo antes de cargar la interfaz gráfica.
La interfaz principal del programa se construye en la función create_gui, que define la ventana principal (root) y su estructura. En la parte superior de la ventana, se encuentra una barra de navegación (nav_frame) con botones que permiten agregar, editar, eliminar, buscar, actualizar registros y visualizar datos más detallados de historias clínicas. En el centro de la ventana, un Treeview llamado turnos_tree muestra una tabla con datos clave como DNI, nombre, teléfono, obra social y número de expediente. Este se actualiza dinámicamente mediante la función load_data, que se llama al iniciar el programa y tras cualquier operación que modifique los datos, asegurando que la información visualizada esté siempre sincronizada con la base de datos.
La funcion add_turno permite añadir nuevos registros abriendo una ventana emergente con campos para DNI, nombre, teléfono y obra social. Los datos ingresados se validan y se almacenan en la base de datos mediante una consulta SQL INSERT. De la misma forma edit_turno permite editar un registro seleccionado, precargando los valores actuales en un formulario que el usuario puede modificar. Una vez confirmados los cambios, estos se actualizan en la base mediante una consulta SQL UPDATE. Por otro lado, delete_turno se encarga de eliminar registros seleccionados del Treeview después de solicitar confirmación al usuario, ejecutando una consulta DELETE en la base de datos.
Se puede encontrar una funcionalidad para gestionar historias clínicas en la función manage_historia_clinica. Esta abre una ventana que permite visualizar y editar información específica de un paciente, como antecedentes médicos, datos laborales o detalles de accidentes. La información se organiza en un formulario donde cada campo corresponde a una columna de la tabla consultorio. Los datos se cargan dinámicamente desde la base de datos según el registro seleccionado en el Treeview. Esta ventana también incluye botones para habilitar la edición de los campos y guardar cambios, utilizando una lógica que determina si los datos deben ser insertados o actualizados.
Dentro del mismo formulario de historias clínicas se pueden gestionar archivos relacionados con cada paciente mediante las funciones cargar_archivos y abrir_archivo. La primera permite al usuario asociar documentos como informes médicos, imágenes o documentos legales a un paciente específico, organizándolos en subcarpetas dentro de un sistema de archivos, mientras que la segunda permite abrir estos documentos directamente desde la aplicación.
También se pueden realizar búsquedas avanzadas a través de la función buscar_historia. Esta permite filtrar registros según criterios como nombre, DNI o expediente. Al realizar una búsqueda, los resultados se muestran directamente en el Treeview, lo que facilita al usuario encontrar la información deseada sin tener que recorrer toda la lista de registros.
