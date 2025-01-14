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
    # Obtener la lista de book_ids desde el evento
    book_ids = event.get('book_ids', [])  # Lista de identificadores de libros

    if not book_ids:
        return {
            'statusCode': 400,
            'body': {
                'message': 'No se proporcionaron book_ids en el evento.'
            }
        }

    try:
        # Inicializar el controlador con el nombre del bucket
        controller = Controller(BUCKET_DATALAKE_NAME)

        # Ejecutar el controlador pasando los book_ids
        controller.run(book_ids)

        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': {
                'message': 'Proceso completado exitosamente',
                'book_ids': book_ids
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
