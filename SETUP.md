Setup Instructions
Prerequisites
Anaconda or Miniconda
A webcam
Windows 10/11 (64-bit)
Git
---
Step 1 — Clone the Repository
```bash
git clone https://github.com/Ethan0Li/Yogamer.git
cd Yogamer
```
---
Step 2 — Create the Computer Vision Environment
This environment is used for data collection and real-time classification.
```bash
conda env create -f environment_cv.yml
conda activate yogamer_cv
```
Verify the installation:
```bash
python -c "import cv2; import mediapipe as mp; print('Capture environment ready')"
```
---
Step 3 — Create the Training Environment
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
Step 4 — Collect Training Data (Optional)
If you want to collect your own training data to train the model over using the current model:
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
Get into the pose
Press `s` to record 5 seconds of landmark data
Press `q` when done
Repeat for each pose, changing `LABEL` each time
---
Step 5 — Train the Model (Optional)
If you collected new data or want to retrain:
```bash
conda activate yogamer_train
```
Open `train_model.ipynb` in VS Code and run all cells from top to bottom (Kernel → Restart & Run All).
The notebook will:
Load and normalize the landmark data
Train the MLP classifier
Save `yoga_pose_classifier.tflite` and `model_config.json`
---
Step 6 — Run the Real-Time App
```bash
conda activate yogamer_cv
python yogamer.py
```
Stand in front of your webcam at 2–4 meters distance
Perform any of the supported poses
Press `q` to quit
---
Supported Poses
Child's Pose
Cobra Pose
Butterfly Pose
Downward Dog Pose
Seated Forward Fold
Ground Quad Stretch
(More could be added)
---
Troubleshooting
Webcam not detected:
```python
cap = cv2.VideoCapture(1)  # try 1 instead of 0
```
Poor detection quality:
Ensure good lighting facing toward you
Try not to wear baggy clothes
Stand 2–4 meters from the camera
Use a plain background if possible

Module not found errors:
Make sure the correct conda environment is activated
Run `conda activate yogamer_capture` before running `.py` files