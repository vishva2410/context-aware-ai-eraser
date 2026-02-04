from core.detectors.face_detector import FaceDetector
from core.detectors.plate_detector import PlateDetector
from core.detectors.id_detector import IDDetector
from core.eraser import apply_anonymization
import os
import cv2

# Define base directory (root of the project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

face_detector = FaceDetector(os.path.join(BASE_DIR, "models/face_detect.pt"))
plate_detector = PlateDetector(os.path.join(BASE_DIR, "models/lp_detect.pt"))
id_detector = IDDetector(os.path.join(BASE_DIR, "models/id_detect.pt"))

def run_pipeline(input_path, context="public"):
    """
    Main entry point. Handles ONLY Images.
    """
    filename = os.path.basename(input_path)
    output_dir = os.path.join(BASE_DIR, "samples/output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Could not load image: {input_path}")

    # OPTIMIZATION: Resize if too large (Max 1280px)
    h, w = image.shape[:2]
    max_dim = 1280
    scale = 1.0
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Detect
    faces = face_detector.detect(image) 
    plates = plate_detector.detect(image)
    ids = id_detector.detect(image)

    detections = faces + plates + ids

    # Apply eraser
    output_image = apply_anonymization(
        image=image,
        detections=detections,
        context=context
    )

    # Save output
    output_filename = f"processed_{filename}"
    output_path = os.path.join(output_dir, output_filename)
    saved = cv2.imwrite(output_path, output_image)
    if not saved:
        raise RuntimeError(f"Failed to write output image to {output_path}")

    return {
        "detections": detections,
        "output_image": output_path,
        "output_filename": output_filename,
        "is_video": False
    }
