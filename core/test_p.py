import cv2
from core.pipeline import process_image

# Load test image
img = cv2.imread("samples/input/car.jpg")

if img is None:
    raise ValueError("Image not found. Check path: samples/input/car.jpg")

# PUBLIC context
out_public, _ = process_image(img.copy(), context="public")
cv2.imwrite("samples/output/public.jpg", out_public)

# PRIVATE context
out_private, _ = process_image(img.copy(), context="private")
cv2.imwrite("samples/output/private.jpg", out_private)

print("✅ Test completed. Check samples/output/")
