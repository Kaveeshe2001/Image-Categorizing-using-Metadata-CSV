import os
import shutil
import pandas as pd

# --- CONFIGURATION ---
# 1. Path to the CSV
CSV_FILE_PATH = r"D:\3rd sem\Research\fitzpatrick17k\fitzpatrick17k.csv"

# Folder where all downloaded images are sitting
LOCAL_SOURCE_FOLDER = r"D:\3rd sem\Research\fitzpatrick17k\data\finalfitz17k"

# 3. Provide the destination folder for sorting
DESTINATION_FOLDER = r"D:\3rd sem\Research\fitzpatrick17k\Fitz17k-sorted"

def sort_fitzpatrick_images():
    print(f"Loading CSV metadata from {CSV_FILE_PATH}...")
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find the file: {CSV_FILE_PATH}")
        return

    moved_counts = {}

    print("Sorting files into folders...")
    
    for index, row in df.iterrows():
        # Get the image filename. 
        # In Fitzpatrick17k, filenames are in the 'md5hash' column
        image_name = str(row['md5hash'])
        if not image_name.endswith('.jpg'):
            image_name = f"{image_name}.jpg"
            
        # First Level: Determine Malignancy
        # look at the 'three_partition_label' which contains: malignant, benign, non-neoplastic
        partition_3 = str(row.get('three_partition_label', '')).strip().lower()
        
        if partition_3 == 'malignant':
            malignancy_status = "Malignant"
        else:
            # Treats both 'benign' and 'non-neoplastic' as Benign for your binary split
            malignancy_status = "Benign" 

        # Second Level: Determine Skin Type
        try:
            fst = int(row['fitzpatrick_scale'])
        except (ValueError, TypeError):
            fst = -1 # Catch missing or 'NaN' values

        if fst in [1, 2, 3]:
            skin_type = "Fitswhite"
        elif fst in [4, 5, 6]:
            skin_type = "Fitsdark"
        else:
            skin_type = "Unknown_Skin_Type" # Handles -1 values in the dataset

        # Define the target folder path 
        target_folder = os.path.join(DESTINATION_FOLDER, malignancy_status, skin_type)
        
        # Create directories if they don't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        source_path = os.path.join(LOCAL_SOURCE_FOLDER, image_name)
        dest_path = os.path.join(target_folder, image_name)
        
        # Move the file
        if os.path.exists(source_path):
            try:
                shutil.move(source_path, dest_path)
                
                # Tracking statistics
                stat_key = f"{malignancy_status}_{skin_type}"
                moved_counts[stat_key] = moved_counts.get(stat_key, 0) + 1
            except Exception as e:
                print(f"Error moving {image_name}: {e}")
        else:
            moved_counts["Missing_Local_File"] = moved_counts.get("Missing_Local_File", 0) + 1

    # --- SUMMARY ---
    print("\n--- Sorting Complete ---")
    for category, count in sorted(moved_counts.items()):
        if count > 0:
            print(f"{category.replace('_', ' ')}: {count}")

if __name__ == "__main__":
    sort_fitzpatrick_images()