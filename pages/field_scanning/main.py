import os
import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import QTimer, Qt

from shared.components.header import Header
from utils.font_loader import get_font
from .components.status_icon import CircleIcon
from manual_labeling import analyze

import cv2
import numpy as np
import tensorflow as tf
import threading
import json
from datetime import datetime
from geopy.geocoders import Nominatim
from tensorflow import keras


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

        # main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # header
        header = Header("Field Scanning", f"Checking {self.field_name}'s health.")
        layout.addWidget(header)

        # timer container
        timer_container = QWidget()
        timer_container.setFixedSize(700, 300)
        timer_container.setStyleSheet("background-color: #0F172A; border-radius: 12px; padding: 30px;")
        timer_layout = QVBoxLayout(timer_container)

        self.icon_label = CircleIcon("assets/icons/clock.png", "#B4A647")
        timer_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        timer_label_layout = QHBoxLayout()
        self.timer_label = QLabel("Time Elapsed")
        self.timer_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        timer_label_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        self.elapsed_time_label = QLabel("00:00:00:00")
        self.elapsed_time_label.setStyleSheet("font-size: 24px;")
        timer_label_layout.addWidget(self.elapsed_time_label, alignment=Qt.AlignCenter)

        timer_layout.addLayout(timer_label_layout)
        timer_layout.addSpacing(15)
        layout.addWidget(timer_container, alignment=Qt.AlignCenter)

        # content container
        content_container = QWidget()
        content_container.setFixedSize(700, 400)
        content_container.setStyleSheet("background-color: #262F43; padding: 10px 20px 20px 20px; border-radius: 12px; margin: 0px;")
        content_layout = QVBoxLayout(content_container)

        # wrapper layout for title + message
        status_wrapper = QWidget()
        status_layout = QVBoxLayout(status_wrapper)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)
        status_layout.setAlignment(Qt.AlignTop)

        # title
        status_title = QLabel("Status")
        status_title.setStyleSheet("font-weight: bold; font-size: 24px;")
        status_title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        status_layout.addWidget(status_title)

        # message
        self.status_message = QLabel("Scanning crops...")
        self.status_message.setAlignment(Qt.AlignTop)
        self.status_message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_message.setFont(get_font("light", 24))
        self.status_message.setStyleSheet("color: #4CAF50; font-weight: 200; font-size: 24px;")

        status_layout.addWidget(self.status_message)

        # add to content
        content_layout.addWidget(status_wrapper)
        layout.addWidget(content_container, alignment=Qt.AlignCenter)

        layout.addSpacing(30)
        
        final_container = QWidget()
        final_container.setFixedSize(700, 100)
        final_layout = QHBoxLayout(final_container)
        final_layout.setAlignment(Qt.AlignCenter)
        
        # end scan button
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
        
        # go back button
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

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_ms = 0
        self.timer.start(10)

        # TensorFlow model and webcam initialization
        self.model = self.load_model()
        self.class_names = self.load_class_names()
        self.capture = None
        self.scanning = False
        self.detections = []
        self.geolocator = Nominatim(user_agent="plant_disease_app")
        self.location = self.get_location()
        self.frame_thread = None

        self.start_scan()

    def update_timer(self):
        self.elapsed_ms += 10
        ms = (self.elapsed_ms // 10) % 100
        s = (self.elapsed_ms // 1000) % 60
        m = (self.elapsed_ms // 60000) % 60
        h = (self.elapsed_ms // 3600000) % 24
        self.elapsed_time_label.setText(f"{h:02d}:{m:02d}:{s:02d}:{ms:02d}")

    def load_model(self):
        try:
            # Load model without compiling (avoids errors from old optimizer/loss configs)
            model = keras.models.load_model("potatoes.h5", compile=False)
            print("Model loaded successfully.")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None


    def load_class_names(self):
        # Replace with your actual class names if available
        return [f"Class_{i}" for i in range(39)]

    def get_location(self):
        try:
            location = self.geolocator.geocode("me")
            if location:
                return {"latitude": location.latitude, "longitude": location.longitude}
        except Exception as e:
            print(f"Error getting location: {e}")
        return {"latitude": None, "longitude": None}

    def start_scan(self):
        self.scanning = True
        # Run manual labeling in a background thread so the GUI stays responsive
        def run_manual_labeling():
            analyze(self.model)
            self.scanning = False
        self.frame_thread = threading.Thread(target=run_manual_labeling, daemon=True)
        self.frame_thread.start()
        self.end_scan_button.setEnabled(True)
        self.end_scan_button.setVisible(True)
        self.return_button.setVisible(False)

    def process_frames(self):
        while self.scanning and self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:
                continue
            # Show the camera frame in a window
            cv2.imshow('Camera - Press Q to close', frame)
            # Preprocess frame for model
            input_frame = cv2.resize(frame, (256, 256))  # Match training size
            input_frame = input_frame / 255.0
            input_tensor = np.expand_dims(input_frame, axis=0).astype(np.float32)
            # Run inference
            try:
                if self.model and self.scanning:  # Check scanning flag before inference
                    pred = self.model.predict(input_tensor)
                    class_idx = int(np.argmax(pred)) if pred.shape[-1] > 1 else int(pred[0] > 0.5)
                    class_names = ["Potato___Early_blight", "Potato___Late_blight", "Potato___healthy"]
                    class_name = class_names[class_idx] if class_idx < len(class_names) else str(class_idx)
                    if class_name != "Potato___healthy":
                        detection = {
                            "datetime": datetime.now().isoformat(),
                            "location": self.location,
                            "class": class_name
                        }
                        self.detections.append(detection)
                        self.status_message.setText(f"Detected: {class_name}")
                    else:
                        self.status_message.setText("Scanning crops...")
            except Exception as e:
                print(f"Inference error: {e}")
            # Allow user to close the camera window with 'q'
            if cv2.waitKey(10) & 0xFF == ord('q'):
                self.scanning = False
                break
            # Wait 1 seconds before next frame analysis
            for _ in range(100):
                if not self.scanning:
                    break
                cv2.waitKey(1)  # 1ms * 100 = 1s
        cv2.destroyAllWindows()

    def end_scan(self):
        self.scanning = False  # Stop AI analysis immediately
        if self.capture:
            self.capture.release()
        cv2.destroyAllWindows()
        if self.detections:
            filename = f"detection_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(self.detections, f, indent=2)
            self.status_message.setText(f"Scan complete. Results saved to {filename}")
        else:
            self.status_message.setText("Scan complete. No diseases detected.")

        self.return_button.setVisible(True)
        if self.status == 0:
            self.status = 1
            self.timer.stop()
            self.icon_label.circle_color = QColor("#4CAF50")
            self.icon_label.pixmap = QPixmap("assets/icons/check.png").scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.icon_label.update()
            self.status_message.setStyleSheet("color: white; font-weight: 200; font-size: 24px;")
            self.end_scan_button.setEnabled(False)

    def reset_page(self):
        self.status = 0
        self.elapsed_ms = 0
        self.timer.start(10)
        self.elapsed_time_label.setText("00:00:00:00")
        self.status_message.setText("Scanning crops...")
        self.status_message.setStyleSheet("color: #4CAF50; font-weight: 200; font-size: 24px;")
        self.icon_label.circle_color = QColor("#B4A647")
        self.icon_label.pixmap = QPixmap("assets/icons/clock.png").scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.icon_label.update()
        self.end_scan_button.setEnabled(True)
        self.return_button.setVisible(False)
        self.detections = []
        self.start_scan()

    def go_back(self):
        self.reset_page()
        self.router.navigate("field_selection")
