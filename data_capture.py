import cv2
import mediapipe as mp
import csv
import os
import time

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

# Define the label for the current pose
LABEL = "Child's Pose"
# where the data goes
CSV_FILE = "yoga_pose.csv"

# create (if not exist) and open csv file create format
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ['label']
        for i in range(33):
            header += [f'x{i}', f'y{i}', f'z{i}', f'v{i}']
        writer.writerow(header)

# Initialize Camera (default webcam) and recording parameters
cap = cv2.VideoCapture(0)
recording_time = 15 
capture_state = False

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
        
        # Draw Landmarks
        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            landmarks = results.pose_landmarks.landmark
            
            # if true, capture data and save to csv
            if capture_state:
                row = [LABEL]
                for lm in landmarks:
                    row += [lm.x, lm.y, lm.z, lm.visibility]
                with open(CSV_FILE, mode='a', newline='') as f:
                    csv.writer(f).writerow(row)
        # display recording status of capturing data and tracking countdown timer           
        if capture_state:
            time_remaining = recording_time - (time.time() - start_time)
            if time_remaining > 0:
                cv2.putText(frame, f'Recording... {int(time_remaining)}s left', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                capture_state = False
                print(f"Done capture for {LABEL}")
            # Print left and right hip coordinates
            # left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            # right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            # print(f"Left Hip: x={left_hip.x}, y={left_hip.y}, z={left_hip.z}")
            # print(f"Right Hip: x={right_hip.x}, y={right_hip.y}, z={right_hip.z}")
        else:    
            cv2.putText(frame, f'Get into Pose: {LABEL}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        cv2.imshow(f'Session for {LABEL}', frame)
        
        key = cv2.waitKey(5) & 0xFF
        
        # Start capturing data when 's' is pressed, stop after recording_time seconds, 'q' to quit
        if  key == ord('s') and not capture_state:
            capture_state = True
            start_time = time.time()
            print("Recording started...")
        elif key == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()