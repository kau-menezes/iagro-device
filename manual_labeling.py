import cv2
import json
from datetime import datetime
from geopy.geocoders import Nominatim
import threading

stop_event = threading.Event()

def analyze(model, stop_event=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    geolocator = Nominatim(user_agent="plant_disease_app")
    try:
        location = geolocator.geocode("me")
        coords = {
            "latitude": location.latitude if location else None,
            "longitude": location.longitude if location else None
        }
    except Exception as e:
        print(f"Error getting location: {e}")
        coords = {"latitude": None, "longitude": None}

    logs = []
    frame_id = 0
    label_map = {
        ord('q'): 'Late Blight',
        ord('w'): 'Light Blight',
        ord('e'): 'Healthy'
    }
    current_label = None

    while True:
        # Check stop_event at the top of the loop
        if stop_event is not None and stop_event.is_set():
            # Release and destroy immediately if stop_event is set
            cap.release()
            cv2.destroyAllWindows()
            break
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        display_frame = frame.copy()
        if current_label:
            cv2.putText(display_frame, f"Label: {current_label}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.imshow('Analysing...', display_frame)
        key = cv2.waitKey(10) & 0xFF

        # Exit on ESC or window close
        if key == 27 or cv2.getWindowProperty('Analysing...', cv2.WND_PROP_VISIBLE) < 1:
            break
        elif key in label_map:
            label = label_map[key]
            log_entry = {
                'datetime': datetime.now().isoformat(),
                'label': label,
                'latitude': coords['latitude'],
                'longitude': coords['longitude']
            }
            logs.append(log_entry)
            current_label = label
        frame_id += 1

    # Ensure resources are released and window is closed
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    # Save logs to JSON
    log_filename = f"manual_label_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, 'w') as f:
        json.dump(logs, f, indent=2)
    print(f"Logs saved to {log_filename}")

# Example usage:
# analyze(None)

# New function to stop the scan from outside
def stop_scan():
    stop_event.set()
