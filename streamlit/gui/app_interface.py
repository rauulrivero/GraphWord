import streamlit as st

class GraphVisualizer:
    def __init__(self, api_handler):
        self.api_handler = api_handler

    def run(self):
        """Controls the Streamlit interface"""
        st.title("Graph Visualization")

        if "api_base_url" not in st.session_state:
            st.session_state.api_base_url = self.api_handler.api_base_url

        self.api_handler.update_base_url(st.session_state.api_base_url)

        st.sidebar.title("Enter API URL")
        api_base_url = st.sidebar.text_input("API URL", value=st.session_state.api_base_url)

        if st.sidebar.button("Update URL"):
            st.session_state.api_base_url = api_base_url
            self.api_handler.update_base_url(api_base_url)
            st.sidebar.success(f"API URL updated to: {api_base_url}")

        st.sidebar.title("Options")

        option = st.sidebar.selectbox(
            "Select an operation:",
            [
                "Initialize Graph",
                "Shortest Path",
                "Isolated Nodes",
                "Longest Path",
                "Nodes with Highest Degree",
                "All Paths",
                "Detect Clusters",
                "Nodes by Degree",
            ]
        )

        if option == "Initialize Graph":
            self.create_graph()
        elif option == "Shortest Path":
            self.shortest_path()
        elif option == "Isolated Nodes":
            self.isolated_nodes()
        elif option == "Longest Path":
            self.longest_path()
        elif option == "Nodes with Highest Degree":
            self.nodes_with_highest_degree()
        elif option == "All Paths":
            self.all_paths()
        elif option == "Detect Clusters":
            self.detect_clusters()
        elif option == "Nodes by Degree":
            self.nodes_by_degree()

    def create_graph(self):
        st.header("Initialize Graph")

        book_ids = st.text_area(
            "Enter the list of book IDs (comma-separated) to create the word graph.",
            placeholder="1,2,3,4"
        )

        if st.button("Initialize Graph"):
            if book_ids:
                try:
                    book_ids_list = [int(book_id.strip()) for book_id in book_ids.split(",")]
                    result = self.api_handler.post_request("create-graph", json={"book_ids": book_ids_list})
                    if result:
                        st.success("Graph initialized successfully.")
                        st.json(result)
                    else:
                        st.error("No valid response received from the backend.")
                except ValueError:
                    st.error("Please enter a valid list of book IDs separated by commas.")
            else:
                st.error("Please enter at least one book ID.")

    def shortest_path(self):
        st.header("Shortest Path")
        source = st.text_input("Source Node")
        target = st.text_input("Target Node")

        if st.button("Calculate"):
            if source and target:
                result = self.api_handler.get_request("shortest-path", params={"source": source, "target": target})
                if result:
                    st.json(result)
            else:
                st.error("Please enter both the source and target nodes.")

    def isolated_nodes(self):
        st.header("Isolated Nodes")

        if st.button("Show Isolated Nodes"):
            result = self.api_handler.get_request("isolated-nodes")
            if result:
                st.json(result)

    def longest_path(self):
        st.header("Longest Path")
        source = st.text_input("Source Node")
        target = st.text_input("Target Node")

        if st.button("Calculate"):
            if source and target:
                result = self.api_handler.get_request("longest-path", params={"source": source, "target": target})
                if result:
                    st.json(result)
            else:
                st.error("Please enter both the source and target nodes.")

    def nodes_with_highest_degree(self):
        st.header("Nodes with Highest Degree")

        if st.button("Show Nodes with Highest Degree"):
            result = self.api_handler.get_request("nodes-with-highest-degree")
            if result:
                st.json(result)

    def all_paths(self):
        st.header("All Paths Between Two Nodes")
        source = st.text_input("Source Node")
        target = st.text_input("Target Node")

        if st.button("Show All Paths"):
            if source and target:
                result = self.api_handler.get_request("all-paths", params={"source": source, "target": target})
                if result:
                    st.json(result)
            else:
                st.error("Please enter both the source and target nodes.")

    def detect_clusters(self):
        st.header("Detect Dense Clusters")

        if st.button("Detect Clusters"):
            result = self.api_handler.get_request("detect-clusters")
            if result:
                st.json(result)

    def nodes_by_degree(self):
        st.header("Nodes by Degree")
        degree = st.number_input("Degree", min_value=0, step=1)

        if st.button("Show Nodes by Degree"):
            result = self.api_handler.get_request("nodes-by-degree", params={"degree": degree})
            if result:
                st.json(result)
