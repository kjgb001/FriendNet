from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QRadioButton, QGroupBox,
    QCheckBox, QLineEdit
)
from PySide6.QtCore import Signal, QSettings


class StartupMenu(QWidget):
    """
    GUI front-door for FriendNet.
    Collects configuration and emits a start signal.
    """

    start_requested = Signal(dict)

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.settings = QSettings("FriendNet", "StartupMenu")

        def _on_close(event):
            # Tell the app to stop
            self.sim.interface.shutdown()

        self.setWindowTitle("FriendNet: New Simulation")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Population
        layout.addWidget(QLabel("Population Size"))

        self.population = QSpinBox()
        self.population.setRange(1, 500)
        self.population.setValue(50)
        layout.addWidget(self.population)

        # Graph Representation
        layout.addWidget(QLabel("Graph Representation"))

        rep_box = QGroupBox()
        rep_layout = QHBoxLayout()

        self.rep_list = QRadioButton("Adjacency List")
        self.rep_matrix = QRadioButton("Adjacency Matrix")
        self.rep_list.setChecked(True)

        rep_layout.addWidget(self.rep_list)
        rep_layout.addWidget(self.rep_matrix)
        rep_box.setLayout(rep_layout)
        layout.addWidget(rep_box)

        # Graph Types
        layout.addWidget(QLabel("Graphs to Load"))

        self.chk_friends = QCheckBox("Friends (Undirected)")
        self.chk_gossip = QCheckBox("Gossip (Directed)")
        self.chk_trust   = QCheckBox("Trust/Friends (Weighted)")

        self.chk_friends.setChecked(True)
        self.chk_gossip.setChecked(True)
        self.chk_trust.setChecked(True)

        layout.addWidget(self.chk_friends)
        layout.addWidget(self.chk_gossip)
        layout.addWidget(self.chk_trust)

        # People Generation
        layout.addWidget(QLabel("People Generation"))

        gen_layout = QHBoxLayout()

        self.gen_count = QSpinBox()
        self.gen_count.setRange(1, 500)
        self.gen_count.setValue(50)

        gen_btn = QPushButton("Generate")

        gen_btn.clicked.connect(self._generate_people)

        gen_layout.addWidget(self.gen_count)
        gen_layout.addWidget(gen_btn)

        layout.addLayout(gen_layout)

        # People location
        layout.addWidget(QLabel("People Dataset"))

        self.location = QLineEdit("generated_set")
        layout.addWidget(self.location)

        # Load Dataset button
        load_btn = QPushButton("Load Dataset")
        load_btn.clicked.connect(self._confirm_location)
        layout.addWidget(load_btn)

        # People Status (Enough People?)
        self.dataset_status = QLabel("")
        layout.addWidget(self.dataset_status)

        # Start button
        self.start_btn = QPushButton("Start Simulation") # Assign as attribute to access in _emit_start()
        self.start_btn.clicked.connect(self._emit_start)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

        # Track population and location changes, then validate the selected dataset after loading state
        self.population.valueChanged.connect(self._validate_dataset)
        self.location.textChanged.connect(self._on_location_edit)
        self.confirmed_location = self.location.text()

        # Load State and Connect Save Signals
        self._load_state()
        self._connect_save_signals()

        # Validation
        self._validate_dataset()


    def _emit_start(self):
        if not self.start_btn.isEnabled():
            return
            
        load_list = []

        if self.chk_trust.isChecked():
            load_list.append("weighted")
        if self.chk_friends.isChecked():
            load_list.append("undirected")
        if self.chk_gossip.isChecked():
            load_list.append("directed")

        config = {
            "populate": self.population.value(),
            "rep": "matrix" if self.rep_matrix.isChecked() else "list",
            "load": load_list,
            "location": self.location.text()
        }

        self._save_state() # Ensure final state is saved

        self.start_btn.setEnabled(False) # Disable button immediately before emmitting to avoid potential bugs
        self.start_requested.emit(config)
        self.close()


    def _generate_people(self):
        count = self.gen_count.value()
        location = self.location.text()

        # Call the existing CLI command logic
        self.interface.handle("generate", [count, location])

        self._validate_dataset()

    def _confirm_location(self):
        self.confirmed_location = self.location.text()
        valid = self._validate_dataset()
        if valid:
            self._save_state()

    def _on_location_edit(self):
        self.start_btn.setEnabled(False)
        self.dataset_status.setText("Dataset path modified: click 'Load Dataset'")
        self.dataset_status.setStyleSheet("color: #aa0;")

    def _validate_dataset(self):
        from utils.peopleIO import load_people

        location = self.confirmed_location
        required = self.population.value()

        try:
            people = load_people(f"assets/people/{location}.json")
            count = len(people)
        except Exception:
            count = 0

        if not people:
            self.dataset_status.setText(
                f"File does not exist or cannot be parsed."
            )
            self.dataset_status.setStyleSheet("color: #b00;")
            self.start_btn.setEnabled(False)
            return False
        elif count < required:
            self.dataset_status.setText(
                f"Dataset has {count} people, but {required} required."
            )
            self.dataset_status.setStyleSheet("color: #b00;")
            self.start_btn.setEnabled(False)
        else:
            self.dataset_status.setText(
                f"Dataset OK ({count} people available)."
            )
            self.dataset_status.setStyleSheet("color: #0a0;")
            self.start_btn.setEnabled(True)
        return True


    def _connect_save_signals(self):
        self.population.valueChanged.connect(self._save_state)
        self.rep_list.toggled.connect(self._save_state)
        self.rep_matrix.toggled.connect(self._save_state)

        self.chk_friends.toggled.connect(self._save_state)
        self.chk_gossip.toggled.connect(self._save_state)
        self.chk_trust.toggled.connect(self._save_state)

        self.gen_count.valueChanged.connect(self._save_state)

    def _save_state(self):
        self.settings.setValue("population", self.population.value())
        self.settings.setValue(
            "rep",
            "matrix" if self.rep_matrix.isChecked() else "list"
        )
        self.settings.setValue("friends", self.chk_friends.isChecked())
        self.settings.setValue("gossip", self.chk_gossip.isChecked())
        self.settings.setValue("trust", self.chk_trust.isChecked())
        self.settings.setValue("gen_count", self.gen_count.value())
        self.settings.setValue("location", self.confirmed_location)

    def _load_state(self):
        self.population.setValue(
            self.settings.value("population", 50, int)
        )

        rep = self.settings.value("rep", "list")
        if rep == "matrix":
            self.rep_matrix.setChecked(True)
        else:
            self.rep_list.setChecked(True)

        self.chk_friends.setChecked(
            self.settings.value("friends", True, bool)
        )
        self.chk_gossip.setChecked(
            self.settings.value("gossip", True, bool)
        )
        self.chk_trust.setChecked(
            self.settings.value("trust", True, bool)
        )

        self.gen_count.setValue(
            self.settings.value("gen_count", 50, int)
        )

        self.confirmed_location = self.settings.value(
            "location", "generated_set"
        )
        self.location.setText(self.confirmed_location)
