from core.detectors.face_detector import FaceDetector
from core.detectors.plate_detector import PlateDetector
from core.detectors.id_detector import IDDetector
from core.eraser import apply_anonymization

face_detector = FaceDetector("models/face_detect.pt")
plate_detector = PlateDetector("models/lp_detect.pt")
id_detector = IDDetector("models/id_detect.pt")

# Renamed to match API expectation
def run_pipeline(image_path, context="public"):
    # Load image
    import cv2
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

    # Encode output image to base64 or save it? 
    # The API expects "output_image" in the result. 
    # Let's adjust to return what the API needs. 
    # The API in routes.py checks result["output_image"].
    # Usually we save it to a temp path or encode it. 
    # For now let's just return the path to a saved file or the array if the API handles it?
    # routes.py just returns it as JSON. JSON cannot hold numpy array. 
    # We should probably save it and return the filename, OR base64 encode it.
    # routes.py: return jsonify({ ..., "output_image": result["output_image"] })
    # Let's save it to a processed folder.
    
    import os
    output_dir = "samples/output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"processed_{filename}")
    cv2.imwrite(output_path, output_image)

    return {
        "detections": detections,
        "output_image": output_path
    }
