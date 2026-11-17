import pytest
from src.engine.qml_predictor import QMLFieldPredictor

def test_qml_init():
    model = QMLFieldPredictor()
    assert model.qlayer.num_qubits == 4
