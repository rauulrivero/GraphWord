from controller import Controller

DATALAKE_PATH = 'datalake'
OUTPUT_JSON_PATH = 'graph.json'

def main():

    controller = Controller(DATALAKE_PATH, OUTPUT_JSON_PATH)

    controller.run()

if __name__ == "__main__":
    main()
