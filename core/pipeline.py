from core.detectors.face_detector import FaceDetector
from core.detectors.plate_detector import PlateDetector
from core.detectors.id_detector import IDDetector
from core.eraser import apply_anonymization
import os
import cv2

# Define base directory (root of the project)
# core/pipeline.py -> parent is core -> parent is root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

face_detector = FaceDetector(os.path.join(BASE_DIR, "models/face_detect.pt"))
plate_detector = PlateDetector(os.path.join(BASE_DIR, "models/lp_detect.pt"))
id_detector = IDDetector(os.path.join(BASE_DIR, "models/id_detect.pt"))

# Renamed to match API expectation
def run_pipeline(image_path, context="public"):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Run detectors
    faces = face_detector.detect(image_path) 
    plates = plate_detector.detect(image_path)
    ids = id_detector.detect(image_path)

    detections = faces + plates + ids

    # Apply eraser
    output_image = apply_anonymization(
        image=image,
        detections=detections,
        context=context
    )

    # Save output
    output_dir = os.path.join(BASE_DIR, "samples/output")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"processed_{filename}")
    cv2.imwrite(output_path, output_image)

    # Return relative path for frontend compatibility if needed, 
    # but frontend might expect consistent pathing.
    # The API returns this path. api/routes.py sends it to frontend.
    return {
        "detections": detections,
        "output_image": output_path
    }
