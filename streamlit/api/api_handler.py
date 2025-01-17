import requests
import streamlit as st

class APIHandler:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def get_request(self, endpoint, params=None):
        """Performs GET requests to the API"""
        try:
            response = requests.get(f"{self.api_base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
            return None

    def post_request(self, endpoint, json=None):
        """Performs POST requests to the API"""
        try:
            response = requests.post(f"{self.api_base_url}/{endpoint}", json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
            return None
        
    def update_base_url(self, api_base_url):
        self.api_base_url = api_base_url
