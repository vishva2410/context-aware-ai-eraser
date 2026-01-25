import os
from core.pipeline import run_pipeline

# Test image path
image_path = "face1.png"

if not os.path.exists(image_path):
    raise ValueError(f"Image not found. Check path: {image_path}")

# PUBLIC context
print("Running PUBLIC context...")
res_public = run_pipeline(image_path, context="public")
print(f"✅ Public output: {res_public['output_image']}")

# PRIVATE context
print("Running PRIVATE context...")
res_private = run_pipeline(image_path, context="private")
print(f"✅ Private output: {res_private['output_image']}")

print("✅ Test completed. Check samples/output/")
