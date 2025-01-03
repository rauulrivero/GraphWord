# Lee el fichero de texto y devuelve su contenido en lista de palabras
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

