import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

from core.pipeline import run_pipeline
import cv2

def verify():
    image_path = "face1.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    print("Running Public Context...")
    try:
        # We need to hack the pipeline or just rename the file after running
        # actually pipeline.py saves to processed_{filename}. 
        # Let's modify pipeline.py to accept an output path OR just rename it here.
        # But pipeline.py logic is hardcoded to processed_...
        # Let's modify pipeline.py first to be more flexible? 
        # Or faster: just rename the file after it returns.
        
        res_public = run_pipeline(image_path, context="public")
        public_out = res_public['output_image']
        new_public_out = public_out.replace(".png", "_public.png")
        if os.path.exists(public_out):
            os.rename(public_out, new_public_out)
            res_public['output_image'] = new_public_out
            
        print(f"Public result: {res_public['output_image']}")
        print(f"Detections: {len(res_public['detections'])}")
    except Exception as e:
        print(f"Public context failed: {e}")
        import traceback
        traceback.print_exc()

    print("\nRunning Private Context...")
    try:
        res_private = run_pipeline(image_path, context="private")
        private_out = res_private['output_image']
        new_private_out = private_out.replace(".png", "_private.png")
        if os.path.exists(private_out):
            os.rename(private_out, new_private_out)
            res_private['output_image'] = new_private_out

        print(f"Private result: {res_private['output_image']}")
        print(f"Detections: {len(res_private['detections'])}")
    except Exception as e:
        print(f"Private context failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()
