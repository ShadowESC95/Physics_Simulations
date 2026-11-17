import os
import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg


class FieldViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ξχ QT 3D Viewer")

        # Load data
        self.xi_log = np.load("output/xi_field_log.npy")
        self.chi_log = np.load("output/chi_field_log.npy")
        self.entropy_log = np.load("output/xi_entropy_log.npy")
        self.drift_tensor = np.load("output/drift_tensor_Xi.npy")

        self.frame = 0
        self.total_frames = self.xi_log.shape[0]

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # 3D plot widget
        self.gl_widget = gl.GLViewWidget()
        self.gl_widget.opts['distance'] = 100
        self.layout.addWidget(self.gl_widget)

        # Sliders
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(pg.QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.total_frames - 1)
        self.slider.valueChanged.connect(self.update_frame)
        self.layout.addWidget(self.slider)

        # Toggle checkboxes
        self.xi_cb = QtWidgets.QCheckBox("Ξ field")
        self.xi_cb.setChecked(True)
        self.chi_cb = QtWidgets.QCheckBox("χ field")
        self.chi_cb.setChecked(True)
        self.drift_cb = QtWidgets.QCheckBox("DRIFT field")
        self.drift_cb.setChecked(True)

        cb_layout = QtWidgets.QHBoxLayout()
        cb_layout.addWidget(self.xi_cb)
        cb_layout.addWidget(self.chi_cb)
        cb_layout.addWidget(self.drift_cb)
        self.layout.addLayout(cb_layout)

        self.init_ui()

    def init_ui(self):
        self.griditem = gl.GLGridItem()
        self.gl_widget.addItem(self.griditem)
        self.update_frame(self.frame)

    def update_frame(self, frame):
        self.frame = frame
        self.gl_widget.clear()
        self.gl_widget.addItem(self.griditem)

        shape = self.xi_log.shape[1]
        grid = np.linspace(-1, 1, shape)
        x = grid
        y = grid
        xi_surface = self.xi_log[frame]

        if self.xi_cb.isChecked():
            surface = gl.GLSurfacePlotItem()
            surface.setData(x=x, y=y, z=xi_surface)
            surface.shader = 'heightColor'
            self.gl_widget.addItem(surface)

        if self.chi_cb.isChecked():
            chi_surface = self.chi_log[frame] * 0.3
            overlay = gl.GLSurfacePlotItem()
            overlay.setData(x=x, y=y, z=chi_surface)
            overlay.color = (1, 0.5, 0.2, 0.4)
            self.gl_widget.addItem(overlay)

        if self.drift_cb.isChecked():
            try:
                dt = self.drift_tensor[frame]
                if dt.ndim == 3 and dt.shape[-1] == 2:
                    skip = shape // 10
                    u = dt[::skip, ::skip, 0]
                    v = dt[::skip, ::skip, 1]
                    pos_x, pos_y = np.meshgrid(np.linspace(-1, 1, u.shape[0]), np.linspace(-1, 1, u.shape[1]))
                    pos = np.stack((pos_x, pos_y), axis=-1).reshape(-1, 2)
                    pos_3d = np.hstack((pos, np.zeros((pos.shape[0], 1))))
                    dirs = np.stack((u, v, np.zeros_like(u)), axis=-1).reshape(-1, 3)
                    arrows = gl.GLLinePlotItem(pos=pos_3d + dirs * 0.05, color=(0.7, 0.7, 0.7, 1), mode='lines')
                    self.gl_widget.addItem(arrows)
            except Exception as e:
                print(f"[Ξχ Viewer] Drift overlay error: {e}")

        self.setWindowTitle(f"[Ξχ Viewer] Frame {frame} | Entropy: {self.entropy_log[frame]:.5f}")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    viewer = FieldViewer()
    viewer.show()
    app.exec_()
