from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QSlider
)
from PySide6.QtCore import Qt


class ControlPanel(QWidget):

    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        self.setWindowTitle("FriendNet Controls")
        self.setMinimumWidth(250)

        layout = QVBoxLayout()

        # Simulation controls
        layout.addWidget(QLabel("Simulation Controls"))

        btn_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.step_btn = QPushButton("Step")

        self.start_btn.clicked.connect(
            lambda: self.interface.command_requested.emit("start", None)
        )
        self.stop_btn.clicked.connect(
            lambda: self.interface.command_requested.emit("stop", None)
        )
        self.step_btn.clicked.connect(
            lambda: self.interface.command_requested.emit("tick", None)
        )

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.step_btn)

        layout.addLayout(btn_layout)

        # Running/Paused Indicator
        self.interface.sim.running_changed.connect(self._on_running_changed)
        self.status_label = QLabel()
        self._on_running_changed(False)
        layout.addWidget(self.status_label)

        # Tick speed
        slider_default = 50

        self.min_interval = 0.1 # slowest
        self.max_interval = 10.0 # fastest
        self.interval = self._calculate_interval(slider_default/100.0)

        self.speed_label = QLabel(f"Tick Speed: {round(1/self.interval, 2)} ticks/s")
        layout.addWidget(self.speed_label)

        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setMinimum(1)
        speed_slider.setMaximum(100)
        speed_slider.setValue(slider_default)

        speed_slider.valueChanged.connect(self._update_speed)

        layout.addWidget(speed_slider)

        self.setLayout(layout)


    def _update_speed(self, value):
        # Normalize slider
        t = value / 100.0

        self.interval = self._calculate_interval(t)

        # Update Label
        self.speed_label.setText(f"Tick Speed: {round(1/self.interval, 2)} ticks/s")

        # Set speed via interface
        self.interface.command_requested.emit(
            "speed", [self.interval]
        )

    def _calculate_interval(self, t):
        # Return inverted mapping
        return self.max_interval - t * (self.max_interval - self.min_interval)


    def _on_running_changed(self, running: bool):
        if running:
            self.status_label.setText("Status: Running")
            self.status_label.setStyleSheet("font-weight: bold; color: #0a0;")

            self.start_btn.setEnabled(False)
            self.step_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:
            self.status_label.setText("Status: Paused")
            self.status_label.setStyleSheet("font-weight: bold; color: #b00;")

            self.start_btn.setEnabled(True)
            self.step_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
