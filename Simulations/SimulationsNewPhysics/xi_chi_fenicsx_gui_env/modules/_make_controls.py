from PyQt5 import QtWidgets, QtCore

def dock_controls(plotter, widget, area='right', name='Controls'):
    areas = {
        'left': QtCore.Qt.LeftDockWidgetArea,
        'right': QtCore.Qt.RightDockWidgetArea,
        'top': QtCore.Qt.TopDockWidgetArea,
        'bottom': QtCore.Qt.BottomDockWidgetArea,
    }
    if hasattr(plotter, 'add_dock_widget'):
        return plotter.add_dock_widget(widget, area=area, name=name)

    parent = getattr(plotter, 'app_window', None) or getattr(plotter, 'window', None)
    if parent is None:
        raise RuntimeError("No Qt parent window found on the plotter to dock into.")

    dock = QtWidgets.QDockWidget(name, parent)
    dock.setObjectName(name.replace(' ', '_'))
    dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
    dock.setWidget(widget)
    parent.addDockWidget(areas.get(area, QtCore.Qt.RightDockWidgetArea), dock)
    if not hasattr(plotter, '_custom_docks'):
        plotter._custom_docks = []
    plotter._custom_docks.append(dock)
    return dock

def _call(viewer, method, *args, **kwargs):
    fn = getattr(viewer, method, None)
    if callable(fn): return fn(*args, **kwargs)

def build_controls(viewer):
    w = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout(w)
    form = QtWidgets.QFormLayout(); vbox.addLayout(form)

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    n = getattr(viewer, 'n_frames', None) or len(getattr(viewer, 'files', [])) or 1
    slider.setRange(0, max(0, n-1))
    slider.setValue(getattr(viewer, 'frame_index', 0))
    form.addRow('Frame', slider)

    row = QtWidgets.QHBoxLayout()
    btn_play, btn_pause = QtWidgets.QPushButton('Play'), QtWidgets.QPushButton('Pause')
    spin_ms = QtWidgets.QSpinBox(); spin_ms.setRange(1, 10000); spin_ms.setValue(int(getattr(viewer,'interval_ms',250))); spin_ms.setSuffix(' ms')
    row.addWidget(btn_play); row.addWidget(btn_pause); row.addWidget(spin_ms); vbox.addLayout(row)

    chk_axes = QtWidgets.QCheckBox('Axes'); chk_grid = QtWidgets.QCheckBox('Grid')
    vbox.addWidget(chk_axes); vbox.addWidget(chk_grid)

    slider.valueChanged.connect(lambda i: (_call(viewer,'set_frame',i) or setattr(viewer,'frame_index',i) or _call(viewer,'render')))
    btn_play.clicked.connect(lambda: _call(viewer,'play') or _call(viewer,'start') or _call(viewer,'toggle_play'))
    btn_pause.clicked.connect(lambda: _call(viewer,'pause') or _call(viewer,'stop'))
    spin_ms.valueChanged.connect(lambda ms: (setattr(viewer,'interval_ms',int(ms)) or _call(viewer,'set_interval_ms',int(ms))))
    chk_axes.toggled.connect(lambda on: (_call(viewer,'toggle_axes',on) or (_call(viewer,'show_axes') if on else _call(viewer,'hide_axes'))))
    chk_grid.toggled.connect(lambda on: _call(viewer,'toggle_grid',on))

    w.slider_frame, w.btn_play, w.btn_pause, w.spin_ms = slider, btn_play, btn_pause, spin_ms
    w.chk_axes, w.chk_grid = chk_axes, chk_grid
    return w
