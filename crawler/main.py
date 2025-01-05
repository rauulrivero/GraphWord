from src.controller import Controller

# Variable global para el número de libros a procesar
N_LIBROS = 10
DATALAKE_PATH = 'datalake'

def main():
    controller = Controller(DATALAKE_PATH)

    controller.run(2500, N_LIBROS)
        

if __name__ == "__main__":
    main()
