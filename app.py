
import streamlit as st
from ultralytics import YOLO
from PIL import Image
from pathlib import Path
from io import BytesIO
import streamlit.components.v1 as components
import cv2
import subprocess
import imageio_ffmpeg
import tempfile
import base64
import textwrap


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Football Vision AI",
    page_icon="⚽",
    layout="wide"
)


# ==========================================
# 2. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best.pt"

EXAMPLES_DIR = BASE_DIR / "examples"

DEMO_BEFORE = EXAMPLES_DIR / "before.mp4"
DEMO_AFTER = EXAMPLES_DIR / "after.mp4"


# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff8e7 0%, #eafaff 52%, #f6edff 100%);
    background-attachment: fixed;
    color: #17233c;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(120deg, #ffe45e 0%, #ff9a5a 48%, #ff6fae 100%);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.8);
    margin-bottom: 30px;
    box-shadow: 0 16px 40px rgba(223, 112, 93, 0.2);
}

.hero h1 {
    color: #17233c;
    font-size: 38px;
    margin-bottom: 8px;
}

.hero p {
    color: #293958;
    font-size: 17px;
    margin: 0;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #17233c;
    margin-top: 20px;
    margin-bottom: 12px;
}

div[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.82);
    border: 2px dashed #37b9ae;
    border-radius: 18px;
    padding: 15px;
    color: #17233c;
    box-shadow: 0 10px 24px rgba(31, 92, 113, 0.08);
}

.stButton > button {
    background: linear-gradient(100deg, #ff8a00, #ff4d8d);
    color: #ffffff;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    padding: 14px 20px;
    width: 100%;
    box-shadow: 0 8px 18px rgba(255, 100, 94, 0.24);
    transition: transform 160ms ease, box-shadow 160ms ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #ff9e22, #ff69a0);
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 12px 22px rgba(255, 100, 94, 0.3);
}

div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(100deg, #26b7a5, #35a7e8);
    color: #ffffff;
    border: none;
    border-radius: 14px;
    font-weight: 600;
    box-shadow: 0 8px 18px rgba(38, 183, 165, 0.2);
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. HTML HERO
# ==========================================

st.html("""
<div class="hero">
    <h1>
        ⚽ Football Vision AI
    </h1>

    <p>
        AI-powered football detection.
        Upload match footage or images and
        visualize detected players and footballs.
    </p>

</div>
""")


# ==========================================
# 5. LOAD YOLO MODEL
# ==========================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return YOLO(str(MODEL_PATH))


try:

    model = load_model()

except Exception as error:

    st.error(f"Failed to load model: {error}")
    st.stop()


# ==========================================
# 6. CUSTOM VIDEO PLAYER
# ==========================================

def display_video(video_bytes, title):

    encoded_video = base64.b64encode(
        video_bytes
    ).decode("utf-8")

    video_html = f"""
    <!DOCTYPE html>
    <html>
    <head>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .video-card {{
                background: linear-gradient(145deg, #fff8df, #ffe9f0);
                border: 1px solid #ffd1a8;
                border-radius: 20px;
                padding: 14px;
                overflow: hidden;
                max-width: 1100px;
                margin: 0 auto;
                box-shadow: 0 14px 32px rgba(58, 89, 128, 0.14);
            }}

            .video-title {{
                color: #253653;
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 12px;
            }}

            video {{
                display: block;
                width: auto;
                height: auto;
                max-width: 100%;
                max-height: min(70vh, 680px);
                object-fit: contain;
                border-radius: 14px;
                margin: 0 auto;
            }}

        </style>

    </head>

    <body>

        <div class="video-card">

            <div class="video-title">
                {title}
            </div>

            <video
                autoplay
                muted
                loop
                playsinline
                preload="metadata"
            >
                <source
                    src="data:video/mp4;base64,{encoded_video}"
                    type="video/mp4"
                >

                Your browser does not support HTML5 video.

            </video>

        </div>

    </body>
    </html>
    """

    components.html(
        video_html,
        height=800,
        scrolling=False
    )


def display_video_pair(
    before_bytes,
    after_bytes,
    before_title,
    after_title
):

    before_video = base64.b64encode(
        before_bytes
    ).decode("utf-8")
    after_video = base64.b64encode(
        after_bytes
    ).decode("utf-8")

    video_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .video-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 16px;
            }}

            .video-card {{
                min-width: 0;
                background: linear-gradient(145deg, #fff8df, #ffe9f0);
                border: 1px solid #ffd1a8;
                border-radius: 20px;
                padding: 14px;
                overflow: hidden;
                box-shadow: 0 14px 32px rgba(58, 89, 128, 0.14);
            }}

            .video-title {{
                color: #253653;
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 12px;
            }}

            .video-stage {{
                height: min(76vh, 680px);
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                border-radius: 14px;
                background: linear-gradient(135deg, #d9fbf3, #fff0c2 55%, #ffe1ec);
            }}

            video {{
                display: block;
                width: auto;
                height: auto;
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
                border-radius: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="video-grid">
            <div class="video-card">
                <div class="video-title">{before_title}</div>
                <div class="video-stage">
                    <video id="before-video" muted loop playsinline preload="auto">
                        <source src="data:video/mp4;base64,{before_video}" type="video/mp4">
                    </video>
                </div>
            </div>
            <div class="video-card">
                <div class="video-title">{after_title}</div>
                <div class="video-stage">
                    <video id="after-video" muted loop playsinline preload="auto">
                        <source src="data:video/mp4;base64,{after_video}" type="video/mp4">
                    </video>
                </div>
            </div>
        </div>
        <div id="playback-error" role="status"></div>
        <script>
            const videos = [
                document.getElementById("before-video"),
                document.getElementById("after-video")
            ];
            let started = false;

            function startTogether() {{
                if (started || videos.some(video => video.readyState < 3)) {{
                    return;
                }}

                started = true;
                Promise.all(videos.map(video => video.play())).catch(error => {{
                    document.getElementById("playback-error").textContent =
                        "Could not start synchronized video playback.";
                    console.error("Could not start synchronized video playback.", error);
                }});
            }}

            videos.forEach(video => {{
                video.addEventListener("canplay", startTogether);
            }});
            startTogether();
        </script>
    </body>
    </html>
    """

    components.html(
        video_html,
        height=760,
        scrolling=False
    )


# ==========================================
# 7. CONVERT DEMO VIDEO TO BROWSER MP4
# ==========================================

def encode_browser_video(input_path, output_path):

    """Create a compact, aspect-preserving preview for browser playback."""

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg_path,
        "-y",
        "-i", str(input_path),
        "-map", "0:v:0",
        "-vf",
        "scale=w='min(480,iw)':h='min(640,ih)':"
        "force_original_aspect_ratio=decrease,fps=24",
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "30",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path)
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr.decode(
                errors="replace"
            )[-2000:]
        )


@st.cache_data(
    show_spinner="Preparing your video preview...",
    max_entries=2
)
def convert_uploaded_video(video_bytes):

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)
        input_path = temp_dir / "uploaded_video"
        output_path = temp_dir / "browser_preview.mp4"

        input_path.write_bytes(video_bytes)
        encode_browser_video(input_path, output_path)

        return output_path.read_bytes()


@st.cache_data(
    show_spinner="Preparing the video showcase...",
    max_entries=2
)
def convert_demo_video(video_path, modified_at):

    """
    Converts a demonstration video into browser-friendly
    H.264 MP4 format.

    Streamlit caches the converted bytes using the source
    path and modification time as the cache key.
    """

    video_path = Path(video_path)

    if not video_path.exists():
        return None

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)

        output_path = temp_dir / "browser_video.mp4"

        encode_browser_video(
            video_path,
            output_path
        )

        return output_path.read_bytes()


# ==========================================
# 8. BEFORE & AFTER DEMONSTRATION
# ==========================================

st.markdown(
    '<div class="section-title">🎬 AI Detection Showcase</div>',
    unsafe_allow_html=True
)

st.caption(
    "Watch how Football Vision AI detects players "
    "and footballs in real match footage. Load the clips when you are ready "
    "to watch them."
)

show_showcase = st.toggle(
    "Load video showcase",
    value=False,
    key="load_video_showcase"
)

if show_showcase:

    if DEMO_BEFORE.exists() and DEMO_AFTER.exists():

        try:

            before_bytes = convert_demo_video(
                str(DEMO_BEFORE),
                DEMO_BEFORE.stat().st_mtime_ns
            )
            after_bytes = convert_demo_video(
                str(DEMO_AFTER),
                DEMO_AFTER.stat().st_mtime_ns
            )

            display_video_pair(
                before_bytes,
                after_bytes,
                "🎬 BEFORE — Original Video",
                "🤖 AFTER — AI Detection"
            )

        except Exception as error:

            st.error(
                f"Could not load comparison videos: {error}"
            )

    else:

        if not DEMO_BEFORE.exists():
            st.warning(f"Missing file: {DEMO_BEFORE}")

        if not DEMO_AFTER.exists():
            st.warning(f"Missing file: {DEMO_AFTER}")


st.divider()


# ==========================================
# 9. DETECTION SETTINGS
# ==========================================

with st.expander(
    "⚙️ Detection Settings",
    expanded=False
):

    confidence = st.slider(
        "Confidence threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.25,
        step=0.05
    )

    st.caption(
        "Image size is fixed at 640 to match your training configuration."
    )


# ==========================================
# 10. INPUT SELECTION
# ==========================================

st.markdown(
    '<div class="section-title">🚀 Try It Yourself</div>',
    unsafe_allow_html=True
)

input_type = st.radio(
    "Choose your input",
    ["🖼️ Image", "🎥 Video"],
    horizontal=True
)


# ==========================================
# 11. IMAGE DETECTION
# ==========================================

if input_type == "🖼️ Image":

    uploaded_image = st.file_uploader(
        "Upload a football image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    if uploaded_image:

        image = Image.open(
            uploaded_image
        ).convert("RGB")

        st.markdown("### Uploaded Image")

        st.image(
            image,
            use_container_width=True
        )

        if st.button("🚀 Analyze Image"):

            try:

                with st.spinner(
                    "Analyzing the image..."
                ):

                    result = model.predict(
                        source=image,
                        conf=confidence,
                        imgsz=640,
                        verbose=False
                    )[0]

                    annotated = result.plot()

                    annotated = cv2.cvtColor(
                        annotated,
                        cv2.COLOR_BGR2RGB
                    )

                # ----------------------------------
                # BEFORE AND AFTER
                # ----------------------------------

                st.markdown(
                    '<div class="section-title">Detection Results</div>',
                    unsafe_allow_html=True
                )

                original_col, result_col = st.columns(2)

                with original_col:

                    st.markdown("**🎬 Original Image**")

                    st.image(
                        image,
                        use_container_width=True
                    )

                with result_col:

                    st.markdown("**🤖 AI Detection**")

                    st.image(
                        annotated,
                        use_container_width=True
                    )

                # ----------------------------------
                # DETECTION SUMMARY
                # ----------------------------------

                boxes = result.boxes

                player_count = 0
                football_count = 0

                if boxes is not None:

                    for box in boxes:

                        class_id = int(box.cls[0])

                        class_name = model.names[class_id]

                        if class_name == "player":

                            player_count += 1

                        elif class_name == "football":

                            football_count += 1

                total_detections = (
                    len(boxes) if boxes is not None else 0
                )

                st.markdown("### Detection Summary")

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric(
                    "Players",
                    player_count
                )

                metric2.metric(
                    "Footballs",
                    football_count
                )

                metric3.metric(
                    "Total Detections",
                    total_detections
                )

                # ----------------------------------
                # DOWNLOAD IMAGE
                # ----------------------------------

                result_image = Image.fromarray(
                    annotated
                )

                image_buffer = BytesIO()

                result_image.save(
                    image_buffer,
                    format="PNG"
                )

                st.download_button(
                    "⬇️ Download Annotated Image",
                    data=image_buffer.getvalue(),
                    file_name="football_detection.png",
                    mime="image/png"
                )

            except Exception as error:

                st.error(
                    f"Image processing failed: {error}"
                )


# ==========================================
# 12. VIDEO PROCESSING
# ==========================================

def process_video(video_bytes, confidence):

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)

        input_path = temp_dir / "input_video.mp4"

        raw_output_path = temp_dir / "output_raw.mp4"

        output_path = temp_dir / "output.mp4"

        # ----------------------------------
        # SAVE INPUT TEMPORARILY
        # ----------------------------------

        input_path.write_bytes(video_bytes)

        cap = cv2.VideoCapture(
            str(input_path)
        )

        if not cap.isOpened():

            raise ValueError(
                "Could not open uploaded video."
            )

        fps = cap.get(cv2.CAP_PROP_FPS)

        width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if fps <= 0:
            fps = 30

        if width <= 0 or height <= 0:

            cap.release()

            raise ValueError(
                "Invalid video dimensions."
            )

        # ----------------------------------
        # CREATE VIDEO WRITER
        # ----------------------------------

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            str(raw_output_path),
            fourcc,
            fps,
            (width, height)
        )

        if not writer.isOpened():

            cap.release()

            raise RuntimeError(
                "Could not create output video."
            )

        progress = st.progress(0)

        status = st.empty()

        frame_count = 0

        try:

            # ----------------------------------
            # PROCESS FRAMES
            # ----------------------------------

            while True:

                success, frame = cap.read()

                if not success:
                    break

                result = model.predict(
                    source=frame,
                    conf=confidence,
                    imgsz=640,
                    verbose=False
                )[0]

                annotated_frame = result.plot()

                writer.write(
                    annotated_frame
                )

                frame_count += 1

                if total_frames > 0:

                    progress.progress(
                        min(
                            frame_count / total_frames,
                            1.0
                        )
                    )

                status.write(
                    f"Processing frame {frame_count} / {total_frames}"
                )

        finally:

            cap.release()
            writer.release()

        if frame_count == 0:

            raise ValueError(
                "No video frames were processed."
            )

        # ----------------------------------
        # CONVERT TO H.264
        # ----------------------------------

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        command = [
            ffmpeg_path,
            "-y",

            "-i", str(raw_output_path),
            "-i", str(input_path),

            "-map", "0:v:0",
            "-map", "1:a?",

            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",

            "-pix_fmt", "yuv420p",

            "-c:a", "aac",

            "-movflags", "+faststart",

            str(output_path)
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr.decode(
                    errors="replace"
                )[-3000:]
            )

        progress.empty()

        before_preview_path = temp_dir / "input_preview.mp4"
        after_preview_path = temp_dir / "detected_preview.mp4"

        encode_browser_video(
            input_path,
            before_preview_path
        )
        encode_browser_video(
            output_path,
            after_preview_path
        )

        status.success(
            "Video detection completed!"
        )

        return (
            output_path.read_bytes(),
            before_preview_path.read_bytes(),
            after_preview_path.read_bytes()
        )


# ==========================================
# 13. USER VIDEO UPLOAD
# ==========================================

if input_type == "🎥 Video":

    uploaded_video = st.file_uploader(
        "Upload your football video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_upload"
    )

    if uploaded_video:

        video_bytes = uploaded_video.getvalue()

        st.markdown("### Your Uploaded Video")

        show_uploaded_preview = st.toggle(
            "Preview uploaded video",
            value=False,
            key="preview_uploaded_video"
        )

        if show_uploaded_preview:
            display_video(
                convert_uploaded_video(video_bytes),
                "🎬 YOUR ORIGINAL VIDEO"
            )

        if st.button(
            "⚡ Detect Players & Football"
        ):

            try:

                with st.spinner(
                    "Running YOLO detection..."
                ):

                    (
                        detected_video,
                        original_preview,
                        detected_preview
                    ) = process_video(
                        video_bytes,
                        confidence
                    )

                st.markdown(
                    '<div class="section-title">Detection Results</div>',
                    unsafe_allow_html=True
                )

                display_video_pair(
                    original_preview,
                    detected_preview,
                    "🎬 BEFORE — Original Video",
                    "🤖 AFTER — AI Detection"
                )

                st.download_button(
                    "⬇️ Download Detected Video",
                    data=detected_video,
                    file_name="football_detection.mp4",
                    mime="video/mp4"
                )

                st.success(
                    "Video detection completed successfully!"
                )

            except Exception as error:

                st.error(
                    f"Video processing failed: {error}"
                )


# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.html("""
<div style="
    text-align: center;
    color: #34445f;
    padding: 26px 20px;
    background: linear-gradient(120deg, #fff1bd, #ffe2ed, #e1f8ff);
    border: 1px solid #ffffff;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(58, 89, 128, 0.1);
">

    <h4 style="color: #253653; margin-bottom: 8px;">
        ⚽ Football Vision AI
    </h4>

    <p style="margin: 0 0 8px;">Powered by YOLO Object Detection</p>

    <p style="
        margin: 0;
        color: #e85d82;
        font-weight: 800;
        font-size: 17px;
    ">
        Made by Omar Abdelaziz
    </p>

</div>
""")
