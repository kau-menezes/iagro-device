from PySide6.QtCore import QSettings

def get_settings():
    return QSettings("IAgro", "IAgroApp")

def get_value(key, default=None):
    return get_settings().value(key, default)

def set_value(key, value):
    get_settings().setValue(key, value)