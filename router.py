from PySide6.QtWidgets import QStackedWidget
from pages.login.main import LoginPage
from pages.field_scanning.main import FieldScanningPage
from pages.field_selection.main import FieldSelectionPage

class Router(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.routes = {
            "login": LoginPage,
            "field_selection": FieldSelectionPage,
            "field_scanning": FieldScanningPage
        }
        self.pages = {}
        self.navigate("field_selection")  # Set the initial page    

    def navigate(self, route_name, **kwargs):
        if route_name not in self.routes:
            print(f"Route '{route_name}' not found!")
            return

        # If not already created, instantiate and cache the page
        if route_name not in self.pages:
            self.pages[route_name] = self.routes[route_name](self, kwargs.get('field_name', None))

        # Add to stack and show it
        if self.indexOf(self.pages[route_name]) == -1:
            self.addWidget(self.pages[route_name])
        self.setCurrentWidget(self.pages[route_name])
