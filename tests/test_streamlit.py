# Simplified Streamlit Test
from gui.app_interface import GraphVisualizer
import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import patch

@patch('gui.app_interface.requests.get')
def test_streamlit_visualizer(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {'path': ['A', 'B']})
    visualizer = GraphVisualizer()
    result = visualizer.get_request('shortest-path', {'origen': 'A', 'destino': 'B'})
    assert result == {'path': ['A', 'B']}
