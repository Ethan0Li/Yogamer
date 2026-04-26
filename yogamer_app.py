import cv2
import mediapipe as mp
import time
import numpy as np
from ai_edge_litert.interpreter import Interpreter
import json

# preprocessing function
def preProcess_rgb(frame):
    frame = cv2.resize(frame, (640, 480))
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    yuv[:,:,0] = cv2.equalizeHist(yuv[:, :, 0])
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, rgb
    
 
# Initialize tools (pose estimation and drawing utilities)
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# load TFlite model for pose classification
interpreter = Interpreter(model_path="yoga_pose_classifier.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# load label map
with open('model_config.json', 'r') as f:
    config = json.load(f)
classes = config['label_encoder']

# Initialize Camera (default webcam) and recording parameters
cap = cv2.VideoCapture(0)


# Process frames -> detect pose -> draw Landmarks
with mp_pose.Pose(
    model_complexity=2,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
    while cap.isOpened():

        success_ret, frame = cap.read()
        if not success_ret:
            break
        
        frame, rgb = preProcess_rgb(frame)
        
        # Input into pose estimation model
        results = pose.process(rgb)
        
        # Establish landmarks, draw time, and feed into model for classification
        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            landmarks = results.pose_landmarks.landmark

            normalized_landmarks = []
            for i in range(33):
                normalized_landmarks.append(landmarks[i].x)
                normalized_landmarks.append(landmarks[i].y)
                normalized_landmarks.append(landmarks[i].z)
                normalized_landmarks.append(landmarks[i].visibility)
                
            # feed into model
            input_data = np.array([normalized_landmarks], dtype=np.float32)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            # display predicted pose
            max_conf = np.max(output_data)
            if max_conf > 0.9:
                predicted_label = classes[np.argmax(output_data)]
            else:
                predicted_label = "Resting"
            
            cv2.putText(frame, f'Pose: {predicted_label}', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (100, 200, 100), 2)
        cv2.imshow(f'Live Yoga Session', frame)
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()