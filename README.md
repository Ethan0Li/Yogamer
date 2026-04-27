Yogamer 🧘
What it Does
Yogamer is a real-time yoga pose classification system that uses a webcam to detect and identify yoga poses as you perform them. It combines MediaPipe's pose estimation model — which tracks 33 body landmarks in real time — with a custom-trained multilayer perceptron (MLP) neural network to classify poses such as Child's Pose, Cobra Pose, Butterfly Pose, Downward Dog, Seated Forward Fold, and Ground Quad Stretch. The system normalizes all landmark coordinates relative to the hip midpoint and torso size, making classification robust to different body sizes, camera distances, and positions. If the model's confidence falls below a threshold, the system displays a "Resting" state rather than forcing a classification.
---
Quick Start
Data Collection (yogamer_cv environment):
```bash
conda activate yogamer_cv
python data_capture.py
```
Change `LABEL` at the top of `data_capture.py` to the pose name
Press `s` to record 5 seconds of pose data
Press `q` to quit
Train the Model (yogamer_train environment):
```bash
conda activate yogamer_train
# Open and run all cells in train_model.ipynb
```
Real-Time Classification (yogamer_capture environment):
```bash
conda activate yogamer_capture
python yogamer.py
```
Press `q` to quit
---
Video Links
🎥 Demo Video: coming soon
🔧 Technical Walkthrough: coming soon
---
Evaluation
Model Performance
The final model was trained on approximately 5,000 samples across 6 yoga pose classes with 70/30 train/test split. Landmark coordinates were normalized relative to hip midpoint and torso size before training.
Hyperparameter Tuning
Config	Architecture	Learning Rate	Dropout	Val Accuracy
Baseline	128 → 64 → 32	0.001	0.3	TBD
Deeper	256 → 128 → 64 → 32	0.001	0.3	TBD
Lower LR	128 → 64 → 32	0.0001	0.3	TBD
Training Curves
![Training Curves](training_curves.png)
Classification Report
To be updated after final training run.
---
Individual Contributions
This is a solo project developed entirely by Ethan Liao. All components — data collection pipeline, preprocessing, model architecture, training, and real-time application — were designed and implemented individually.
---
Project Structure
```
Yogamer/
├── data_capture.py              # Webcam data collection script
├── yogamer.py                   # Real-time pose classification app
├── train_model.ipynb            # Model training notebook
├── yoga_pose_classifier.tflite  # Trained model (TFLite format)
├── model_config.json            # Class labels and confidence threshold
├── environment_capture.yml      # Conda environment for data capture
├── environment_train.yml        # Conda environment for training
├── SETUP.md                     # Installation instructions
└── ATTRIBUTION.md               # Sources and AI usage
```