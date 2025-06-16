from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame, QHBoxLayout
)
from PySide6.QtGui import QPixmap

import qrcode

from PySide6.QtCore import Qt

import router
from shared.components.header import Header

class LoginPage(QWidget):
    def __init__(self, parent=None):
            super().__init__(parent)
            self.router = router
            self.setWindowTitle("Login Into Your IAgro Account")
            self.setMinimumSize(800, 600)

            # Ensure background fills
            self.setAutoFillBackground(True)
            self.setStyleSheet("background-color: #151D2C; color: white;")

            self.setStyleSheet("""
                QFrame {
                    background-color: #0F172A;
                    border-radius: 12px;
                    padding: 16px;
                }
                
                QLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                }
                
            """)

            layout = QVBoxLayout(self)  

            header = Header("Login", "Login into your account.")
            layout.addWidget(header)
            
            grid = QGridLayout()
            grid.setVerticalSpacing(20)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            h_box = QHBoxLayout()
            
            
            image_path = "assets/link/qrcode.png"  
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label = QLabel()
            
            label.setPixmap(scaled_pixmap)

            layout.addSpacing(20)
            layout.addLayout(grid)
            layout.addWidget(label)
            layout.addStretch()

