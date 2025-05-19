from PySide6.QtWidgets import (
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)

from PySide6.QtCore import Qt, Signal
from utils.font_loader import get_font

class FieldCard(QFrame):
    clicked = Signal(str) 
    
    def __init__(self, field_name, location, area, scan_info):
        super().__init__()
        self.field_name = field_name

        self.setObjectName("field_card")

        self.setStyleSheet("""
            QFrame {
                background-color: #2C3544;
                border-radius: 12px;
                padding: 16px;
            }
            
            QFrame#field_card:hover {
                background-color: #2C3544;
                border: 2px solid #39B465;
            }
            
            QLabel {
                color: white;
            }
            
            QPushButton {
                color: #39B465;
                background: transparent;
                border: none;
                font-weight: bold;
            }
            
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        
        self.setFixedSize(600, 280)
        

        self.setFont(get_font("regular", 14))
        self.setCursor(Qt.PointingHandCursor)
        
        # Layouts
        main_layout = QVBoxLayout(self)

        # Header (Field Name + Last Scan)
        header_layout = QHBoxLayout()
        label_field = QLabel(f"{field_name}")
        label_field.setFont(get_font("bold", 24))
        
        label_scan = QLabel(scan_info)
        label_scan.setFont(get_font("light", 16))
        label_scan.setStyleSheet("color: #cccccc;font-weight: 200;")
        
        label_scan.setAlignment(Qt.AlignRight)

        header_layout.addWidget(label_field)
        header_layout.addStretch()
        header_layout.addWidget(label_scan)

        # Body (Location)
        label_location = QLabel(location)
        label_location.setFont(get_font("light", 16))
        label_location.setStyleSheet("color: #cccccc;font-weight: 200;")
        
        # Body (Area)
        label_area = QLabel(f"{area} acres")
        label_area.setFont(get_font("light", 16))
        label_area.setStyleSheet("color: #cccccc; font-weight: 200;")
        

        # Footer (Start Scan button)
        scan_button = QPushButton("Start Scan  →")
        scan_button.setFont(get_font("bold", 16))
        scan_button.setCursor(Qt.PointingHandCursor)

        # Add widgets
        main_layout.addLayout(header_layout)
        main_layout.addWidget(label_location)
        main_layout.addWidget(label_area)
        main_layout.addStretch()
        main_layout.addWidget(scan_button, alignment=Qt.AlignRight)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
                self.clicked.emit(self.field_name) 