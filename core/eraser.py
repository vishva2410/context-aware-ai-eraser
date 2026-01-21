import cv2
import numpy as np

def blur_region(image, bbox):
    x1, y1, x2, y2 = bbox

    # Ensure bbox is within image bounds
    h_img, w_img = image.shape[:2]
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w_img, x2)
    y2 = min(h_img, y2)

    if x1 >= x2 or y1 >= y2:
        return image

    roi = image[y1:y2, x1:x2]

    # Apply Gaussian blur
    # Kernel size should be odd and depend on the ROI size
    h, w = roi.shape[:2]
    k_w = int(w // 3) | 1
    k_h = int(h // 3) | 1
    # Ensure kernel size is at least 1
    k_w = max(1, k_w)
    k_h = max(1, k_h)

    blurred_roi = cv2.GaussianBlur(roi, (k_w, k_h), 0)
    image[y1:y2, x1:x2] = blurred_roi
    return image

def blur_faces(image_path, detections, output_path):
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not open or find the image: {image_path}")

    for detection in detections:
        bbox = detection["bbox"]
        image = blur_region(image, bbox)

    # Save output
    cv2.imwrite(output_path, image)
    return output_path

def erase_region(image, bbox):
    # For now, just black it out as a placeholder for erase
    x1, y1, x2, y2 = bbox

    # Ensure bbox is within image bounds
    h_img, w_img = image.shape[:2]
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w_img, x2)
    y2 = min(h_img, y2)

    if x1 >= x2 or y1 >= y2:
        return image

    image[y1:y2, x1:x2] = (0, 0, 0)
    return image
