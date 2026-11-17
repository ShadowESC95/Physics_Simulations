import torch_geometric as tg
from torch_geometric.nn import GCNConv

class FieldGNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(1, 32)
        self.conv2 = GCNConv(32, 1)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)

# Convert Ξ field to graph
xi = np.load("output/xi_field_log.npy")[0]
grid = tg.utils.grid(xi.shape)  # Create grid graph
data = tg.data.Data(x=xi.flatten(), edge_index=grid.edge_index)
