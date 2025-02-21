import os


def rename_images(folder_path):
    # Get the list of files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Filter to include only image files (optional, based on extensions)
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')  # Add other formats if needed
    images = [file for file in files if file.lower().endswith(image_extensions)]

    # Sort files to maintain order (optional)
    images.sort()

    # Rename images
    for index, image in enumerate(images[:50]):  # Process only the first 50 images
        new_name = f"star{index + 1}.jpg"  # New file name
        src = os.path.join(folder_path, image)
        dst = os.path.join(folder_path, new_name)

        try:
            os.rename(src, dst)
            print(f"Renamed: {image} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {image}: {e}")


# Usage
folder_path = '"C:/Users/Asus/Downloads/image1"'  # Replace with the actual folder path
rename_images(folder_path)
