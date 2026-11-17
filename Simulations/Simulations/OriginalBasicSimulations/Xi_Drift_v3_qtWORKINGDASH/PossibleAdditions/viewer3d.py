
import sys
import os
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph.opengl as gl
import pyqtgraph as pg


class FieldViewer(QtWidgets.QWidget):
    def __init__(self, data_paths=None):
        super().__init__()
        self.setWindowTitle("Ξχ 3D Field Viewer")
        self.resize(1000, 800)

        # Load data
        self.data_paths = data_paths or {
            'xi': 'output/xi_field_log.npy',
            'chi': 'output/chi_field_log.npy',
            'drift': 'output/drift_tensor_Xi.npy'
        }
        self.data = {k: np.load(v) for k, v in self.data_paths.items() if os.path.exists(v)}
        self.current_frame = 0
        self.total_frames = next(iter(self.data.values())).shape[0] if self.data else 0

        # UI Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.gl_widget = gl.GLViewWidget()
        self.gl_widget.opts['distance'] = 80
        self.layout.addWidget(self.gl_widget)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.total_frames - 1)
        self.slider.valueChanged.connect(self.update_frame)
        self.layout.addWidget(self.slider)

        # Checkboxes
        self.checkboxes = {}
        cb_layout = QtWidgets.QHBoxLayout()
        for name in self.data:
            cb = QtWidgets.QCheckBox(name)
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_frame)
            cb_layout.addWidget(cb)
            self.checkboxes[name] = cb
        self.layout.addLayout(cb_layout)

        self.grid = gl.GLGridItem()
        self.gl_widget.addItem(self.grid)
        self.update_frame(self.current_frame)

    def update_frame(self, frame):
        if isinstance(frame, int):
            self.current_frame = frame
        else:
            self.current_frame = frame

        self.gl_widget.clear()
        self.gl_widget.addItem(self.grid)

        for name, data in self.data.items():
            if self.checkboxes[name].isChecked():
                slice_data = data[self.current_frame]
                p_item = gl.GLSurfacePlotItem(
                    z=slice_data,
                    shader='shaded',
                    computeNormals=False
                )
                self.gl_widget.addItem(p_item)


def main():
    app = QtWidgets.QApplication(sys.argv)
    viewer = FieldViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
