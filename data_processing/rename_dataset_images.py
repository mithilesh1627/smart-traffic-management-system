import os
from utils.config import TRAIN_IMG_DIR,VALID_IMG_DIR,TEST_IMG_DIR

def rename_images(image_dir, start_index=1):
    images = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

    idx = start_index
    for img in images:
        ext = os.path.splitext(img)[1]
        old_path = os.path.join(image_dir, img)
        new_name = f"{idx}{ext}"
        new_path = os.path.join(image_dir, new_name)

        os.rename(old_path, new_path)
        idx += 1

    print(f" Renamed images in {image_dir}")

rename_images(TRAIN_IMG_DIR, start_index=1)
rename_images(VALID_IMG_DIR, start_index=1000)
rename_images(TEST_IMG_DIR, start_index=2000)