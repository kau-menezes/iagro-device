from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame
)
from .components.field_card import FieldCard

from shared.components.header import Header

class FieldSelectionPage(QWidget):
    
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.setWindowTitle("Field Selection Page")
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

        # header component
        header = Header("Select Field", "Tap on a field to start scanning.")
        
        layout.addWidget(header)

        
        grid = QGridLayout()
        grid.setVerticalSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        

        fields = ["Field A", "Field B", "Field C"]
        for i, name in enumerate(fields):
            card = FieldCard(name, "Brazil, Minas Gerais", "120", "Last Scan: 14 days ago")
            print(f"Creating card for {name}, {i}")
            card.clicked.connect(self.go_to_field_scan)
            grid.addWidget(card, i // 2, i % 2)
            
        layout.addSpacing(20)
        layout.addLayout(grid)
        layout.addStretch()
        
    def go_to_field_scan(self, field_name):
        print(f"Clicked on {field_name}")
        self.router.navigate("field_scanning", field_name=field_name)
