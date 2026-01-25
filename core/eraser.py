import cv2
import numpy as np

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
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = det["label"]

        # LICENSE PLATE RULES
        if label == "license_plate":
            if context == "public":
                image = blur_region(image, x1, y1, x2, y2)
            elif context == "private":
                image = erase_region(image, x1, y1, x2, y2)

        # FACE RULES
        elif label == "face":
            if context == "public":
                image = blur_region(image, x1, y1, x2, y2)
            elif context == "private":
                image = erase_region(image, x1, y1, x2, y2)

        # ID CARD RULES
        elif label == "id_card":
            if context == "public":
                image = blur_region(image, x1, y1, x2, y2)
            elif context == "private":
                image = erase_region(image, x1, y1, x2, y2)

    return image
