import streamlit as st

class GraphVisualizer:
    def __init__(self, api_handler):
        self.api_handler = api_handler


    def run(self):
        """Controla la interfaz de Streamlit"""
        st.title("Visualización de Grafos")

        st.sidebar.title("Introduce la URL de la API")
        api_base_url = st.sidebar.text_input("URL de la API", value=self.api_handler.api_base_url)

        if st.sidebar.button("Actualizar URL"):
            self.api_handler.update_base_url(api_base_url)
            st.sidebar.success(f"URL de la API actualizada a: {api_base_url}")

        st.sidebar.title("Opciones")

        option = st.sidebar.selectbox(
            "Selecciona una operación:",
            [
                "Inicializar Grafo",
                "Camino más corto",
                "Nodos aislados",
                "Camino más largo",
                "Nodos con mayor grado",
                "Todos los caminos",
                "Detectar clusters",
                "Nodos por grado",
            ]
        )

        if option == "Inicializar Grafo":
            self.initialize_graph()
        elif option == "Camino más corto":
            self.shortest_path()
        elif option == "Nodos aislados":
            self.isolated_nodes()
        elif option == "Camino más largo":
            self.longest_path()
        elif option == "Nodos con mayor grado":
            self.nodes_with_highest_degree()
        elif option == "Todos los caminos":
            self.all_paths()
        elif option == "Detectar clusters":
            self.detect_clusters()
        elif option == "Nodos por grado":
            self.nodes_by_degree()



    def initialize_graph(self):
        st.header("Inicializar Grafo")

        book_ids = st.text_area("Introduce la lista de IDs de libros (separados por comas), con los que quieres crear el grafo de palabras.", placeholder="1,2,3,4")

        if st.button("Inicializar Grafo"):
            if book_ids:
                book_ids_list = [book_id.strip() for book_id in book_ids.split(",")]
                result = self.api_handler.post_request("initialize-graph", json={"book_ids": book_ids_list})
                if result:
                    st.success("Grafo inicializado correctamente.")
                    st.json(result)
            else:
                st.error("Por favor, ingresa al menos un ID de libro.")
    def shortest_path(self):
        st.header("Camino más corto")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Calcular"):
            if origen and destino:
                result = self.api_handler.get_request("shortest-path", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def isolated_nodes(self):
        st.header("Nodos aislados")

        if st.button("Mostrar nodos aislados"):
            result = self.api_handler.get_request("isolated-nodes")
            if result:
                st.json(result)

    def longest_path(self):
        st.header("Camino más largo")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Calcular"):
            if origen and destino:
                result = self.api_handler.get_request("longest-path", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def nodes_with_highest_degree(self):
        st.header("Nodos con mayor grado")

        if st.button("Mostrar nodos con mayor grado"):
            result = self.api_handler.get_request("nodes-with-highest-degree")
            if result:
                st.json(result)

    def all_paths(self):
        st.header("Todos los caminos entre dos nodos")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Mostrar todos los caminos"):
            if origen and destino:
                result = self.api_handler.get_request("all-paths", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def detect_clusters(self):
        st.header("Detectar clusters densos")

        if st.button("Detectar clusters"):
            result = self.api_handler.get_request("detect-clusters")
            if result:
                st.json(result)

    def nodes_by_degree(self):
        st.header("Nodos por grado")
        degree = st.number_input("Grado", min_value=0, step=1)

        if st.button("Mostrar nodos por grado"):
            result = self.api_handler.get_request("nodes-by-degree", params={"degree": degree})
            if result:
                st.json(result)

    