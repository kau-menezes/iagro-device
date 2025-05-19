from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtGui import QPixmap, QColor, QPainter, QBrush
from PySide6.QtCore import QTimer, Qt

from shared.components.header import Header


class CircleIcon(QLabel):
    def __init__(self, pixmap_path, circle_color, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(pixmap_path).scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.circle_color = QColor(circle_color)
        self.setFixedSize(80, 80)  # circle + some padding

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw circle
        painter.setBrush(QBrush(self.circle_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        # Draw icon pixmap centered
        pixmap_x = (self.width() - self.pixmap.width()) // 2
        pixmap_y = (self.height() - self.pixmap.height()) // 2
        painter.drawPixmap(pixmap_x, pixmap_y, self.pixmap)