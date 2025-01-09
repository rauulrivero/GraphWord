from src.controller import Controller

DATALAKE_PATH = 'datalake'
OUTPUT_JSON_PATH = 'graph.json'
DATALAKE_BUCKET = 'datalake-books'
GRAPH_BUCKET = 'wordgraph-tcsd'

def main():

    controller = Controller(DATALAKE_PATH, OUTPUT_JSON_PATH, DATALAKE_BUCKET, GRAPH_BUCKET)

    controller.run()

if __name__ == "__main__":
    main()
