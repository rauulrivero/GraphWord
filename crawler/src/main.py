from datalakeuploader.book_saver import save_book_content

# Variable global para el número de libros a procesar
N_LIBROS = 50

def main():
    # Extrae el contenido de los libros y los guarda en el datalake
    for i in range(25001, 25001 + N_LIBROS):
        save_book_content(i)

if __name__ == "__main__":
    main()
