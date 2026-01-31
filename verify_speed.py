import requests
import time
import os

def test_speed():
    url = "http://127.0.0.1:5001/upload"
    img_path = "face1.png"
    
    # Ensure dummy image exists
    if not os.path.exists(img_path):
        import cv2
        import numpy as np
        # Create a large dummy image (e.g. 4000x3000) to test resizing
        dummy = np.zeros((3000, 4000, 3), dtype=np.uint8)
        cv2.imwrite(img_path, dummy)
        print("Created dummy 4K image.")

    print(f"Uploading {img_path}...")
    start_time = time.time()
    
    with open(img_path, "rb") as f:
        files = {"file": f}
        data = {"context": "public"}
        try:
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
        except Exception as e:
            print(f"Request failed: {e}")
            return

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Total Time: {duration:.4f} seconds")

if __name__ == "__main__":
    test_speed()
