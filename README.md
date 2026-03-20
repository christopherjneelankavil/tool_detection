# 🔧 Tool Detection using YOLOv8

A real-time computer vision application that detects workshop tools using a custom-trained YOLOv8 model.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-brightgreen)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 Demo

> Real-time tool detection via webcam with bounding boxes and confidence scores.

---

## 🛠️ Detected Tools

| Tool | Class Name |
|------|------------|
| 🔨 Hammer | `Hammer` |
| 🔧 Wrench | `Wrench` |
| 🪛 Plier | `Plier` |
| 🔩 Socket | `Socket` |
| 🪚 Bit | `Bit` |

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| mAP@50 | 0.730 |
| mAP@50-95 | 0.421 |
| Inference Speed | ~15ms/frame |
| Best Epoch | 7 / 17 |

---

## 🗂️ Project Structure

```
tool_detector_app/
├── venv/                  # Virtual environment
├── tool_detector.py       # Main webcam detection script
├── best.pt                # Trained YOLOv8 model weights
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/christopherjneelankavil/tool_detection.git
cd tool_detection
```

### 2. Create & Activate Virtual Environment (Ubuntu)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install ultralytics opencv-python
```

### 4. Download Model Weights

Download `best.pt` from the [Releases](https://github.com/christopherjneelankavil/tool_detection/releases) section and place it in the project root.

---

## 🚀 Usage

### Run Webcam Detection (CPU)

```bash
python tool_detector.py
```

### Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the application |
| `S` | Save screenshot |

---

## 🧠 Model Details

- **Architecture:** YOLOv8n (Nano)
- **Dataset:** [Tools Dataset – Roboflow](https://universe.roboflow.com/hammer-dqemv/tools-vl4du)
- **Training Images:** 2,507
- **Validation Images:** 177
- **Epochs:** 17 (early stopping at patience=10)
- **Image Size:** 640×640
- **Framework:** Ultralytics YOLOv8

---

## 📦 Export Formats Available

| Format | File | Use Case |
|--------|------|----------|
| PyTorch | `best.pt` | PC / Laptop inference |
| ONNX | `best.onnx` | Cross-platform deployment |
| TFLite | `best_float32.tflite` | Mobile / Edge devices |

---

## 📁 Dataset

- **Source:** [Roboflow Universe – Tools Dataset](https://universe.roboflow.com/hammer-dqemv/tools-vl4du)
- **License:** CC BY 4.0
- **Total Images:** 2,787
- **Classes:** 5 (Hammer, Wrench, Plier, Socket, Bit)

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| Webcam not opening | Change `VideoCapture(0)` → `VideoCapture(1)` |
| `best.pt` not found | Ensure it's in the same folder as the script |
| Low FPS on CPU | `imgsz=320` is already applied for speed |
| No detections | Lower confidence: `conf=0.25` |

---

## 🗺️ Roadmap

- [x] Train YOLOv8 on custom tool dataset
- [x] Real-time webcam detection (CPU)
- [x] Export to ONNX and TFLite
- [ ] Android mobile app
- [ ] Improve Hammer detection confidence
- [ ] Retrain with YOLOv8s for better accuracy

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Roboflow Universe](https://universe.roboflow.com)
- Dataset by [hammer @ Roboflow](https://universe.roboflow.com/hammer-dqemv)
