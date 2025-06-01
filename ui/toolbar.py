from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .style_guide import spacing, fonts, colors

class ToolbarWidget(QToolBar):
    """
    Custom toolbar widget for the main window, including file actions, analyze button, date range label, and help/documentation icons.
    """
    def __init__(self, main_window):
        super().__init__("File Toolbar")
        self.setMovable(False)
        self.setStyleSheet(
            f"QToolBar {{ height: {fonts['base_size'] * 3.5}px; spacing: {spacing['md']}px; padding: {spacing['sm']}px {spacing['md']}px; }}"
        )
        self.main_window = main_window
        self._init_toolbar_contents()

    def _init_toolbar_contents(self):
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(spacing['sm'], spacing['sm'], spacing['sm'], spacing['sm'])
        toolbar_layout.setSpacing(spacing['md'])
        toolbar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        toolbar_widget.setLayout(toolbar_layout)

        # Left: Load CSV and BLS
        for text, tip, slot in [
            ("Load CSV", "Import a bank statement CSV file", self.main_window.load_csv),
            ("Load BLS", "Import BLS benchmark data (JSON)", self.main_window.load_bls)
        ]:
            btn = QPushButton(text)
            btn.setToolTip(tip)
            btn.clicked.connect(slot)
            btn.setMinimumHeight(int(fonts['base_size'] * 2.2))
            btn.setMinimumWidth(110)
            btn.setStyleSheet(f"font-size: {fonts['base_size'] + 2}px; padding: 6px 18px;")
            btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            toolbar_layout.addWidget(btn)

        # Middle: Analyze button and date range
        analyze_button = QPushButton("Analyze")
        analyze_button.setToolTip("Analyze spending for selected files and date range")
        analyze_button.clicked.connect(self.main_window.analyze_spending)
        analyze_button.setMinimumHeight(int(fonts['base_size'] * 2.2))
        analyze_button.setMinimumWidth(110)
        analyze_button.setStyleSheet(f"font-size: {fonts['base_size'] + 2}px; padding: 6px 18px;")
        analyze_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        toolbar_layout.addWidget(analyze_button)

        self.date_range_label = QLabel()
        self.date_range_label.setStyleSheet(f"font-size: {fonts['base_size']}px; font-weight: 500; margin: 0 {spacing['sm']}px;")
        self.date_range_label.setText("Date Range: Not loaded")
        toolbar_layout.addWidget(self.date_range_label)

        toolbar_layout.addStretch(1)

        # Right: Help and Documentation icons
        for icon_name, callback in [("help-circle", self.main_window.show_help_dialog), ("book-open", self.main_window.show_documentation)]:
            btn = QPushButton()
            btn.setToolTip(icon_name.replace('-', ' ').capitalize())
            btn.setIcon(QIcon.fromTheme(icon_name))
            btn.setFixedSize(fonts['base_size'] * 2, fonts['base_size'] * 2)
            btn.setStyleSheet(
                f"border: none; background: {colors['background_alt']}; border-radius: {fonts['base_size']}px;"
                f" QPushButton:hover {{ background: {colors['primary']}; color: #fff; }}"
                f" QPushButton:pressed {{ background: {colors['accent']}; color: #fff; }}"
            )
            btn.clicked.connect(callback)
            toolbar_layout.addWidget(btn)
        self.addWidget(toolbar_widget)

    def update_date_range_label(self, start_date, end_date):
        """
        Update the date range label in the toolbar.
        Args:
            start_date: datetime.date or None
            end_date: datetime.date or None
        """
        if start_date and end_date:
            start_str = start_date.strftime('%b %d, %Y')
            end_str = end_date.strftime('%b %d, %Y')
            self.date_range_label.setText(f"Date Range: {start_str} – {end_str}")
        else:
            self.date_range_label.setText("Date Range: Not loaded")
