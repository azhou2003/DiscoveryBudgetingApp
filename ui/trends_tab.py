from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QSizePolicy
import pyqtgraph as pg
from .style_guide import spacing, fonts, colors

class TrendsTab(QWidget):
    """
    Tab for displaying spending trends and controls for category and comparison toggles.
    """
    def __init__(self, main_window):
        """
        Initialize the TrendsTab with category selector, budget/BLS toggles, and a plot area.

        Args:
            main_window: Reference to the main application window for callbacks.
        """
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        self.layout.setSpacing(spacing['md'])

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(spacing['md'])
        self.category_selector = QComboBox()
        self.category_selector.addItem("Total Spending")
        self.category_selector.setToolTip("Select a category to view its trend")
        self.category_selector.setMinimumWidth(spacing['xl'] * 2)
        self.category_selector.setMinimumHeight(fonts['base_size'] * 2)
        self.category_selector.currentIndexChanged.connect(self.main_window.update_trend_plot)
        controls_layout.addWidget(self.category_selector)
        self.show_budget_checkbox = QCheckBox("Show Budget")
        self.show_budget_checkbox.setChecked(True)
        self.show_budget_checkbox.setToolTip("Show your budget line on the plot")
        self.show_budget_checkbox.setMinimumHeight(fonts['base_size'] * 2)
        self.show_budget_checkbox.stateChanged.connect(self.main_window.update_trend_plot)
        controls_layout.addWidget(self.show_budget_checkbox)
        self.show_bls_checkbox = QCheckBox("Show BLS Avg")
        self.show_bls_checkbox.setChecked(True)
        self.show_bls_checkbox.setToolTip("Show BLS average line on the plot")
        self.show_bls_checkbox.setMinimumHeight(fonts['base_size'] * 2)
        self.show_bls_checkbox.stateChanged.connect(self.main_window.update_trend_plot)
        controls_layout.addWidget(self.show_bls_checkbox)
        controls_layout.addStretch(1)
        self.layout.addLayout(controls_layout)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(colors['background'])
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.plot_widget.setMinimumHeight(spacing['xl'] * 2)
        self.layout.addWidget(self.plot_widget, stretch=1)
        self.setLayout(self.layout)