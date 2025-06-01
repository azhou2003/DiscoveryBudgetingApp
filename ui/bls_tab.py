from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QSizePolicy, QSplitter, QLabel, QHeaderView
from PyQt6.QtCore import Qt
from .style_guide import spacing, fonts

class BLSTab(QWidget):
    """
    Tab for comparing user spending to BLS (Bureau of Labor Statistics) benchmarks.
    """
    def __init__(self, main_window):
        """
        Initialize the BLSTab with a BLS comparison table and category grouping placeholder.
        Args:
            main_window: Reference to the main application window for callbacks.
        """
        super().__init__()
        self.main_window = main_window

        bls_group = QWidget()
        bls_layout = QVBoxLayout()
        bls_layout.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        bls_layout.setSpacing(spacing['sm'])
        self.bls_table = QTableWidget()
        self.bls_table.setColumnCount(4)
        self.bls_table.setHorizontalHeaderLabels(["Category", "User Weekly Avg", "BLS Weekly Avg", "Diff"])
        self.bls_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.bls_table.setMinimumHeight(300)
        self.bls_table.setMinimumWidth(400)
        self.bls_table.setToolTip("Compare your spending to BLS averages")
        header = self.bls_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bls_table.verticalHeader().setDefaultSectionSize(36)
        bls_layout.addWidget(self.bls_table)
        bls_group.setLayout(bls_layout)
        bls_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        bls_vbox = QVBoxLayout()
        bls_vbox.setSpacing(spacing['sm'])
        bls_vbox.setContentsMargins(0, 0, 0, 0)
        bls_header = QLabel("BLS Comparison")
        bls_header.setStyleSheet(
            f"font-size: {fonts['heading_size']}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        bls_header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        bls_header.setContentsMargins(0, 0, 0, 0)
        bls_header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        bls_vbox.addWidget(bls_header)
        bls_vbox.addWidget(bls_group)
        bls_widget = QWidget()
        bls_widget.setLayout(bls_vbox)

        right_vbox = QVBoxLayout()
        right_vbox.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        right_vbox.setSpacing(spacing['sm'])
        right_label = QLabel("Category Grouping")
        right_label.setStyleSheet(
            f"font-size: {fonts['heading_size']-1}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        right_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        right_vbox.addWidget(right_label)
        right_content = QLabel("(Future: Group categories here)")
        right_content.setWordWrap(True)
        right_vbox.addWidget(right_content)
        right_vbox.addStretch(1)
        right_widget = QWidget()
        right_widget.setLayout(right_vbox)
        right_widget.setMinimumWidth(200)
        right_widget.setMaximumWidth(400)
        right_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        splitter.addWidget(bls_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 400])

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(spacing['lg'], spacing['lg'], spacing['lg'], spacing['lg'])
        main_layout.setSpacing(spacing['lg'])
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)