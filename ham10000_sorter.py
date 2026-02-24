import os
import shutil
import pandas as pd

# Path to CSV file
CSV_FILE_PATH = r"D:\3rd sem\Research\Dataset Hm100\HAM10000_metadata.csv"

# Folder where all HAM10000 images are currently sitting
LOCAL_SOURCE_FOLDER = r"D:\3rd sem\Research\Dataset Hm100\HAM10000"

# Folder where the Benign and Malignant folders to be created
DESTINATION_FOLDER = r"D:\3rd sem\Research\Dataset Hm100\HAM10000 Sorted"

# Map the 'dx' codes from the dataset to Benign or Malignant
dx_to_category = {
    'mel': 'Malignant',
    'bcc': 'Malignant',
    'akiec': 'Malignant',
    'nv': 'Benign',
    'bkl': 'Benign',
    'df': 'Benign',
    'vasc': 'Benign'
}

def sort_ham10000_images():
    print("Loading CSV metadata...")
    
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Could not find the file: {CSV_FILE_PATH}")
        return

    # Track how many we move
    moved_counts = {"Benign": 0, "Malignant": 0, "Missing": 0}

    print("Sorting files...")
    for index, row in df.iterrows():
        image_id = row['image_id']
        dx_code = row['dx']
        
        # Determine the category based on the dictionary map
        category = dx_to_category.get(dx_code, "Unknown")
        
        if category == "Unknown":
            print(f"Warning: Unknown diagnosis code '{dx_code}' for image {image_id}")
            continue
            
        # Ensure folders exist
        dest_dir = os.path.join(DESTINATION_FOLDER, category)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        # The HAM10000 dataset usually comes as .jpg images
        filename = f"{image_id}.jpg"
        source_path = os.path.join(LOCAL_SOURCE_FOLDER, filename)
        dest_path = os.path.join(dest_dir, filename)
        
        # Move the file if it exists in the source folder
        if os.path.exists(source_path):
            try:
                shutil.move(source_path, dest_path)
                moved_counts[category] += 1
                # print(f"Moved {filename} -> {category}") # Uncomment to see progress line-by-line
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            moved_counts["Missing"] += 1

    # --- SUMMARY ---
    print("\n--- Sorting Complete ---")
    print(f"Benign moved: {moved_counts['Benign']}")
    print(f"Malignant moved: {moved_counts['Malignant']}")
    if moved_counts["Missing"] > 0:
        print(f"Missing images (Not found in source folder): {moved_counts['Missing']}")

if __name__ == "__main__":
    sort_ham10000_images()