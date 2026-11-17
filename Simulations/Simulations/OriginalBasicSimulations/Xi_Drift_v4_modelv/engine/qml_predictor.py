import pennylane as qml
import torch

class QMLFieldPredictor(torch.nn.Module):
    def __init__(self, n_qubits=4):
        super().__init__()
        self.qlayer = qml.qnn.TorchLayer(
            self._quantum_circuit, 
            weight_shapes={"weights": (n_qubits,)}
        )
        self.clayer = torch.nn.Conv2d(1, 1, 3)
        
    def _quantum_circuit(self, inputs, weights):
        qml.AngleEmbedding(inputs, wires=range(n_qubits))
        qml.BasicEntanglerLayers(weights, wires=range(n_qubits))
        return qml.expval(qml.PauliZ(0))
    
    def forward(self, x):
        x = self.clayer(x)
        x = torch.flatten(x)
        return self.qlayer(x)
