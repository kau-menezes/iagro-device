import cv2
import json
import os
from datetime import datetime

def analyze(model):
    cap = cv2.VideoCapture(0)
    logs = []
    frame_id = 0
    label_map = {
        ord('q'): 'Late Blight',
        ord('w'): 'Light Blight',
        ord('e'): 'Healthy'
    }
    current_label = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        display_frame = frame.copy()
        if current_label:
            cv2.putText(display_frame, f"Label: {current_label}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.imshow('Manual Labeling - Q: Late Blight | W: Light Blight | E: Healthy | ESC: Exit', display_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC to exit
            break
        elif key in label_map:
            label = label_map[key]
            log_entry = {
                'frame_id': frame_id,
                'datetime': datetime.now().isoformat(),
                'label': label
            }
            logs.append(log_entry)
            current_label = label
        frame_id += 1
    cap.release()
    cv2.destroyAllWindows()
    # Save logs to JSON
    log_filename = f"manual_label_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, 'w') as f:
        json.dump(logs, f, indent=2)
    print(f"Logs saved to {log_filename}")

# Example usage:
# analyze(None)
