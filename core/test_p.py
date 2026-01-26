import os
from core.pipeline import run_pipeline

# Try to find a valid test image
possible_paths = [
    "samples/input/face1.png",
    "face1.png",
    "samples/input/brain.png"
]

image_path = None
for path in possible_paths:
    if os.path.exists(path):
        image_path = path
        break

if image_path is None:
    # If no image found, create a dummy one or raise error?
    # Better to raise error so we know something is wrong with setup.
    raise ValueError(f"No test image found. Checked: {possible_paths}")

print(f"Using test image: {image_path}")

# PUBLIC context
print("Running PUBLIC context...")
try:
    res_public = run_pipeline(image_path, context="public")
    print(f"✅ Public output: {res_public['output_image']}")
except Exception as e:
    print(f"❌ Public context failed: {e}")
    raise

# PRIVATE context
print("Running PRIVATE context...")
try:
    res_private = run_pipeline(image_path, context="private")
    print(f"✅ Private output: {res_private['output_image']}")
except Exception as e:
    print(f"❌ Private context failed: {e}")
    raise

print("✅ Test completed. Check samples/output/")
