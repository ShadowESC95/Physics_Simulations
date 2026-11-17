# visual/qt_field_viewer3d.py

import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QSlider, QLabel, QTabWidget, QFileDialog
)
from PyQt5.QtCore import Qt
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui
import pyvista as pv

class Field3DViewer(QWidget):
    def __init__(self, title, data_loader_func):
        super().__init__()
        self.setWindowTitle(title)
        self.data_loader_func = data_loader_func

        self.layout = QVBoxLayout()
        self.view = gl.GLViewWidget()
        self.layout.addWidget(self.view)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(99)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_field)
        self.layout.addWidget(self.slider)

        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("Export PNG")
        self.export_btn.clicked.connect(self.export_png)
        self.export_vtk_btn = QPushButton("Export VTK")
        self.export_vtk_btn.clicked.connect(self.export_vtk)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.export_vtk_btn)

        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        self.surface = None
        self.update_field(0)

    def update_field(self, index):
        self.view.clear()
        x, y, z = self.data_loader_func(index)
        self.surface = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='shaded', smooth=True)
        self.view.addItem(self.surface)

    def export_png(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png)")
        if filename:
            exporter = QtGui.QScreen.grabWindow(self.view.winId())
            exporter.save(filename, 'png')

import pyvista as pv  # add to imports

def export_vtk(self):
    filename, _ = QFileDialog.getSaveFileName(self, "Save VTK", "", "VTU Files (*.vtu)")
    if filename:
        x, y, z = self.data_loader_func(self.slider.value())

        # pyvista grid creation
        grid = pv.StructuredGrid()
        grid.points = np.c_[x.ravel(), y.ravel(), z.ravel()]
        grid.dimensions = x.shape[0], x.shape[1], 1
        grid["field_values"] = z.ravel(order="F")

        grid.save(filename)
        print(f"Saved to {filename}")


class MultiViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ξχ Drift Field Viewer")
        self.tabs = QTabWidget()

        self.tabs.addTab(Field3DViewer("Ξ Field", self.load_xi), "Ξ Field")
        self.tabs.addTab(Field3DViewer("χ Field", self.load_chi), "χ Field")
        self.tabs.addTab(Field3DViewer("Drift Tensor", self.load_drift), "Drift Tensor")
        self.tabs.addTab(Field3DViewer("Entropy Arc", self.load_entropy), "Entropy")

        self.setCentralWidget(self.tabs)
        self.resize(900, 700)

    def load_xi(self, idx):
        data = np.load("output/xi_field_log.npy")
        return self.reconstruct_surface(data[idx])

    def load_chi(self, idx):
        try:
            data = np.load("output/chi_field_log.npy")
            return self.reconstruct_surface(data[idx])
        except FileNotFoundError:
            z = np.zeros((100, 100))
            return self.reconstruct_surface(z)

    def load_drift(self, idx):
        data = np.load("output/drift_tensor_Xi.npy")
        return self.reconstruct_surface(data[idx])

    def load_entropy(self, idx):
        try:
            data = np.load("output/xi_entropy_log.npy")
            return self.reconstruct_surface(data[idx])
        except FileNotFoundError:
            z = np.zeros((100, 100))
            return self.reconstruct_surface(z)

    def reconstruct_surface(self, z):
        x = np.linspace(-10, 10, z.shape[0])
        y = np.linspace(-10, 10, z.shape[1])
        x, y = np.meshgrid(x, y)
        return x, y, z

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MultiViewerApp()
    viewer.show()
    sys.exit(app.exec_())
