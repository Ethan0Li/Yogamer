Attribution
Libraries and Frameworks
Library	Version	Purpose	License
MediaPipe	0.10.9	Pose landmark detection	Apache 2.0
OpenCV (`opencv-python`)	4.x	Webcam capture and image processing	Apache 2.0
TensorFlow / Keras	2.13.0	Neural network training	Apache 2.0
AI Edge LiteRT (`ai-edge-litert`)	latest	TFLite model inference in app	Apache 2.0
scikit-learn	1.x	Label encoding, train/test split, evaluation metrics	BSD
NumPy	1.x	Numerical operations and array handling	BSD
pandas	2.x	CSV loading and data manipulation	BSD
matplotlib	3.x	Training curve visualization	PSF
---
External References
MediaPipe Pose Landmarker Documentation — landmark index reference and pose detection API
TensorFlow Keras Documentation — model building and training API reference
scikit-learn Documentation — LabelEncoder and classification report reference
OpenCV Documentation — video capture and image processing reference
---
AI Assistance
This project was developed with significant assistance from Claude (Anthropic) via claude.ai and Cursor
What AI Was Used For
Claude assisted with the following throughout development:
Conceptual explanations — explaining neural network concepts (MLP, softmax, dropout, overfitting, backpropagation, early stopping) and computer vision concepts (BGR vs RGB, landmark coordinates, normalization)
Code guidance — Directing me to the proper documentation for Mediapipe and tensorflow
Architecture decisions — discussing model architecture choices, hyperparameter selection, and environment isolation strategy
Debugging — diagnosing issues such as dependency conflicts (protobuf/TFLite), mislabeled CSV data, and model not learning
Refining Data pipeline design — While I came up with hip-centering for position, Claude recommended torso-size for different body shapes.
Claude was also used to generate most of the documentation (Readme, attribution, etc).
Cursor was used to generate the front-end and back-end application of the models in its entireity. I just provided the workflow logic for the poses (if hold for 4 seconds, start active timer and add to pose catalog for total time per pose). 
What Was Written Independently
Near all final ML code was written and typed by Ethan Li
Data collection was performed independently
Design decisions (pose selection, confidence threshold, project structure) were made independently
All understanding of concepts was developed through the guided learning approach
Nature of AI Interaction
Claude was used in a teaching capacity — explaining concepts before code, asking questions to test understanding, and pointing out bugs rather than fixing them outright. The interaction was structured as a learning conversation rather than code generation.
---
Dataset
All training data was collected by Ethan Liao using the `data_capture.py` script with a personal webcam. No external datasets were used.