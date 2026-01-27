from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path, conf=0.3):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, image):
        """
        Detect license plates in the given image.
        :param image: numpy array (cv2 image) or file path
        """
        results = self.model(image, conf=self.conf, verbose=False)
        detections = []

        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "label": "license_plate",
                    "bbox": [x1, y1, x2, y2],
                    "score": float(box.conf[0])
                })

        return detections
