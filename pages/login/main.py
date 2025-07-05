from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame, QHBoxLayout, QStackedWidget
)
from PySide6.QtGui import QPixmap

import qrcode

from PySide6.QtCore import Qt, QTimer

import router
from shared.components.header import Header
import requests

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Accept router as a parameter if passed, else None
        self.router = parent if isinstance(parent, QStackedWidget) else None
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
        # Add polling timer for device status
        self.device_code = "123device123uhul"
        self.api_url = f"http://localhost:5215/api/devices/{self.device_code}"
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.check_device_status)
        self.poll_timer.start(5000)  # every 5 seconds

    def check_device_status(self):
        try:
            response = requests.get(self.api_url, timeout=3)
            if response.ok:
                data = response.json()
                if data.get("companyId") is not None:
                    self.poll_timer.stop()
                    if self.router is not None and hasattr(self.router, "navigate"):
                        self.router.navigate("field_selection")
        except Exception as e:
            print(f"Device status check failed: {e}")

