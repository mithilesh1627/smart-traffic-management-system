import cv2
import shutil
from config import RAW_IMG_DIR, DATASET_DIR, TEST_SPLIT_METADATA

TEST_IMG_DIR = DATASET_DIR / "Processed_dataset" / "test" / "images"
TEST_LABL_DIR = DATASET_DIR / "Processed_dataset" / "test" / "labels"

TEST_IMG_DIR.mkdir(parents=True, exist_ok=True)
TEST_LABL_DIR.mkdir(parents=True, exist_ok=True)
def main():
    try:
        with open(TEST_SPLIT_METADATA, "r") as f:
            for idx, line in enumerate(f):
                rel_path = line.strip() + ".jpg"

                img_path = RAW_IMG_DIR / rel_path
                dst_path = TEST_IMG_DIR / img_path.name

                if not img_path.exists():
                    print("Missing:", img_path)
                    continue

                shutil.copy2(img_path, dst_path)

                image = cv2.imread(str(img_path))
                if image is None:
                    print("Failed to read:", img_path)
                    continue

                cv2.imshow(f"image {idx}", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                if idx == 1:
                    break

    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()