import cv2
import requests

# 1. WhatsApp Configuration (Using Fonnte API)
# Get your token from fonnte.com
API_TOKEN = "YOUR_FONNTE_TOKEN_HERE"
TARGET_PHONE = "08123456789"

def send_wa_notification():
    url = "https://api.fonnte.com/send"
    payload = {
        'target': TARGET_PHONE,
        'message': 'Attendance Alert: Face has been detected successfully!',
    }
    headers = {
        'Authorization': API_TOKEN
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        print("WhatsApp Notification Sent!")
    except Exception as e:
        print(f"Failed to send WhatsApp: {e}")

# 2. Load Face Detection Model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. Start Camera
cap = cv2.VideoCapture(0)
print("System is running... Press 'ESC' to exit.")

# Flag to prevent sending multiple WA messages at once
notification_sent = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Face Detected', (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Logic to send WA only once when face is first seen
        if not notification_sent:
            send_wa_notification()
            notification_sent = True

    cv2.imshow('Face Detection Attendance System', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
