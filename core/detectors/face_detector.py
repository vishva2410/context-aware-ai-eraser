from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path="models/face_detect.pt", conf=0.15):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, image):
        """
        Detect faces in the given image.
        :param image: numpy array (cv2 image) or file path
        """
        results = self.model(image, conf=self.conf)
        detections = []

        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "label": "face",
                    "bbox": [x1, y1, x2, y2],
                    "score": float(box.conf[0])
                })

        return detections
