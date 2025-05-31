from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget

class BLSTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.bls_table = QTableWidget()
        self.bls_table.setColumnCount(4)
        self.bls_table.setHorizontalHeaderLabels(["Category", "User Avg", "BLS Avg", "Difference"])
        self.layout.addWidget(self.bls_table)
        self.setLayout(self.layout)