from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import QTimer, Qt

from shared.components.header import Header
from utils.font_loader import get_font
from .components.status_icon import CircleIcon


class FieldScanningPage(QWidget):
    def __init__(self, router, field_name=None, parent=None):
        super().__init__(parent)
        self.router = router
        self.field_name = field_name or "Unknown Field"
        self.status = 0

        self.setWindowTitle("Field Scanning Page")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QFrame {
                background-color: #0F172A;
                border-radius: 12px;
                padding: 16px;
                margin: 0px;
            }
            
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = Header("Field Scanning", f"Checking {self.field_name}'s health.")
        layout.addWidget(header)

        # Timer container
        timer_container = QWidget()
        timer_container.setFixedSize(700, 300)
        timer_container.setStyleSheet("background-color: #0F172A; border-radius: 12px; padding: 30px;")
        timer_layout = QVBoxLayout(timer_container)

        self.icon_label = CircleIcon("assets/icons/clock.png", "#B4A647")
        timer_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        timer_label_layout = QHBoxLayout()
        self.timer_label = QLabel("Time Elapsed")
        self.timer_label.setStyleSheet("font-weight: bold; font-size: 24;")
        timer_label_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        self.elapsed_time_label = QLabel("00:00:00:00")
        self.elapsed_time_label.setStyleSheet("font-size: 24;")
        timer_label_layout.addWidget(self.elapsed_time_label, alignment=Qt.AlignCenter)

        timer_layout.addLayout(timer_label_layout)
        timer_layout.addSpacing(15)
        layout.addWidget(timer_container, alignment=Qt.AlignCenter)

        # Content container
        content_container = QWidget()
        content_container.setFixedSize(700, 400)
        content_container.setStyleSheet("background-color: #262F43; padding: 10px 20px 20px 20px; border-radius: 12px; margin: 0px;")
        content_layout = QVBoxLayout(content_container)
        

        # Wrapper layout for title + message
        status_wrapper = QWidget()
        status_layout = QVBoxLayout(status_wrapper)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)
        status_layout.setAlignment(Qt.AlignTop)

        # Title
        status_title = QLabel("Status")
        status_title.setStyleSheet("font-weight: bold; font-size: 24px;")
        status_title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        status_layout.addWidget(status_title)

        # Message
        self.status_message = QLabel("Scanning crops...")
        self.status_message.setAlignment(Qt.AlignTop)
        self.status_message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_message.setFont(get_font("light", 24))
        self.status_message.setStyleSheet("color: #4CAF50; font-weight: 200; font-size: 24px;")

        status_layout.addWidget(self.status_message)

        # Add to content
        content_layout.addWidget(status_wrapper)
        layout.addWidget(content_container, alignment=Qt.AlignCenter)

        layout.addSpacing(30)
        
        final_container = QWidget()
        final_container.setFixedSize(700, 100)
        final_layout = QHBoxLayout(final_container)
        final_layout.setAlignment(Qt.AlignCenter)
        
        # End Scan button
        self.end_scan_button = QPushButton("End Scan")
        self.end_scan_button.setStyleSheet(
            """
                background-color: #52A260;
                padding: 10px;
                border-radius: 8px;    
                font-size: 20px;
                font-weight: normal;                        
            """)
        
        self.end_scan_button.setFixedWidth(150)
        self.end_scan_button.setCursor(Qt.PointingHandCursor)
        self.end_scan_button.clicked.connect(self.end_scan)
        layout.addWidget(self.end_scan_button, alignment=Qt.AlignCenter)
        
        # Go Back button
        self.return_button = QPushButton("Go Back")
        self.return_button.setStyleSheet(
            """
                background-color: #4A4E59;
                padding: 10px;
                border-radius: 8px;    
                font-size: 20px;
                font-weight: normal;                        
            """)
        
        self.return_button.setFixedWidth(150)
        self.return_button.setCursor(Qt.PointingHandCursor)
        self.return_button.clicked.connect(self.go_back)
        layout.addWidget(self.return_button, alignment=Qt.AlignCenter)
        
        final_layout.addWidget(self.end_scan_button)
        final_layout.addWidget(self.return_button)
        
        self.return_button.setVisible(False)
        
        layout.addWidget(final_container, alignment=Qt.AlignCenter)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_ms = 0
        self.timer.start(10)

    def update_timer(self):
        self.elapsed_ms += 10
        ms = (self.elapsed_ms // 10) % 100
        s = (self.elapsed_ms // 1000) % 60
        m = (self.elapsed_ms // 60000) % 60
        h = (self.elapsed_ms // 3600000) % 24
        self.elapsed_time_label.setText(f"{h:02d}:{m:02d}:{s:02d}:{ms:02d}")

    def end_scan(self):
        self.return_button.setVisible(True)

        if self.status == 0:
            self.status = 1
            self.timer.stop()

            self.icon_label.circle_color = QColor("#4CAF50")
            self.icon_label.pixmap = QPixmap("assets/icons/check.png").scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.icon_label.update()

            self.status_message.setStyleSheet("color: #FFFFFF;")
            self.status_message.setText(
                "Area Scanned: 120 acres<br><br>"
                "Healthy Plants: 92%<br><br>"
                "<span style='color: #FF4C4C;'>Potential Diseases: 8%</span>"
            )
            self.status_message.setTextFormat(Qt.RichText)
            
            self.status_message.setStyleSheet("color: white; font-weight: 200; font-size: 24px;")

        

            self.end_scan_button.setEnabled(False)
            
    def reset_page(self):
        self.status = 0
        self.elapsed_ms = 0
        self.timer.start(10)

        self.elapsed_time_label.setText("00:00:00:00")

        self.status_message.setText("Scanning crops...")
        self.status_message.setTextFormat(Qt.PlainText)
        self.status_message.setStyleSheet("color: #4CAF50; font-weight: 200; font-size: 24px;")

        self.icon_label.circle_color = QColor("#B4A647")
        self.icon_label.pixmap = QPixmap("assets/icons/clock.png").scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.icon_label.update()

        self.end_scan_button.setEnabled(True)

        self.return_button.setVisible(False)
            
    def go_back(self):
        self.reset_page()
        
        self.router.navigate("field_selection")
