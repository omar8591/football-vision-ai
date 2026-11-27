# ⚽ Football Vision AI

A football object detection application powered by **YOLO11** and **Streamlit**.

Football Vision AI detects football players and footballs in uploaded images and videos. It provides visual detection results with bounding boxes, confidence scores, and a before-and-after video comparison.

## ✨ Features

- **Image Detection:** Upload an image and detect players and footballs.
- **Video Detection:** Process football videos frame by frame.
- **Before & After Comparison:** View the original video alongside the AI-annotated video.
- **Detection Statistics:** Display the number of detected players, footballs, and total detections.
- **Confidence Threshold:** Adjust the minimum confidence required for a detection.
- **Video Caching:** Reuse previously processed videos without running inference again.
- **Download Results:** Download annotated images and processed videos.
- **Custom UI:** Football-themed interface built with Streamlit.

## 🧠 Model

The application uses a fine-tuned YOLO11 model trained on a football object detection dataset.

| Class ID | Class |
|---|---|
| 0 | football |
| 1 | player |

The model uses an inference image size of **640 × 640**.

The trained model weights are stored in:

```text
best.pt
```

## 🛠️ Technologies

- Python
- YOLO11 — Ultralytics
- Streamlit
- OpenCV
- Pillow
- NumPy
- ImageIO-FFmpeg

## 📁 Project Structure

```text
YOLO_Football/
│
├── app.py
├── best.pt
├── requirements.txt
├── README.md
│
└── .video_cache/
    ├── original videos
    └── processed videos
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd YOLO_Football
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the trained model

Place your trained `best.pt` file in the project root directory:

```text
YOLO_Football/best.pt
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 📸 How to Use

### Image Detection

1. Select the **Image** input option.
2. Upload a football image.
3. Click **Analyze Image**.
4. View the original image and the detection result.
5. Download the annotated image if needed.

### Video Detection

1. Select the **Video** input option.
2. Upload a football video.
3. Click **Detect Players & Football**.
4. Wait for the model to process the video.
5. Compare the original and detected videos side by side.
6. Download the processed video.

## ⚡ Video Caching

Processed videos are stored locally in the `.video_cache` directory.

The application identifies cached results using:

- The uploaded video's content
- The model weights
- The confidence threshold

When the same video is uploaded again with the same model and confidence threshold, the application loads the cached result instead of processing the video again.

This significantly reduces processing time when revisiting previously analyzed videos.

## 📊 Detection Settings

| Setting | Value |
|---|---|
| Model | YOLO11 |
| Input types | Images and videos |
| Inference image size | 640 |
| Confidence threshold | Adjustable |
| Video processing | Frame-by-frame |
| Output format | Annotated image / MP4 video |
