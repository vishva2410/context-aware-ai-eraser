from core.detectors.face_detector import FaceDetector
from core.detectors.plate_detector import PlateDetector
from core.detectors.id_detector import IDDetector
from core.eraser import apply_anonymization
import cv2
import os

face_detector = FaceDetector("models/face_detect.pt")
plate_detector = PlateDetector("models/lp_detect.pt")
id_detector = IDDetector("models/id_detect.pt")

def run_pipeline(image_path, context="public"):
    # Load image once
    if not os.path.exists(image_path):
        raise ValueError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Pass loaded image to detectors
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

    output_dir = "samples/output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    # Avoid overwriting original if input is in same dir, but here we save to output dir
    output_path = os.path.join(output_dir, f"processed_{filename}")
    cv2.imwrite(output_path, output_image)

    return {
        "detections": detections,
        "output_image": output_path
    }
