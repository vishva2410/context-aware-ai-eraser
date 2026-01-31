import cv2
import numpy as np

def blur_region(image, x1, y1, x2, y2, ksize=(51, 51)):
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
    blurred = cv2.GaussianBlur(roi, ksize, 0)
    image[y1:y2, x1:x2] = blurred
    return image


def erase_region(image, x1, y1, x2, y2, padding=20):
    """
    Optimized: Only inpaint the ROI, not the full image.
    """
    h, w = image.shape[:2]
    
    # Add padding to give context for inpainting
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)

    # Extract ROI
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
        
    mask = np.zeros(roi.shape[:2], dtype=np.uint8)
    
    # The area to erase is now relative to the ROI
    # We padded by `padding`, so the object starts at `padding` inside the ROI
    # But wait, we just expanded x1/y1. The internal box also needs to be erased.
    # Actually, simpler: create mask for ROI.
    # The 'box' inside the ROI corresponds to the original (unpadded) coordinates, 
    # but mapped to ROI space.
    # Simpler approach: Just mask the CENTRAL part of the padded ROI.
    # Or, rely on the fact that we passed x1,y1 (original) to this function?
    # Wait, the function receives the BOX coordinates.
    # Let's stick to the coordinates passed.
    
    # Re-calculate relative coords
    # We essentially want to mask the whole box (plus maybe a bit?), 
    # but `inpaint` needs pixels AROUND the mask to fill it in.
    # So we mask the *exact* box inside the *larger* ROI.
    
    rel_x1 = padding
    rel_y1 = padding
    
    # Dimensions of the box
    box_w = (x2 - padding) - (x1 + padding) # Wait, logic tricky.
    
    # Correct logic:
    # 1. Expand box by padding to get ROI coords (rx1, ry1, rx2, ry2)
    rx1 = max(0, x1 - padding)
    ry1 = max(0, y1 - padding)
    rx2 = min(w, x2 + padding)
    ry2 = min(h, y2 + padding)
    
    roi = image[ry1:ry2, rx1:rx2]
    
    # 2. Inside this ROI, the area we want to erase is (x1,y1) to (x2,y2)
    # relative to (rx1, ry1)
    mask_x1 = x1 - rx1
    mask_y1 = y1 - ry1
    mask_x2 = x2 - rx1
    mask_y2 = y2 - ry1
    
    mask = np.zeros(roi.shape[:2], dtype=np.uint8)
    mask[mask_y1:mask_y2, mask_x1:mask_x2] = 255

    # 3. Inpaint only the ROI
    # Radius 3 is usually fast enough.
    inpainted_roi = cv2.inpaint(roi, mask, 3, cv2.INPAINT_TELEA)
    
    # 4. Paste back
    image[ry1:ry2, rx1:rx2] = inpainted_roi
    
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

        # FACE RULES (already detected)
        elif label == "face":
            if context == "private":
                image = blur_region(image, x1, y1, x2, y2)

        # ID CARD RULES
        elif label == "id_card":
            if context == "public":
                image = blur_region(image, x1, y1, x2, y2)
            elif context == "private":
                image = erase_region(image, x1, y1, x2, y2)

    return image
