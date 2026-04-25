# CS372 Final Project: Yogamer (In-Progress)

## Project Overview
The goal of this project is to deepen my understanding of ML while also addressing an issue. 
Motivation: the focus of today is too much focused on attaining the perfect physique and building muscle. While they are worthwhile investments, the other aspects of physcail health may be left behind. To advocate for the improvement of flexibility and mobility, this application is meant to promote and yoga. this is important because blah blah blah

The workflow is as follows: I plan to use MediaPipe to identify body positioning, and the body positioning is fed into a Multiclass-classifcation NN that classifies the poses into the corresponding Yoga pose all in real time. This information is displayed to you and the time is tracked for you which you can track in the home screen. 

## Environments
- `yogamer_capture` — data collection (MediaPipe + OpenCV)
- `yogamer_train` — model training (TensorFlow + scikit-learn)

## Setup
# Capture environment
conda env create -f environment_capture.yml
conda activate yogamer_capture

# Train environment  
conda env create -f environment_train.yml
conda activate yogamer_train

## Project Structure
data_capture.py        # collect training data
yoga_pose.csv          # landmark dataset
train_model.ipynb      # training notebook
yoga_pose_classifier.keras  # saved model
model_config.json      # class labels and threshold
yogamer.py             # real-time application (coming soon)

## Poses
Current classes: Child's Pose, Cobra Pose, Seated Forward Fold