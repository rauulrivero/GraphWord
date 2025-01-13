from src.controller import Controller

# Nombre del bucket del datalake
BUCKET_DATALAKE_NAME = 'books-datalake'

def lambda_handler(event, context):
    """
    Handler de AWS Lambda para ejecutar la lógica principal.

    Args:
        event (dict): Datos del evento que invoca la función.
        context (object): Información del contexto de la ejecución.

    Returns:
        dict: Respuesta con el estado de la ejecución.
    """
    # Obtener los parámetros del evento, con valores por defecto
    n_libros = event.get('n_libros', 10)  # Número de libros a procesar (predeterminado: 10)
    threshold = event.get('threshold', 2500)  # Umbral o límite a pasar al controlador

    try:
        # Inicializar el controlador con el nombre del bucket
        controller = Controller(BUCKET_DATALAKE_NAME)

        # Ejecutar el controlador con los parámetros especificados
        controller.run(threshold, n_libros)

        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': {
                'message': 'Proceso completado exitosamente',
                'n_libros': n_libros,
                'threshold': threshold
            }
        }
    except Exception as e:
        # Manejo de errores
        return {
            'statusCode': 500,
            'body': {
                'message': 'Error al procesar los libros',
                'error': str(e)
            }
        }
