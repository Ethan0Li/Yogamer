# Yogamer

Yogamer is a real-time yoga pose tracking app built with MediaPipe + a custom MLP classifier.
It includes:

- a live pose session (`yogamer_app.py`) using webcam + TFLite inference
- a Flask web app (`backend_app.py`) with:
  - Home page with **Start Session**
  - separate **Pose Catalog** page with total tracked time per pose

## Features

- Real-time pose classification from webcam landmarks
- Pose hold gating (default: `4` seconds) before timing starts
- Per-pose cumulative time tracking persisted to `pose_stats.json`
- Web UI with separate Home and Catalog pages
- Catalog cards with stock-style pose images

## Tech Stack

- Python
- OpenCV
- MediaPipe
- TensorFlow / TFLite (`ai-edge-litert` runtime)
- Flask
- HTML/CSS/JavaScript

## Project Files

- `backend_app.py` - Flask backend and API routes
- `yogamer_app.py` - live webcam session + pose timing logic
- `templates/` - HTML pages (`index.html`, `catalog.html`)
- `static/` - frontend assets (`styles.css`, `home.js`, `catalog.js`)
- `mlp.ipynb` - model training notebook
- `model_config.json` - label map for inference
- `yoga_pose_classifier.tflite` - deployed model
- `yoga_pose_classifier.keras` - Keras model artifact
- `data_capture.py` - dataset capture script
- `yoga_pose.csv` - landmark dataset
- `pose_stats.json` - persisted pose time totals

## Environment Setup (Conda)

This project currently uses Conda environments.

### 1) Create and activate runtime environment

```bash
conda env create -f environment_cv.yml
conda activate yogamer_cv
```

If your runtime env name differs, update the backend runtime selection:

```bash
set YOGAMER_CONDA_ENV=yogamer_cv
```

### 2) (Optional) Training environment

Use your training env for `mlp.ipynb` and model export.

## Run the Web App

From the project root:

```bash
conda activate yogamer_cv
python backend_app.py
```

Then open:

- `http://127.0.0.1:5000/` (Home)
- `http://127.0.0.1:5000/catalog` (Pose Catalog)

Press **Start Session** on Home to launch the webcam session window.

## Runtime Config

- `POSE_HOLD_SECONDS` (default `4.0`): seconds pose must be stable before timing begins
- `YOGAMER_CONDA_ENV` (default `yogamer_cv`): conda env used to launch `yogamer_app.py`
- `YOGAMER_RUNTIME_PYTHON` (optional): explicit Python path for runtime process

## Current Pose Classes

- Butterfly Pose
- Child's Pose
- Cobra Pose
- Downward Dog Pose
- Ground Quad Stretch
- Seated Forward Fold