from src.controller import Controller

# Variable global para el número de libros a procesar
N_LIBROS = 10
BUCKET_DATALAKE_NAME = 'books-datalake'

def main():
    controller = Controller(BUCKET_DATALAKE_NAME)

    controller.run(2500, N_LIBROS)
        

if __name__ == "__main__":
    main()
