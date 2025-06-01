from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QGroupBox, QSizePolicy, QSplitter, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from .style_guide import spacing, fonts

class TransactionsTab(QWidget):
    """
    Tab for managing and displaying transaction data and file selection in the budgeting app.
    """
    def __init__(self, main_window):
        """
        Initialize the TransactionsTab with file selector and transactions tables.
        Args:
            main_window: Reference to the main application window for callbacks.
        """
        super().__init__()
        self.main_window = main_window

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        # File selector group
        file_selector_group = QGroupBox()
        file_selector_group.setTitle("")
        file_selector_layout = QVBoxLayout()
        file_selector_layout.setContentsMargins(0, 0, 0, 0)
        file_selector_layout.setSpacing(spacing['sm'])
        self.file_selector_table = QTableWidget()
        self.file_selector_table.setColumnCount(3)
        self.file_selector_table.setHorizontalHeaderLabels(["Include", "File", "Bank"])
        self.file_selector_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.file_selector_table.cellChanged.connect(self.main_window.on_file_selector_changed)
        self.file_selector_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.file_selector_table.setMinimumHeight(300)
        self.file_selector_table.setMinimumWidth(320)
        self.file_selector_table.setToolTip("Select which files to include in analysis")
        self.file_selector_table.horizontalHeader().setStretchLastSection(True)
        self.file_selector_table.verticalHeader().setDefaultSectionSize(46)
        self.file_selector_table.setStyleSheet(
            "QTableWidget::item { padding: 8px 6px; }"
            "QTableWidget::indicator { width: 28px; height: 28px; margin: 4px; }"
            "QCheckBox { margin: 0 8px; }"
        )
        file_selector_layout.addWidget(self.file_selector_table)
        file_selector_group.setLayout(file_selector_layout)
        file_selector_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Data Files section header
        file_selector_header = QLabel("Data Files")
        file_selector_header.setStyleSheet(
            f"font-size: {fonts['heading_size']}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        file_selector_header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        file_selector_header.setContentsMargins(0, 0, 0, 0)
        file_selector_header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        data_files_vbox = QVBoxLayout()
        data_files_vbox.setSpacing(0)
        data_files_vbox.setContentsMargins(0, 0, 0, 0)
        data_files_vbox.addWidget(file_selector_header)
        data_files_vbox.addWidget(file_selector_group)
        data_files_widget = QWidget()
        data_files_widget.setLayout(data_files_vbox)

        # Transactions table group
        trans_group = QGroupBox()
        trans_group.setTitle("")
        trans_table_layout = QVBoxLayout()
        trans_table_layout.setContentsMargins(0, 0, 0, 0)
        trans_table_layout.setSpacing(spacing['sm'])
        self.trans_table = QTableWidget()
        self.trans_table.setColumnCount(3)
        self.trans_table.setHorizontalHeaderLabels(["Date", "Category", "Amount"])
        self.trans_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.trans_table.setMinimumHeight(400)
        self.trans_table.setMinimumWidth(500)
        self.trans_table.setToolTip("All transactions from selected files")
        self.trans_table.horizontalHeader().setStretchLastSection(True)
        self.trans_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.trans_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.trans_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.trans_table.verticalHeader().setDefaultSectionSize(47)
        self.trans_table.setStyleSheet("QTableWidget { border-bottom: 1.5px solid #4A90E2; } QTableWidget::item { padding: 8px 6px; }")
        trans_table_container = QWidget()
        trans_table_container_layout = QVBoxLayout()
        trans_table_container_layout.setContentsMargins(0, 0, 0, 0)
        trans_table_container_layout.setSpacing(0)
        trans_table_container.setLayout(trans_table_container_layout)
        trans_table_container_layout.addWidget(self.trans_table)
        trans_table_layout.addWidget(trans_table_container)
        trans_group.setLayout(trans_table_layout)
        trans_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Transactions section header
        trans_header = QLabel("Transactions")
        trans_header.setStyleSheet(
            f"font-size: {fonts['heading_size']}px; font-weight: {fonts['heading_weight']}; margin-bottom: {spacing['sm']}px;"
        )
        trans_header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        trans_header.setContentsMargins(0, 0, 0, 0)
        trans_header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        trans_vbox = QVBoxLayout()
        trans_vbox.setSpacing(0)
        trans_vbox.setContentsMargins(0, 0, 0, 0)
        trans_vbox.addWidget(trans_header)
        trans_vbox.addWidget(trans_group)
        trans_widget = QWidget()
        trans_widget.setLayout(trans_vbox)

        splitter.addWidget(data_files_widget)
        splitter.addWidget(trans_widget)
        splitter.setSizes([350, 650])

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(spacing['md'], spacing['md'], spacing['md'], spacing['md'])
        main_layout.setSpacing(spacing['md'])
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Remove borders for a clean look
        file_selector_group.setStyleSheet("QGroupBox { border: none; }")
        trans_group.setStyleSheet("QGroupBox { border: none; }")

        # Consistent internal padding
        for group in [file_selector_group, trans_group]:
            group.layout().setContentsMargins(spacing['sm'], spacing['sm'], spacing['sm'], spacing['sm'])
            group.layout().setSpacing(spacing['sm'])

        self.file_selector_table.horizontalHeader().setSectionResizeMode(self.file_selector_table.horizontalHeader().ResizeMode.Stretch)
        for col in range(self.file_selector_table.columnCount()):
            self.file_selector_table.horizontalHeader().setSectionResizeMode(col, self.file_selector_table.horizontalHeader().ResizeMode.Stretch)
        self.trans_table.horizontalHeader().setSectionResizeMode(self.trans_table.horizontalHeader().ResizeMode.Stretch)
        for col in range(self.trans_table.columnCount()):
            self.trans_table.horizontalHeader().setSectionResizeMode(col, self.trans_table.horizontalHeader().ResizeMode.Stretch)