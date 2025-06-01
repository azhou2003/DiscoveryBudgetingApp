"""
Theme manager for applying the application's color palette and style system.
"""

from PyQt6.QtGui import QFontDatabase, QFont
from qt_material import apply_stylesheet
from .style_guide import colors, spacing, fonts

LIGHT_PALETTE = {
    "primaryColor": colors['primary'],
    "accentColor": colors['accent'],
    "background": colors['background'],
    "secondaryBackground": colors['background_alt'],
    "text": colors['text']
}

def apply_theme(app):
    """
    Apply the application's theme, fonts, and color palette to the given QApplication.

    Args:
        app: QApplication instance to style.
    """
    try:
        font_id = QFontDatabase.addApplicationFont(":/fonts/Roboto-Regular.ttf")
        size = fonts['base_size']
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                app.setFont(QFont(families[0], size))
        else:
            app.setFont(QFont("Segoe UI", size))
    except Exception:
        app.setFont(QFont("Segoe UI", 15))
    apply_stylesheet(app, theme='light_blue.xml', extra=LIGHT_PALETTE)
    app.setStyleSheet(app.styleSheet() + "\n"
        "QWidget, QMainWindow, QTabWidget, QGroupBox, QTableWidget, QComboBox, QLineEdit, QCheckBox, QPushButton, QLabel, QScrollArea, QHeaderView, QAbstractItemView, QFrame {"
        f"background-color: {colors['background']}; color: {colors['text']}; border-color: {colors['primary']}; font-size: {fonts['base_size']}px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }}\n"
        f"QHeaderView::section {{ background-color: {colors['background_alt']}; color: {colors['text']}; font-size: {fonts['base_size'] - 1}px; padding: {spacing['sm']}px {spacing['xs']}px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }}\n"
        "QTabBar::tab:selected { background: #E3F2FD; color: #222; font-weight: bold; }\n"
        "QTabBar::tab { background: #fff; color: #222; min-width: 160px; min-height: 40px; padding: 12px 24px; border-radius: 8px 8px 0 0; margin-right: 4px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QTabWidget::pane { border-top: 2px solid #4A90E2; margin-top: 2px; }\n"
        "QPushButton { background: #E3F2FD; color: #222; border-radius: 8px; border: 1.5px solid #4A90E2; padding: 10px 24px; font-size: 16px; font-weight: 500; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QPushButton:checked, QPushButton:pressed { background: #FFA726; color: #fff; }\n"
        "QPushButton:focus { background: #E3F2FD; color: #222; border: 1.5px solid #4A90E2; }\n"
        "QPushButton:!hover:!pressed:!checked { background: #E3F2FD; color: #222; border: 1.5px solid #4A90E2; }\n"
        "QLineEdit, QComboBox { min-height: 36px; border-radius: 6px; border: 1.5px solid #4A90E2; padding: 6px 12px; font-size: 16px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QLineEdit:hover, QComboBox:hover { border: 1.5px solid #FFA726; background: #F5F7FA; }\n"
        "QLineEdit:focus, QComboBox:focus { border: 1.5px solid #FFA726; background: #FFF3E0; }\n"
        "QTableWidget { gridline-color: #E3F2FD; font-size: 15px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QTableWidget QTableView { background: #fff; color: #222; }\n"
        "QGroupBox { border: 1.5px solid #4A90E2; border-radius: 10px; margin-top: 16px; font-size: 17px; font-weight: 600; padding: 12px 16px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QLabel { font-size: 16px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QCheckBox { font-size: 15px; min-height: 28px; padding-left: 32px; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }\n"
        "QCheckBox::indicator { width: 24px; height: 24px; border-radius: 6px; border: 2px solid #4A90E2; background: #fff; margin-right: 8px; }\n"
        "QCheckBox::indicator:checked { background: #4A90E2; border: 2px solid #4A90E2; image: url(); }\n"
        "QCheckBox::indicator:unchecked { background: #fff; border: 2px solid #4A90E2; }\n"
        "QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:focus { background: #FFA726; border: 2px solid #FFA726; }\n"
        "QCheckBox:hover { color: #4A90E2; }\n"
        "QCheckBox::indicator:hover { border: 2px solid #FFA726; background: #E3F2FD; }\n"
        "QScrollBar:vertical, QScrollBar:horizontal { background: #F5F7FA; width: 14px; border-radius: 7px; }\n"
        "QScrollBar::handle { background: #4A90E2; border-radius: 7px; min-height: 30px; }\n"
        "QScrollBar::add-line, QScrollBar::sub-line { background: none; }\n"
        "QToolBar { background: #fff; border-bottom: 2px solid #E3F2FD; padding: 8px 16px; }\n"
    )
