import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtWidgets, QtCore

class FieldViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.xi_log = np.load("output/xi_field_log.npy")
        self.chi_log = np.load("output/chi_field_log.npy")
        self.drift_tensor = np.load("output/drift_tensor_Xi.npy")

        self.current_frame = 0
        self.max_frame = len(self.xi_log)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ξχ Scalar Field Simulation Viewer")
        self.resize(1200, 800)

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(layout)

        # 3D OpenGL widget
        self.plot = gl.GLViewWidget()
        self.plot.opts['distance'] = 80
        self.plot.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.plot)

        # Frame slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.max_frame - 1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider)

        # Timer for auto-play
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.advance_frame)

        # Playback controls
        controls = QtWidgets.QHBoxLayout()
        self.play_button = QtWidgets.QPushButton("▶ Play")
        self.play_button.clicked.connect(self.toggle_play)
        controls.addWidget(self.play_button)

        self.pause_button = QtWidgets.QPushButton("⏸ Pause")
        self.pause_button.clicked.connect(self.pause)
        controls.addWidget(self.pause_button)

        self.speed_label = QtWidgets.QLabel("Speed (ms):")
        controls.addWidget(self.speed_label)

        self.speed_box = QtWidgets.QSpinBox()
        self.speed_box.setMinimum(10)
        self.speed_box.setMaximum(2000)
        self.speed_box.setValue(200)
        self.speed_box.valueChanged.connect(self.set_speed)
        controls.addWidget(self.speed_box)

        layout.addLayout(controls)

        # Initial display
        self.show_frame()

    def on_slider_changed(self, value):
        self.current_frame = value
        self.show_frame()

    def toggle_play(self):
        self.timer.start(self.speed_box.value())

    def pause(self):
        self.timer.stop()

    def set_speed(self, value):
        if self.timer.isActive():
            self.timer.start(value)

    def advance_frame(self):
        self.current_frame = (self.current_frame + 1) % self.max_frame
        self.slider.setValue(self.current_frame)
        self.show_frame()

    def show_frame(self):
        xi = self.xi_log[self.current_frame]
        chi = self.chi_log[self.current_frame]
        dt = self.drift_tensor

        self.plot.clear()

        # Ξ field
        xi_surface = gl.GLSurfacePlotItem(
            z=xi,
            shader='heightColor',
            color=(1, 0, 0, 0.9),  # Red
            smooth=False,
            computeNormals=False
        )
        self.plot.addItem(xi_surface)

        # χ overlay
        chi_surface = gl.GLSurfacePlotItem(
            z=chi,
            shader='heightColor',
            color=(0, 0, 1, 0.5),  # Blue
            smooth=False,
            computeNormals=False
        )
        self.plot.addItem(chi_surface)

        # DRIFT vector overlay
        try:
            skip = 10
            x, y = np.meshgrid(
                np.linspace(0, xi.shape[0]-1, skip),
                np.linspace(0, xi.shape[1]-1, skip),
            )

            if dt.ndim == 4:  # [x, y, 2, 2]
                u = dt[::skip, ::skip, 0, 0]
                v = dt[::skip, ::skip, 1, 1]
            elif dt.ndim == 3:  # [x, y, 2]
                u = dt[::skip, ::skip, 0]
                v = dt[::skip, ::skip, 1]
            else:
                raise ValueError("Unsupported drift tensor shape.")

            z = np.zeros_like(u)
            vectors = np.stack([u, v, z], axis=-1)
            positions = np.stack([x, y, z], axis=-1)

            for i in range(vectors.shape[0]):
                for j in range(vectors.shape[1]):
                    start = positions[i, j]
                    end = start + vectors[i, j] * 2
                    pts = np.array([start, end])
                    plt = gl.GLLinePlotItem(pos=pts, color=(1, 1, 1, 1), width=1, mode='lines')
                    self.plot.addItem(plt)
        except Exception as e:
            print(f"[Ξχ Viewer] Drift overlay error: {e}")

        self.setWindowTitle(f"Ξχ Viewer - Frame {self.current_frame + 1} / {self.max_frame}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    viewer = FieldViewer()
    viewer.show()
    sys.exit(app.exec_())
