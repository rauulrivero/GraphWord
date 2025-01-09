from gui.app_interface import GraphVisualizer

def main():

    visualizer = GraphVisualizer(api_base_url="http://localhost:5000/")
    visualizer.run()



if __name__ == "__main__":
    main()