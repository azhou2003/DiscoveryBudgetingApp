import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QVBoxLayout, QLabel, QPushButton, QTabWidget, QTextEdit
)
from PyQt6.QtCore import Qt
from budgeting.discover_activity_processing import DiscoverActProc

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discovery Budgeting App")
        self.setGeometry(100, 100, 1000, 600)

        self.processor = None

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_home_tab()
        self.init_transactions_tab()

    def init_home_tab(self):
        home_tab = QWidget()
        layout = QVBoxLayout()

        self.summary_label = QLabel("Load a CSV file to begin analysis.")
        layout.addWidget(self.summary_label)

        load_button = QPushButton("Load Discover CSV")
        load_button.clicked.connect(self.load_csv)
        layout.addWidget(load_button)

        home_tab.setLayout(layout)
        self.tabs.addTab(home_tab, "Home")

    def init_transactions_tab(self):
        self.trans_tab = QWidget()
        self.trans_layout = QVBoxLayout()

        self.trans_text = QTextEdit()
        self.trans_text.setReadOnly(True)
        self.trans_layout.addWidget(self.trans_text)

        self.trans_tab.setLayout(self.trans_layout)
        self.tabs.addTab(self.trans_tab, "Transactions")

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Discover CSV", "resources/", "CSV Files (*.csv)")
        if file_path:
            self.processor = DiscoverActProc(file_path)
            self.processor.analyze_spending()

            self.summary_label.setText(f"Loaded {file_path}\n\n"
                                        f"Date Range: {self.processor.start_date.date()} to {self.processor.end_date.date()}\n"
                                        f"Average Weekly Spending: ${self.processor.average_spending:.2f}")

            # Display transaction sample
            preview = ""
            for date, trans in list(self.processor.transactions_dict.items())[:10]:
                preview += f"{date.date()}\n"
                for cat, amt in trans:
                    preview += f"    {cat}: ${amt:.2f}\n"
            self.trans_text.setText(preview)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec())
