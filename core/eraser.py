import cv2
import numpy as np
from core.context_rules import decide_action

def blur_region(image, x1, y1, x2, y2, ksize=(51, 51)):
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
    blurred = cv2.GaussianBlur(roi, ksize, 0)
    image[y1:y2, x1:x2] = blurred
    return image


def erase_region(image, x1, y1, x2, y2):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255

    # Inpainting removes the region realistically
    image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    return image


def apply_anonymization(image, detections, context="public"):
    """
    context: 'public' or 'private'
    """
    action = decide_action(context)

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]

        # All detected objects (faces, plates, IDs) follow the same context rules
        # "blur" for public, "erase" for private.
        # verify_pipeline.py and previous logic confirms this uniform behavior.

        if action == "blur":
            image = blur_region(image, x1, y1, x2, y2)
        elif action == "erase":
            image = erase_region(image, x1, y1, x2, y2)

    return image
