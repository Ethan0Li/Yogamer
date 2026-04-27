# Yogamer 🧘 Yoga Tracker

## What it Does

Yogamer is a real-time yoga pose classification system that uses a webcam to detect and identify yoga poses as you perform them. It combines MediaPipe's pose estimation model — which tracks 33 body landmarks in real time — with a custom-trained multilayer perceptron (MLP) neural network to classify poses such as Child's Pose, Cobra Pose, Butterfly Pose, Downward Dog, Seated Forward Fold, and Ground Quad Stretch. The system normalizes all landmark coordinates relative to the hip midpoint and torso size, making classification robust to different body sizes, camera distances, and positions. If the model's confidence falls below a threshold, the system displays a "Resting" state rather than forcing a classification. Once a pose is held consistently, the session logs an active timer of that pose. Once the user stops, the time doing the pose is added to the pose catalog from which the user can observe their progress. The session allows the capture of all registered poses, meaning that the user may switch between poses, and Yogamer would track all of it for the user (only complication is making sure the user stays in view).

---

## Motivation

During a time of heightened fitness culture, push-up counters and gym tracking apps are everywhere. However, one important aspect of physical health is often overlooked — flexibility. Yoga improves joint mobility and range of motion, allowing people to move more freely and with less risk of injury. This way, the joints and ligaments are able to catch up to the bulging muscles you would want to build, and allow you to move the way you want. Built with extensibility in mind, new poses can be added simply by collecting additional training data and retraining the model. More functionalities that motivate yoga may be added later as well.

---

## Quick Start

**Data Collection** (yogamer_cv environment):
```bash
conda activate yogamer_cv
python data_capture.py
```
- Change `LABEL` at the top of `data_capture.py` to the pose name
- Press `s` to record 5 seconds of pose data
- Press `q` to quit

**Train the Model** (yogamer_train environment):
```bash
conda activate yogamer_train
# Open and run all cells in train_model.ipynb
```

**Real-Time Classification** (yogamer_cv environment):
```bash
conda activate yogamer_cv
python backend_app.py
```
- Press `q` to quit

---

## Video Links

- 🎥 Demo Video: _coming soon_
- 🔧 Technical Walkthrough: _coming soon_

---

## Evaluation

### Hyperparameter Tuning

There are many hyperparameters that could be adjusted, so I only tuned the ones I felt were most significant.

- **Epochs, batch size, & patience** — batch size of 32 was used as it is standard and outperformed other options in testing. Epochs and patience work in tandem — patience ensures the model stops early before overfitting, so most runs do not reach the full 100 epochs.
- **Train/validation/test split** — I utilized the standard from class: 70/30 train/test split with 10% of training held out for validation, producing a 63/7/30 train/validation/test split.
- **Architecture depth** — I utilize the standard 3-layer depth since the number of inputs does not increase (132).

The following table documents the results of tuning the remaining hyperparameters — learning rate, architecture width, and dropout rate:

| Config | Architecture | Learning Rate | Dropout | Val Accuracy | Test Accuracy | Applied Performance |
|---|---|---|---|---|---|---|
| Baseline | 128 → 64 → 32 | 0.001 | 0.3 | 1.000 | 1.000 | Poor |
| Wider | 256 → 128 → 64 | 0.001 | 0.3 | 1.000 | 1.000 | Decent |
| Lower LR | 256 → 128 → 64 | 0.0001 | 0.3 | 1.000 | 1.000 | Poor |
| Lower DR | 256 → 128 → 64 | 0.001 | 0.2 | 1.000 | 1.000 | Poor |

Notes about Applied Performance in `yogamer_app.py`:
- **Baseline** — Quick to classify random states as poses with 1.00 confidence (viewing of my face was classified as Butterfly Pose).
- **Wider** — Fixes issues of Baseline, but classifies transitioning into a pose as the pose itself. Not much of an issue currently due to the 4s timer, but would be problematic in the future when poses are similar.
- **Lower LR** — Reverts back to Baseline behavior. This is likely due to overfitting of the training data.
- **Lower DR** — Reverts back to Baseline. The lower dropout rate allows the model to establish specific pathways for classification.

---

### Training Curves

**Config 1: 128→64→32, Dropout=0.3, LR=1e-3**
![Config 1](training_curves/128-64-32_dropout0.3_lr1e-3.png)

**Config 2: 256→128→64, Dropout=0.2, LR=1e-4**
![Config 2](training_curves/256-128-64_dropout0.2_lr1e-4.png)

**Config 3: 256→128→64, Dropout=0.3, LR=1e-3**
![Config 3](training_curves/256-128-64_dropout0.3_lr1e-3.png)

**Config 4: 256→128→64, Dropout=0.3, LR=1e-4**
![Config 4](training_curves/256-128-64_dropout0.3_lr1e-4.png)

---

### Classification Report

More hyperparameter tuning could be done as I add more data and poses to the model. These behaviors were counter to expectations because of the way I approached MLP. The MLP only trained on the poses, not on noise or "resting state". Since resting state can mean too many different things, and I was afraid that noise similar to poses would significantly decrease the performance of the model. The solution I came up with was thresholding the confidence level produced by the model. This was experimentally confirmed to be around the 0.9–0.95 range currently, where confidence levels below would be considered "Resting". It should be noted that the 0.9–0.95 threshold was calibrated for the current set of poses and may require retuning as additional poses are added, since a more complex model with more classes will naturally produce lower peak confidence values.

This presents an issue where the model is well-trained to the different poses, but when encountering "noise", it is inclined to try and fit that noise to a pose — and if the model is overfitted, it would likely classify some noise with 100% certainty.

This presents an interesting finding where it would be more preferable that the model is slightly less accurate (instead of 100% for training, validation, and testing, perhaps around 99%), so that the classifications are correct but the confidence levels are not at 100%.

I do not foresee this as a major issue. Prior to this finding, the poses I picked were meant to be quite distinct from one another. As more data and poses are added to the model, the accuracy would naturally drop, and the hyperparameters could be tuned further.

---

## Individual Contributions

This is a solo project developed entirely by Ethan Liao. All components — data collection pipeline, preprocessing, model architecture, training, and real-time application — were designed and implemented individually.

---

## Project Structure

```
Yogamer/
├── data_capture.py              # Webcam data collection script
├── backend_app.py               # Application entry point
├── yogamer.py                   # Real-time pose classification app
├── train_model.ipynb            # Model training notebook
├── yoga_pose_classifier.tflite  # Trained model (TFLite format)
├── model_config.json            # Class labels and confidence threshold
├── environment_cv.yml           # Conda environment for capture and app
├── environment_train.yml        # Conda environment for training
├── training_curves/             # Hyperparameter tuning plots
├── SETUP.md                     # Installation instructions
└── ATTRIBUTION.md               # Sources and AI usage
```
