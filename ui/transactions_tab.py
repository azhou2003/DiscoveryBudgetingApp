from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget

class TransactionsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        main_layout = QHBoxLayout()
        # File selector
        file_selector_layout = QVBoxLayout()
        self.file_selector_table = QTableWidget()
        self.file_selector_table.setColumnCount(3)
        self.file_selector_table.setHorizontalHeaderLabels(["Include", "File", "Bank"])
        self.file_selector_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.file_selector_table.cellChanged.connect(self.main_window.on_file_selector_changed)
        file_selector_layout.addWidget(self.file_selector_table)
        # Transactions table
        trans_table_layout = QVBoxLayout()
        self.trans_table = QTableWidget()
        self.trans_table.setColumnCount(3)
        self.trans_table.setHorizontalHeaderLabels(["Date", "Category", "Amount"])
        trans_table_layout.addWidget(self.trans_table)
        main_layout.addLayout(file_selector_layout, 1)
        main_layout.addLayout(trans_table_layout, 1)
        self.setLayout(main_layout)