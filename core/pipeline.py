import os
from core.detectors.face_detector import FaceDetector
from core.eraser import blur_faces

face_detector = FaceDetector(conf=0.15)

def run_pipeline(image_path):
    detections = face_detector.detect(image_path)

    output_dir = "samples/output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir, "blurred_" + os.path.basename(image_path)
    )

    blur_faces(image_path, detections, output_path)

    return {
        "detections": detections,
        "output_image": output_path
    }
