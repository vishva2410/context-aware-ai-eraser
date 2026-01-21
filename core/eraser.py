import cv2
import numpy as np
from core.context_rules import decide_action

def blur_region(image, bbox):
    x1, y1, x2, y2 = bbox
    roi = image[y1:y2, x1:x2]
    # Apply strong Gaussian blur
    # Kernel size must be odd
    k_w = int((x2-x1) * 0.5) // 2 * 2 + 1
    k_h = int((y2-y1) * 0.5) // 2 * 2 + 1
    k_w = max(1, k_w)
    k_h = max(1, k_h)
    
    blurred_roi = cv2.GaussianBlur(roi, (k_w, k_h), 0)
    image[y1:y2, x1:x2] = blurred_roi
    return image

def erase_region(image, bbox):
    x1, y1, x2, y2 = bbox
    # Create a mask for the region
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255
    
    # Use inpainting to remove the content
    # radius 3, TELEA algorithm
    try:
        image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    except Exception as e:
        print(f"Inpainting failed: {e}. Fallback to black box.")
        # Fallback to black box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), -1)
        
    return image

def apply_anonymization(image, detections, context="public"):
    action_type = decide_action(context)
    
    if not action_type:
        return image
        
    # We should iterate through detections and apply changes.
    # Note: If we use inpainting, it modifies the image structure.
    # It's better to process them one by one.
    
    # Filter detections based on context if needed?
    # The prompt says:
    # Public Mode: Minimal redaction (e.g., only blurs license plates, keeps faces visible).
    # Private Mode: Aggressive redaction (blurs/erases faces, IDs, and background text).
    
    # But `decide_action` just returns "blur" or "erase" based on context string.
    # It doesn't seem to account for object type.
    # We need to refine the logic here or in context_rules.py.
    # However, I should stick to the existing `decide_action` or improve it?
    # The README says:
    # * If Context == Public: Ignore Faces, Mask Plates.
    # * If Context == Private: Mask Faces, Mask Plates, Mask IDs.
    
    # Let's adjust logic here to respect the object type as per README specs,
    # because `decide_action` in `context_rules.py` is too simple (just based on public/private).
    # I will override or enhance the logic here.
    
    for det in detections:
        label = det.get("label")
        bbox = det.get("bbox")
        
        should_act = False
        method = "blur" # default
        
        if context == "public":
            if label == "license_plate":
                should_act = True
                method = "blur" # Public usually implies lighter touch, or standard blur
            elif label == "face":
                should_act = False # Keep faces visible
                
        elif context == "private":
            should_act = True
            method = "erase" # Aggressive redaction
            
        if should_act:
            if method == "blur":
                image = blur_region(image, bbox)
            elif method == "erase":
                image = erase_region(image, bbox)
                
    return image
