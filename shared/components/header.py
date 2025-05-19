from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QFrame
)

from utils.font_loader import get_font

class Header(QFrame):
    def __init__(self, title_text, subtitle_text):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                border-radius: 12px;
                margin: 0px;
                padding: 0px;
            }
            
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
               
            }
        """)
        # self.setFixedHeight(80)

        layout = QVBoxLayout(self) 
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(0)

        title = QLabel(title_text)
        title.setFont(get_font("bold", 32))
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold; margin: 20 20 10 20")
        
        subtitle = QLabel(subtitle_text)
        subtitle.setFont(get_font("light", 24))
        subtitle.setStyleSheet("color: #cccccc;padding-left: 12px; font-weight: 200; margin: 0 20 20 20")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("border-bottom: 1px solid white;")
        layout.addWidget(line)
