from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QSlider
)
from PySide6.QtCore import Qt


VIEW_MODES = [
    ("Friends", "friends"),
    ("Gossip", "gossip"),
    ("Trust", "trust"),
]

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

        # View controls
        self.interface.view_changed.connect(self._update_view_buttons)
        layout.addWidget(QLabel("View Mode"))

        self.view_buttons = {}
        view_layout = QHBoxLayout()

        for label, mode in VIEW_MODES:
            btn = QPushButton(label)
            btn.setCheckable(False)

            btn.clicked.connect(
                lambda checked=False, m=mode: self._set_view(m)
            )

            self.view_buttons[mode] = btn
            view_layout.addWidget(btn)

        layout.addLayout(view_layout)
        self._update_view_buttons("friends")

        # Rumor Browser
        layout.addWidget(QLabel("Rumor Browser"))

        self.rumor_index = 0

        rumor_btn_layout = QHBoxLayout()

        self.prev_rumor_btn = QPushButton("◀ Prev")
        self.next_rumor_btn = QPushButton("Next ▶")

        self.prev_rumor_btn.clicked.connect(self._prev_rumor)
        self.next_rumor_btn.clicked.connect(self._next_rumor)

        rumor_btn_layout.addWidget(self.prev_rumor_btn)
        rumor_btn_layout.addWidget(self.next_rumor_btn)

        layout.addLayout(rumor_btn_layout)

        self.rumor_label = QLabel("No rumors")
        self.rumor_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.rumor_label)

        self.interface.rumor_added.connect(self._on_rumor_added)
        self.interface.rumor_selected.connect(self._on_rumor_selected)

        self._update_rumor_controls() # Initialize disabled state

        # Set finalized layout
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


    def _set_view(self, mode: str):
        # Issue command
        self.interface.command_requested.emit("view", [mode])

    def _update_view_buttons(self, active_mode: str):
        for mode, btn in self.view_buttons.items():
            if mode == active_mode:
                btn.setEnabled(False)
                btn.setStyleSheet("font-weight: bold;")
            else:
                btn.setEnabled(True)
                btn.setStyleSheet("")


    def _prev_rumor(self):
        if self.rumor_index > 0:
            self.rumor_index -= 1
            self._show_rumor()

    def _next_rumor(self):
        if self.rumor_index < len(self.interface.sim.rumors) - 1:
            self.rumor_index += 1
            self._show_rumor()

    def _update_rumor_controls(self):
        self.rumor_index = len(self.interface.sim.rumors) - 1
        self._show_rumor()

    def _on_rumor_added(self):
        # Snap to newest rumor
        self.rumor_index = len(self.interface.sim.rumors) - 1
        self._show_rumor()

    def _on_rumor_selected(self, rumor):
        # Minimal, readable display
        self.rumor_label.setText(
            f"{rumor.spreader} -> {rumor.target}\n"
            f"“{rumor.rumor}”\n"
            f"Rumor {self.rumor_index + 1} / {len(self.interface.sim.rumors)}"
        )

    def _show_rumor(self):
        rumors = self.interface.sim.rumors

        if not rumors:
            self.rumor_label.setText("No rumors")
            self.prev_rumor_btn.setEnabled(False)
            self.next_rumor_btn.setEnabled(False)
            return

        self.rumor_index = max(0, min(self.rumor_index, len(rumors) - 1))

        self.prev_rumor_btn.setEnabled(self.rumor_index > 0)
        self.next_rumor_btn.setEnabled(self.rumor_index < len(rumors) - 1)

        self.interface.select_rumor(rumors[self.rumor_index])


