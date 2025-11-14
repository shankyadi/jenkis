import cv2
import mediapipe as mp
import numpy as np


def objective_function(x):
    return -x**2 + 10*x  # Max at x=5


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)

x = np.random.randint(0, 10)  # Start point
best_x = x
best_y = objective_function(x)

print(f"Starting at x={x}, f(x)={best_y}")

def count_fingers(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)

            if finger_count == 1:
                x = max(0, x - 1)
            elif finger_count == 2:
                x = min(10, x + 1)

            y = objective_function(x)
            if y > best_y:
                best_x, best_y = x, y
                print(f"New best: x={best_x}, f(x)={best_y}")

    cv2.putText(frame, f"x={x}  f(x)={objective_function(x):.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Hill Climbing with Hand Gesture", frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
