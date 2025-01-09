import argparse
from gui.app_interface import GraphVisualizer

def main():
    # Configure the argument parser
    parser = argparse.ArgumentParser(description="Start the graph visualizer with a custom API base URL.")
    parser.add_argument(
        "--api_base_url",
        type=str,
        default="http://localhost:5000/",
        help="The base URL of the API. Default is 'http://localhost:5000/'."
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Use the provided API base URL
    visualizer = GraphVisualizer(api_base_url=args.api_base_url)
    visualizer.run()

if __name__ == "__main__":
    main()
