import argparse
import os
import exifread
from PIL import Image
from PIL import ImageCms
from PIL.ExifTags import TAGS

def display_metadata(image_path):
    try:
        image = Image.open(image_path)
        print("File:", image_path)

        _, file_extension = os.path.splitext(image_path)

        if file_extension.lower() == ".jpg" or file_extension.lower() == ".jpeg":
            # For JPEG files
            print("Metadata:")
            for key, value in image.info.items():
                if (key == "icc_profile" or key == "exif"):
                    continue
                else:
                    print(f"    - {key}: {value}")
            exif_data = image._getexif()
            if exif_data is not None:
                print("EXIF data:")
                for tag_id in exif_data:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)
                    # remove \n from data
                    data = str(data).replace("\n", "")
                    if isinstance(data, bytes):
                        data = data.decode()
                    print(f"    - {tag}: {data}")
            else:
                print("EXIF data: None")

        elif file_extension.lower() == ".png":
            # For PNG files
            print("PNG Metadata:")
            print("    - Width:", image.width)
            print("    - Height:", image.height)
            print("    - Color Mode:", image.mode)
            print("    - Transparency:", image.info.get("transparency"))

            # Extract text metadata if available
            if "text" in image.info:
                print("Text Metadata:")
                for key, value in image.info["text"].items():
                    print(f"{key}: {value}")

        elif file_extension.lower() == ".gif":
            # For GIF files
            print("GIF Metadata:")
            print("    - Width:", image.width)
            print("    - Height:", image.height)
            print("    - Color Palette Size:", image.n_frames)
            print("    - Duration (ms):", image.info.get("duration"))

            # Extract text metadata if available
            if "text" in image.info:
                print("Text Metadata:")
                for key, value in image.info["text"].items():
                    print(f"    - {key}: {value}")

        elif file_extension.lower() == ".bmp":
            # For BMP files
            print("BMP Metadata:")
            print("    - Width:", image.width)
            print("    - Height:", image.height)
            print("    - Color Mode:", image.mode)

    except Exception as e:
        print(f"Error processing file: {image_path}")
        print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A program to parse image files for metadata.")
    parser.add_argument("files", nargs="+", help="List of image files to process.")

    args = parser.parse_args()

    image_files = args.files

    for image_file in image_files:
        if os.path.isfile(image_file):
            display_metadata(image_file)
        else:
            print(f"File not found: {image_file}")
