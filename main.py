from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSettings
import sys
from PySide6.QtGui import QGuiApplication

from router import Router
from setup import check_existence
from utils.font_loader import load_fonts, get_font
from utils.settings_manager import get_settings, set_value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    load_fonts()
    # app.setFont(get_font("regular", 14))  # optional global font setting
    
    window = QMainWindow()
    
    check_existence()
    
    # Only reset company data if really needed
    # set_value("company_id", None)
    # set_value("company_name", None)
    
    router = Router()
    window.setCentralWidget(router)
    window.setStyleSheet("background-color: #0F172A;")
    
    window.showMaximized()
    sys.exit(app.exec())
