import streamlit as st
import requests

class GraphVisualizer:
    def __init__(self):
        self.api_base_url = "http://localhost:5000/"

    def get_request(self, endpoint, params=None):
        """Realiza solicitudes GET a la API"""
        try:
            response = requests.get(f"{self.api_base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error al conectar con la API: {e}")
            return None

    def shortest_path(self):
        st.header("Camino más corto")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Calcular"):
            if origen and destino:
                result = self.get_request("shortest-path", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def isolated_nodes(self):
        st.header("Nodos aislados")

        if st.button("Mostrar nodos aislados"):
            result = self.get_request("isolated-nodes")
            if result:
                st.json(result)

    def longest_path(self):
        st.header("Camino más largo")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Calcular"):
            if origen and destino:
                result = self.get_request("longest-path", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def nodes_with_highest_degree(self):
        st.header("Nodos con mayor grado")

        if st.button("Mostrar nodos con mayor grado"):
            result = self.get_request("nodes-with-highest-degree")
            if result:
                st.json(result)

    def all_paths(self):
        st.header("Todos los caminos entre dos nodos")
        origen = st.text_input("Nodo origen")
        destino = st.text_input("Nodo destino")

        if st.button("Mostrar todos los caminos"):
            if origen and destino:
                result = self.get_request("all-paths", params={"origen": origen, "destino": destino})
                if result:
                    st.json(result)
            else:
                st.error("Por favor, ingresa tanto el nodo origen como el destino.")

    def detect_clusters(self):
        st.header("Detectar clusters densos")

        if st.button("Detectar clusters"):
            result = self.get_request("detect-clusters")
            if result:
                st.json(result)

    def nodes_by_degree(self):
        st.header("Nodos por grado")
        degree = st.number_input("Grado", min_value=0, step=1)

        if st.button("Mostrar nodos por grado"):
            result = self.get_request("nodes-by-degree", params={"degree": degree})
            if result:
                st.json(result)

    def run(self):
        """Controla la interfaz de Streamlit"""
        st.title("Visualización de Grafos")

        st.sidebar.title("Introduce la url de la API")
        self.api_base_url = st.sidebar.text_input("URL de la API", value=self.api_base_url)

        st.sidebar.title("Opciones")

        option = st.sidebar.selectbox(
            "Selecciona una operación:",
            [
                "Camino más corto",
                "Nodos aislados",
                "Camino más largo",
                "Nodos con mayor grado",
                "Todos los caminos",
                "Detectar clusters",
                "Nodos por grado",
            ]
        )

        if option == "Camino más corto":
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

