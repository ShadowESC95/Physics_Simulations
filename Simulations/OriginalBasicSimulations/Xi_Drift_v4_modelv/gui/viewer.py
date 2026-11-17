from PyQt5 import QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

class SurfaceViewer(QtWidgets.QMainWindow):
    def __init__(self, data: np.ndarray):
        super().__init__()
        self.setWindowTitle("3D Surface Viewer")
        self.resize(800, 600)

        self.widget = gl.GLViewWidget()
        self.setCentralWidget(self.widget)
        self.plot_surface(data)

    def plot_surface(self, data: np.ndarray):
        x, y = np.meshgrid(np.linspace(-10, 10, data.shape[0]), np.linspace(-10, 10, data.shape[1]))
        z = data

        verts = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
        faces = []
        for i in range(data.shape[0] - 1):
            for j in range(data.shape[1] - 1):
                idx = i * data.shape[1] + j
                faces.append([idx, idx + 1, idx + data.shape[1]])
                faces.append([idx + 1, idx + data.shape[1] + 1, idx + data.shape[1]])

        mesh = gl.GLMeshItem(vertexes=verts, faces=np.array(faces), smooth=False, drawEdges=True)
        self.widget.addItem(mesh)

def show_viewer(data):
    app = QtWidgets.QApplication([])
    viewer = SurfaceViewer(data)
    viewer.show()
    app.exec_()
