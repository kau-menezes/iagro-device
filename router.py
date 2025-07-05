from PySide6.QtWidgets import QStackedWidget
from PySide6.QtCore import QSettings
from pages.login.main import LoginPage
from pages.field_scanning.main import FieldScanningPage
from pages.field_selection.main import FieldSelectionPage
from utils.settings_manager import get_settings, get_value

class Router(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.routes = {
            "login": LoginPage,
            "field_selection": FieldSelectionPage,
            "field_scanning": FieldScanningPage
        }
        self.pages = {}
        
        settings = get_settings()
        
        if get_value("company_id") is None:
            self.navigate("login")   # MUDAR PARA PÁGINA DE LOGIN POSTERIORMENTE
        else:
            self.navigate("field_selection")  # initial page    
        

    def navigate(self, route_name, **kwargs):
        if route_name not in self.routes:
            print(f"Route '{route_name}' not found!")
            return

        if route_name not in self.pages:
            if route_name == "field_scanning":
                self.pages[route_name] = self.routes[route_name](self, kwargs.get("field_name", None))
            else:
                self.pages[route_name] = self.routes[route_name](self)

        if self.indexOf(self.pages[route_name]) == -1:
            self.addWidget(self.pages[route_name])
        self.setCurrentWidget(self.pages[route_name])

