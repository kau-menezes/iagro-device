from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

import router

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.router = router

        layout = QVBoxLayout()

        label = QLabel("This is the Login Page")

