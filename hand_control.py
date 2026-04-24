import cv2
import mediapipe as mp
import serial
import time
import math
import numpy as np

# ================= SERIAL SETUP =================
PORT = "COM5"        #  CHANGE if needed
BAUD = 115200

ser = None
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # allow ESP32 reset
    print("ESP32 connected")
except:
    print("ESP32 not connected (camera-only mode)")

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ================= MATH FUNCTIONS =================
def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])

def length(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def angle(v1, v2):
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    l1, l2 = length(v1), length(v2)
    if l1*l2 == 0:
        return 0
    return math.degrees(math.acos(max(-1, min(1, dot/(l1*l2)))))

def finger_angle(a,b,c,d):
    return (angle(vec(a,b), vec(b,c)) + angle(vec(b,c), vec(c,d))) / 2

def map_servo(val):
    return int(np.interp(val, [10, 90], [0, 180]))

# ================= CAMERA =================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

finger_names = ["Thumb","Index","Middle","Ring","Pinky"]
last_send = time.time()

print("Press ESC or Q to quit")

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark
        h, w, _ = frame.shape

        def p(i):
            return (int(lm[i].x*w), int(lm[i].y*h))

        angles = [
            finger_angle(p(1),p(2),p(3),p(4)),     # Thumb
            finger_angle(p(5),p(6),p(7),p(8)),     # Index
            finger_angle(p(9),p(10),p(11),p(12)),  # Middle
            finger_angle(p(13),p(14),p(15),p(16)), # Ring
            finger_angle(p(17),p(18),p(19),p(20))  # Pinky
        ]

        servos = [map_servo(a) for a in angles]

        # show values on screen
        for i, val in enumerate(servos):
            cv2.putText(frame, f"{finger_names[i]}: {val}",
                        (10, 30 + i*30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # SEND TO ESP32 (20 Hz)
        if ser and time.time() - last_send > 0.05:
            data = ",".join(map(str, servos)) + "\n"
            ser.write(data.encode())
            last_send = time.time()

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand → ESP32 Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

    time.sleep(0.005)

# ================= CLEAN EXIT =================
cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
print("Program stopped")