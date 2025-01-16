import os

# Obtener la ruta del directorio actual
current_directory = os.getcwd()

# Listar los archivos y carpetas en el directorio actual
files_and_dirs = os.listdir(current_directory)

# Imprimir los resultados para verificar
print("Archivos y directorios disponibles:", files_and_dirs)# Test simple sin importar librerías adicionales

def test_suma():
    """Prueba básica que verifica si la suma funciona correctamente."""
    resultado = 2 + 2
    assert resultado == 4, f"Error: se esperaba 4, pero se obtuvo {resultado}"

def test_string_concatenation():
    """Prueba básica que verifica la concatenación de cadenas."""
    resultado = "Hola" + " " + "Mundo"
    assert resultado == "Hola Mundo", f"Error: se esperaba 'Hola Mundo', pero se obtuvo {resultado}"

def test_list_length():
    """Prueba básica que verifica la longitud de una lista."""
    mi_lista = [1, 2, 3, 4, 5]
    assert len(mi_lista) == 5, f"Error: se esperaba longitud 5, pero se obtuvo {len(mi_lista)}"
