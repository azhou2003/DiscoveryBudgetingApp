from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class TrendsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.category_selector = QComboBox()
        self.category_selector.addItem("Total Spending")
        self.category_selector.currentIndexChanged.connect(self.main_window.update_trend_plot)
        self.layout.addWidget(self.category_selector)
        self.trend_controls_layout = QHBoxLayout()
        self.show_budget_checkbox = QCheckBox("Show Budget")
        self.show_budget_checkbox.setChecked(True)
        self.show_budget_checkbox.stateChanged.connect(self.main_window.update_trend_plot)
        self.trend_controls_layout.addWidget(self.show_budget_checkbox)
        self.show_bls_checkbox = QCheckBox("Show BLS Avg")
        self.show_bls_checkbox.setChecked(True)
        self.show_bls_checkbox.stateChanged.connect(self.main_window.update_trend_plot)
        self.trend_controls_layout.addWidget(self.show_bls_checkbox)
        self.layout.addLayout(self.trend_controls_layout)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)