from gui.app_interface import GraphVisualizer
from api.api_handler import APIHandler

def main():
    api_handler = APIHandler("http://localhost:5000")
    visualizer = GraphVisualizer(api_handler)
    
    visualizer.run()

if __name__ == "__main__":
    main()
