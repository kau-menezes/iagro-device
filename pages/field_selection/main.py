from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QGridLayout, QFrame
)
from .components.field_card import FieldCard

from shared.components.header import Header
import requests
from utils.settings_manager import get_value

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

        # Fetch fields from API
        self.fields = self.fetch_fields()
        for i, field in enumerate(self.fields):
            name = field.get("nickname", f"Field {i+1}")
            area = str(int(field.get("area", 0)))
            card = FieldCard(name, "Brazil, Minas Gerais", area, "Last Scan: 14 days ago")
            print(f"Creating card for {name}, {i}")
            card.clicked.connect(lambda checked, name=card.field_name: self.go_to_field_scan(card.field_name))
            
            grid.addWidget(card, i // 2, i % 2)
            
        layout.addSpacing(20)
        layout.addLayout(grid)
        layout.addStretch()
        
    def fetch_fields(self):
        company_id = get_value("company_id")
        if not company_id:
            print("No company_id found in QSettings.")
            return []
        url = f"http://localhost:5215/api/fields/company/{company_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.ok:
                return response.json()
            else:
                print(f"Failed to fetch fields: {response.status_code}")
        except Exception as e:
            print(f"Error fetching fields: {e}")
        return []

    def go_to_field_scan(self, field_name):
        print(f"Clicked on {field_name}")
        self.router.navigate("field_scanning", field_name=field_name)
