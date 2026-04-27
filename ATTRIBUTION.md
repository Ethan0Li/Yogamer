# Attribution

## Libraries and Frameworks

| Library | Version | Purpose | License |
|---|---|---|---|
| MediaPipe | 0.10.9 | Pose landmark detection | Apache 2.0 |
| OpenCV (`opencv-python`) | 4.x | Webcam capture and image processing | Apache 2.0 |
| TensorFlow / Keras | 2.13.0 | Neural network training | Apache 2.0 |
| AI Edge LiteRT (`ai-edge-litert`) | latest | TFLite model inference in app | Apache 2.0 |
| scikit-learn | 1.x | Label encoding, train/test split, evaluation metrics | BSD |
| NumPy | 1.x | Numerical operations and array handling | BSD |
| pandas | 2.x | CSV loading and data manipulation | BSD |
| matplotlib | 3.x | Training curve visualization | PSF |

---

## External References

- [MediaPipe Pose Landmarker Documentation](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker) — landmark index reference and pose detection API
- [TensorFlow Keras Documentation](https://www.tensorflow.org/api_docs/python/tf/keras) — model building and training API reference
- [scikit-learn Documentation](https://scikit-learn.org/stable/) — LabelEncoder and classification report reference
- [OpenCV Documentation](https://docs.opencv.org/) — video capture and image processing reference

---

## AI Assistance

This project was developed with significant assistance from **Claude (Anthropic)** via claude.ai and Cursor
Within each file, if the comment was AI-Generated, that module was AI generated. else, I was written by me. 

### What AI Was Used For

Claude assisted with the following throughout development:

- **Conceptual explanations** — explaining neural network concepts (MLP, softmax, dropout, overfitting, backpropagation, early stopping) and computer vision concepts (BGR vs RGB, landmark coordinates, normalization)
- **Code guidance** — refering me to proper documentation
- **Architecture decisions** — discussing model architecture choices, hyperparameter selection, and environment isolation strategy
- **Debugging** — diagnosing issues such as dependency conflicts (protobuf/TFLite), mislabeled CSV data, and model not learning
- **Data pipeline design** — normalization approach (hip-centered, torso-scaled), CSV structure, and the state machine pattern for data capture
- **Documentation** — The format and most of documentation in the .md files were AI generated with Claude. 

Cusor assisted with the following:

- **Front-end** — The entire Front-end was developed through Cursor, I only provided the template and general style of website (2 tabs with home and pose catalog)

- **Back-end** — backend_app.py was entirely AI-generated. I only provided the general flow (if pose for 4 seconds, start active_timer to add to total pose catalog)

### What Was Written Independently

- Near all final code was written and typed by Ethan Liao
- Data collection was performed independently
- Design decisions (pose selection, confidence threshold, project structure) were made independently
- All understanding of concepts was developed through the guided learning approach

### Nature of AI Interaction

Claude was used in a teaching capacity — explaining concepts before code, asking questions to test understanding, and pointing out bugs rather than fixing them outright. The interaction was structured as a learning conversation rather than code generation.

Cusor was used as the tool to quickly complete all non-ML aspects that put this project together in a clean display. 
---

## Dataset

All training data was collected by Ethan Liao using the `data_capture.py` script with a personal webcam. No external datasets were used.
