import cv2
import numpy as np

def blur_region(image, bbox):
    return image

def erase_region(image, bbox):
    return image

def blur_faces(image_path, detections, output_path):
    """
    Blurs the faces in the image based on detections and saves to output_path.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not open or find the image: {image_path}")

    for detection in detections:
        # Check if the detection is a face
        if detection.get("type") == "face":
            bbox = detection.get("bbox")
            if bbox:
                x1, y1, x2, y2 = map(int, bbox)

                # Ensure coordinates are within image bounds
                h, w = image.shape[:2]
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)

                if x2 > x1 and y2 > y1:
                    # Extract the region of interest (ROI)
                    roi = image[y1:y2, x1:x2]

                    # Apply Gaussian Blur
                    # Calculate kernel size based on ROI size to make it adaptive
                    # or use a fixed strong blur.
                    k_w = (x2 - x1) // 3
                    k_h = (y2 - y1) // 3
                    if k_w % 2 == 0: k_w += 1
                    if k_h % 2 == 0: k_h += 1

                    # Ensure kernel size is at least 3
                    k_w = max(3, k_w)
                    k_h = max(3, k_h)

                    blurred_roi = cv2.GaussianBlur(roi, (k_w, k_h), 0)

                    # Put the blurred ROI back into the image
                    image[y1:y2, x1:x2] = blurred_roi

    # Save the processed image
    cv2.imwrite(output_path, image)
