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
    
    # fonts setup
    load_fonts()
    
    # main font for the whole project - otherwise overwritten
    # app.setFont(get_font("regular", 14))
    
    window = QMainWindow()
    
    check_existence()
    
    settings = get_settings()
    set_value("company_id", None)
    set_value("company_name", None)
    
    router = Router()
    window.setCentralWidget(router)
    window.setStyleSheet("background-color: #0F172A;")
    
    # gets and sets the app size to the size of the device
    screen = QGuiApplication.primaryScreen()
    size = screen.size()

    window.resize(size.width(), size.height())
    window.showMaximized()

    sys.exit(app.exec())
