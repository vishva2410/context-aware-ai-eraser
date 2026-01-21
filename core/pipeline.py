from core.detectors.face_detector import FaceDetector
from core.detectors.plate_detector import PlateDetector
from core.eraser import apply_anonymization

face_detector = FaceDetector("models/face_detect.pt")
plate_detector = PlateDetector("models/lp_detect.pt")

# Renamed to match API expectation
def run_pipeline(image_path, context="public"):
    # Load image
    import cv2
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Run detectors (detectors accept image path or numpy array depending on implementation, 
    # but based on previous view, they prefer path or just work with YOLO. 
    # Let's pass the path to detectors as they seem to use ultralytics directly on input)
    # FaceDetector.detect takes image_path. PlateDetector.detect takes image.
    # Let's check PlateDetector again. It takes 'image'. YOLO can take path or array. 
    # To be safe, let's pass image_path to both if possible, or array.
    # FaceDetector lines 8-9: results = self.model(image_path, conf=self.conf)
    # PlateDetector lines 8-9: results = self.model(image, conf=self.conf, verbose=False)
    
    # Passing the image path is safest for YOLO
    faces = face_detector.detect(image_path) 
    plates = plate_detector.detect(image_path)

    detections = faces + plates

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
