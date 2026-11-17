# Recreate enhanced viewer3d.py after reset

enhanced_viewer3d_code = """
import sys
import os
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from field_loader import load_field
from lammps_export import export_to_lammps
from dealii_export import export_to_hdf5
from openfoam_export import export_openfoam_field

EXPORT_FORMATS = ['.npy', '.hdf5', 'LAMMPS', 'OpenFOAM']

class FieldViewer(QtWidgets.QWidget):
    def __init__(self, data_paths=None):
        super().__init__()
        self.setWindowTitle("Ξχ 3D Field Viewer")
        self.resize(1000, 900)

        self.data_paths = data_paths or {
            'xi': 'output/xi_field_log.npy',
            'chi': 'output/chi_field_log.npy',
            'drift': 'output/drift_tensor_Xi.npy'
        }

        self.data = {}
        for k, v in self.data_paths.items():
            try:
                self.data[k] = load_field(v)
            except Exception as e:
                print(f"[WARNING] Failed to load {v}: {e}")
        
        self.current_frame = 0
        self.total_frames = next(iter(self.data.values())).shape[0] if self.data else 0

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

        # Export controls
        export_layout = QtWidgets.QHBoxLayout()
        self.export_button = QtWidgets.QPushButton("📤 Export Frame")
        self.export_button.clicked.connect(self.export_frame)
        self.export_format = QtWidgets.QComboBox()
        self.export_format.addItems(EXPORT_FORMATS)
        self.export_path = QtWidgets.QLineEdit("export_output/")
        self.export_field_name = QtWidgets.QLineEdit("Xi")
        export_layout.addWidget(QtWidgets.QLabel("Dir:"))
        export_layout.addWidget(self.export_path)
        export_layout.addWidget(QtWidgets.QLabel("Field Name:"))
        export_layout.addWidget(self.export_field_name)
        export_layout.addWidget(self.export_format)
        export_layout.addWidget(self.export_button)
        self.layout.addLayout(export_layout)

        self.update_frame(self.current_frame)

    def update_frame(self, frame):
        self.current_frame = frame if isinstance(frame, int) else frame
        self.gl_widget.clear()
        self.gl_widget.addItem(self.grid)

        for name, data in self.data.items():
            if self.checkboxes[name].isChecked():
                try:
                    slice_data = data[self.current_frame]
                except IndexError:
                    slice_data = data
                surf = gl.GLSurfacePlotItem(z=slice_data, shader='shaded', computeNormals=False)
                self.gl_widget.addItem(surf)

    def export_frame(self):
        out_dir = self.export_path.text().strip()
        os.makedirs(out_dir, exist_ok=True)
        field = self.export_field_name.text().strip()
        fmt = self.export_format.currentText()

        if field not in self.data:
            QtWidgets.QMessageBox.warning(self, "Export Error", f"Field '{field}' not loaded.")
            return

        slice_data = self.data[field]
        if slice_data.ndim == 4:
            slice_data = slice_data[self.current_frame]

        try:
            if fmt == '.npy':
                np.save(os.path.join(out_dir, f"{field}.npy"), slice_data)
            elif fmt == '.hdf5':
                export_to_hdf5(slice_data, filename=os.path.join(out_dir, f"{field}.h5"))
            elif fmt == 'LAMMPS':
                export_to_lammps(slice_data, filename=os.path.join(out_dir, f"{field}_lammps.data"))
            elif fmt == 'OpenFOAM':
                export_openfoam_field(slice_data, field_name=field, output_dir=out_dir)
            QtWidgets.QMessageBox.information(self, "Export Success", f"{field} exported as {fmt} in {out_dir}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Export Failed", str(e))


def main():
    app = QtWidgets.QApplication(sys.argv)
    viewer = FieldViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
"""

# Save to file
enhanced_viewer3d_path = "/mnt/data/viewer3d.py"
with open(enhanced_viewer3d_path, "w") as f:
    f.write(enhanced_viewer3d_code.strip())

enhanced_viewer3d_path
