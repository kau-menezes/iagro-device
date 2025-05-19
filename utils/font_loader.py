from PySide6.QtGui import QFontDatabase, QFont

_fonts = {}

def load_fonts():
    global _fonts
    _fonts["regular"] = _register_font("assets/fonts/JosefinSans-Regular.ttf")
    _fonts["light"] = _register_font("assets/fonts/JosefinSans-Light.ttf")
    _fonts["bold"] = _register_font("assets/fonts/JosefinSans-Bold.ttf")

def _register_font(path):
    font_id = QFontDatabase.addApplicationFont(path)
    families = QFontDatabase.applicationFontFamilies(font_id)
    if families:
        return families[0]
    return None

def get_font(name: str, size: int = 14, weight: int = -1):
    family = _fonts.get(name)
    if family:
        font = QFont(family, size)
        if weight != -1:
            font.setWeight(weight)
        return font
    return QFont()
