from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class ControlPanel(QWidget):
    def __init__(self, callbacks):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Simulation Controls")
        self.layout.addWidget(self.label)

        self.start_btn = QPushButton("Start Simulation")
        self.start_btn.clicked.connect(callbacks["start"])
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Simulation")
        self.stop_btn.clicked.connect(callbacks["stop"])
        self.layout.addWidget(self.stop_btn)
