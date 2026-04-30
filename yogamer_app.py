import json
import os
import time
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from ai_edge_litert.interpreter import Interpreter


RESTING_LABEL = "Resting"
CONFIDENCE_THRESHOLD = 0.95
POSE_HOLD_SECONDS = float(os.getenv("POSE_HOLD_SECONDS", "4.0"))
STATS_PATH = Path(os.getenv("POSE_STATS_FILE", "pose_stats.json"))


# Proccesses the frame for better pose estimation
def preprocess_rgb(frame):
    frame = cv2.resize(frame, (640, 480))
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    frame = cv2.convertScaleAbs(frame, alpha=1.35, beta=0)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, rgb

# Normalizes landmarks
def normalize_landmarks(landmarks):
    hip_mid_x = (landmarks[23].x + landmarks[24].x) / 2
    hip_mid_y = (landmarks[23].y + landmarks[24].y) / 2
    hip_mid_z = (landmarks[23].z + landmarks[24].z) / 2

    shoulder_mid_x = (landmarks[11].x + landmarks[12].x) / 2
    shoulder_mid_y = (landmarks[11].y + landmarks[12].y) / 2
    torso_size = np.sqrt((shoulder_mid_x - hip_mid_x) ** 2 + (shoulder_mid_y - hip_mid_y) ** 2)
    torso_size = max(torso_size, 1e-6)

    normalized = []
    for lm in landmarks:
        normalized.extend(
            [
                (lm.x - hip_mid_x) / torso_size,
                (lm.y - hip_mid_y) / torso_size,
                (lm.z - hip_mid_z) / torso_size,
                lm.visibility,
            ]
        )
    return normalized

# AI-GENERATED COMMENT: Added for web catalog persistence.
def load_pose_stats(classes):
    if STATS_PATH.exists():
        with STATS_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = {}
    for pose_name in classes:
        data.setdefault(pose_name, 0.0)
    return data

# AI-GENERATED COMMENT: Added for web catalog persistence.
def save_pose_stats(stats):
    with STATS_PATH.open("w", encoding="utf-8") as file:
        json.dump(stats, file, indent=2)

# AI-GENERATED COMMENT: Added to improve live UI formatting.
def draw_overlay(frame, predicted_label, max_conf, tracked_pose, hold_progress, active_duration):
    # AI-GENERATED COMMENT:
    # The panel UI below replaces plain text with a card-style HUD for readability.
    panel = frame.copy()
    cv2.rectangle(panel, (20, 20), (540, 210), (20, 20, 20), -1)
    cv2.addWeighted(panel, 0.65, frame, 0.35, 0, frame)
    cv2.rectangle(frame, (20, 20), (540, 210), (90, 210, 255), 2)

    cv2.putText(frame, "Yogamer Live Session", (35, 55), cv2.FONT_HERSHEY_DUPLEX, 0.9, (240, 240, 240), 2)
    cv2.putText(
        frame,
        f"Detected: {predicted_label}",
        (35, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (220, 250, 220),
        2,
    )
    cv2.putText(
        frame,
        f"Confidence: {max_conf:.2f}",
        (35, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (220, 220, 255),
        2,
    )

    tracking_text = f"Tracking: {tracked_pose}" if tracked_pose else "Tracking: waiting for stable pose"
    cv2.putText(frame, tracking_text, (35, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 235, 190), 2)
    cv2.putText(
        frame,
        f"Active timer: {active_duration:.1f}s",
        (35, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (180, 255, 180),
        2,
    )

    bar_x, bar_y, bar_w, bar_h = 35, 195, 480, 10
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (100, 100, 100), 1)
    fill = int(max(0.0, min(1.0, hold_progress)) * bar_w)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill, bar_y + bar_h), (90, 210, 255), -1)

# AI-GENERATED COMMENT: Added to safely finalize active pose timing.
def flush_active_pose(active_pose, active_start_time, pose_stats):
    if active_pose is None or active_start_time is None:
        return
    elapsed = max(0.0, time.time() - active_start_time)
    pose_stats[active_pose] = pose_stats.get(active_pose, 0.0) + elapsed
    save_pose_stats(pose_stats)

# Main session loop with pose estimation, timing, and stats tracking
def main():
    # Initialize tools (pose estimation and drawing utilities)
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils

    # load TFlite model for pose classification
    interpreter = Interpreter(model_path="yoga_pose_classifier.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # load label map
    with open("model_config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    classes = config["label_encoder"]
    pose_stats = load_pose_stats(classes)
    save_pose_stats(pose_stats)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        # AI-GENERATED COMMENT:
        # Fail loudly so backend/UI can report why the session exited immediately.
        raise RuntimeError("Camera open failed. Ensure webcam is connected and not in use by another app.")
    candidate_pose = None
    candidate_start_time = None
    active_pose = None
    active_start_time = None

    with mp_pose.Pose(
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as pose:
        # Process frames -> detect pose -> draw landmarks
        while cap.isOpened():
            success_ret, frame = cap.read()
            if not success_ret:
                break

            frame, rgb = preprocess_rgb(frame)
            # Input into pose estimation model
            results = pose.process(rgb)
            predicted_label = RESTING_LABEL
            max_conf = 0.0

            if results.pose_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark
                # normalize all landmarks before input into model
                normalized_landmarks = normalize_landmarks(landmarks)

                # feed into model
                input_data = np.array([normalized_landmarks], dtype=np.float32)
                interpreter.set_tensor(input_details[0]["index"], input_data)
                interpreter.invoke()
                output_data = interpreter.get_tensor(output_details[0]["index"])

                # determine predicted pose
                max_conf = float(np.max(output_data))
                if max_conf > CONFIDENCE_THRESHOLD:
                    predicted_label = classes[int(np.argmax(output_data))]

            #AI Generated
            #for better UX, require pose to be held for a short duration before counting as active pose
            now = time.time()
            pose_changed = predicted_label != candidate_pose
            if pose_changed:
                candidate_pose = predicted_label
                candidate_start_time = now

            hold_elapsed = 0.0 if candidate_start_time is None else now - candidate_start_time
            hold_progress = hold_elapsed / POSE_HOLD_SECONDS if POSE_HOLD_SECONDS > 0 else 1.0

            stable_pose = candidate_pose if (candidate_pose != RESTING_LABEL and hold_elapsed >= POSE_HOLD_SECONDS) else None
            if stable_pose != active_pose:
                flush_active_pose(active_pose, active_start_time, pose_stats)
                active_pose = stable_pose
                active_start_time = now if active_pose else None

            active_duration = 0.0 if active_start_time is None else max(0.0, now - active_start_time)
            draw_overlay(frame, predicted_label, max_conf, active_pose, hold_progress, active_duration)
            cv2.imshow("Yogamer Session (Press Q to quit)", frame)

            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

    flush_active_pose(active_pose, active_start_time, pose_stats)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()