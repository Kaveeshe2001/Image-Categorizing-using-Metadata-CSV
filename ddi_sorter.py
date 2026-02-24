import os
import shutil
import pandas as pd

# Exact path to ddi_metadata.csv file
CSV_FILE_PATH = r"D:\3rd sem\Research\ddidiversedermatologyimages\ddi_metadata.csv"

# Folder where all downloaded DDI .png images are currently sitting
LOCAL_SOURCE_FOLDER = r"D:\3rd sem\Research\ddidiversedermatologyimages"

# Folder where the Benign and Malignant folders to be created
DESTINATION_FOLDER = r"D:\3rd sem\Research\ddidiversedermatologyimages\Sorted-DDI"

def sort_ddi_images():
    print("Loading DDI CSV metadata...")
    
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find the file: {CSV_FILE_PATH}")
        return

    moved_counts = {"Benign": 0, "Malignant": 0, "Missing": 0}

    print("Sorting files...")
    
    # Iterate through every row in the CSV
    for index, row in df.iterrows():
        # Get filename and malignancy status directly from your CSV
        filename = row['DDI_file']
        is_malignant = row['malignant']
        
        # Check if the filename already has .png, if not, add it
        if not str(filename).endswith('.png'):
            filename = f"{filename}.png"

        # Categorize based on the boolean True/False in the 'malignant' column
        if is_malignant == True:
            category = "Malignant"
        else:
            category = "Benign"
            
        # Ensure folders exist
        dest_dir = os.path.join(DESTINATION_FOLDER, category)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        source_path = os.path.join(LOCAL_SOURCE_FOLDER, filename)
        dest_path = os.path.join(dest_dir, filename)
        
        # Move the file if it exists
        if os.path.exists(source_path):
            try:
                shutil.move(source_path, dest_path)
                moved_counts[category] += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            moved_counts["Missing"] += 1

    print("\n--- Sorting Complete ---")
    print(f"Benign moved: {moved_counts['Benign']}")
    print(f"Malignant moved: {moved_counts['Malignant']}")
    if moved_counts["Missing"] > 0:
        print(f"Missing images (Not found in source folder): {moved_counts['Missing']}")

if __name__ == "__main__":
    sort_ddi_images()