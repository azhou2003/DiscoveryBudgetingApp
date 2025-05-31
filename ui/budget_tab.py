from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton

class BudgetTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(4)
        self.budget_table.setHorizontalHeaderLabels(["Category", "Weekly Budget", "Actual Avg", "Over/Under"])
        self.layout.addWidget(self.budget_table)
        save_button = QPushButton("Update Budgets")
        save_button.clicked.connect(self.main_window.update_budget_comparison)
        save_config_btn = QPushButton("Save Budget Config")
        save_config_btn.clicked.connect(self.main_window.save_config)
        self.layout.addWidget(save_config_btn)
        load_config_btn = QPushButton("Load Budget Config")
        load_config_btn.clicked.connect(self.main_window.load_config)
        self.layout.addWidget(load_config_btn)
        self.layout.addWidget(save_button)
        self.setLayout(self.layout)