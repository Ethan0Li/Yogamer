# Setup Instructions

## Prerequisites

- [Anaconda or Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- A webcam
- Windows 10/11 (64-bit)
- Git

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/Ethan0Li/Yogamer.git
cd Yogamer
```

---

## Step 2 — Create the CV Environment

This environment is used for data collection and real-time classification.

```bash
conda env create -f environment_cv.yml
conda activate yogamer_cv
```

Verify the installation:
```bash
python -c "import cv2; import mediapipe as mp; print('CV environment ready')"
```

---

## Step 3 — Create the Training Environment (Optional)

This environment is used for training the neural network.

```bash
conda env create -f environment_train.yml
conda activate yogamer_train
```

Verify the installation:
```bash
python -c "import tensorflow as tf; import sklearn; print('Train environment ready')"
```

---

## Step 4 — Collect Training Data (Optional)

If you want to collect your own training data rather than using the provided dataset:

```bash
conda activate yogamer_cv
```

Edit `data_capture.py` and change the `LABEL` variable to the pose name:
```python
LABEL = "Child's Pose"  # change this for each pose
```

Run the script:
```bash
python data_capture.py
```

- Get into the pose
- Press `s` to record 15 seconds of landmark data
- Press `q` when done
- Repeat for each pose, changing `LABEL` each time

---

## Step 5 — Train the Model (Optional)

If you collected new data or want to retrain:

```bash
conda activate yogamer_train
```

Open `train_model.ipynb` in VS Code and run all cells from top to bottom (Kernel → Restart & Run All).

The notebook will:
1. Load and normalize the landmark data
2. Train the MLP classifier
3. Save `yoga_pose_classifier.tflite` and `model_config.json`

---

## Step 6 — Run the Real-Time Classifier

```bash
conda activate yogamer_cv
python yogamer_app.py
```

- Stand in front of your webcam at 2–4 meters distance
- Angle yourself such that the webcam captures your sideview (direction shouldn't matter)
- Make sure to place the webcam to capture all parts of your body
- Perform any of the supported poses
- Press `q` to quit

---

## Step 7 — Run the Application

```bash
conda activate yogamer_cv
python backend_app.py
```

### Home

The start session button launches the pose classification session via `yogamer_app.py`. Note that you may need to click more than once and wait, as the application has high latency (work in progress).

- Stand in front of your webcam at 2–4 meters distance
- Angle yourself such that the webcam captures your side view (direction does not matter)
- Make sure the webcam captures all parts of your body
- Perform any of the supported poses
- Press `q` to quit

---

### Catalog

A simple catalog that records the total time spent in each pose across all yoga sessions.

---

## Troubleshooting

**Webcam not detected:**
```python
cap = cv2.VideoCapture(1)  # try 1 instead of 0
```

**Poor detection quality:**
- Ensure good lighting facing toward you
- Wear less loose clothing
- Stand 2–4 meters from the camera
- Use a plain background if possible

**Module not found errors:**
- Make sure the correct conda environment is activated
- Run `conda activate yogamer_capture` before running `.py` files
