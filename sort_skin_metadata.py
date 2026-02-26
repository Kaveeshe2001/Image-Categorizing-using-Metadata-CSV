import os
import shutil
import pandas as pd

# --- CONFIGURATION ---
# Exact path to CSV file
CSV_FILE_PATH = r"D:\3rd sem\Research\dataverse_files\METADATA\Skin_Metadata-1.csv"

# Folder where all unsorted images are currently sitting
LOCAL_SOURCE_FOLDER = r"D:\3rd sem\Research\Dataverse"

# Main destination folder for sorting
DESTINATION_FOLDER = r"D:\3rd sem\Research\Sorted_dataverse"

# --- MEDICAL CLASSIFICATION ---
# Strictly Malignant (Including the medically corrected CTCL)
MALIGNANT_DISEASES = [
    "Squamous Cell Carcinoma",
    "Basal Cell Carcinoma",
    "Melanoma",
    "Bowen's Metastasis",
    "Mycosis fungoides"  # Corrected from 'Fungal' to 'Malignant Lymphoma'
]

# Potentially Malignant / Pre-Malignant Disorders (PMDs)
POTENTIALLY_MALIGNANT = [
    "Cheilitis", 
    "Keratoacanthoma", 
    "Actinic Dermatitis"
]

def sort_skin_images():
    print("Loading CSV metadata...")
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find the file: {CSV_FILE_PATH}")
        return

    moved_counts = {}

    print("Sorting files into folders...")
    
    for index, row in df.iterrows():
        # Read data
        image_name = str(row['Image_name'])
        disease = str(row['Disease_label'])
        
        # Determine Skin Type (Second Level)
        fst = str(row['Fitzpatrick']).strip().upper()
        if fst in ['FST 1', 'FST 2', 'FST 3']:
            skin_type = "Fitswhite"
        elif fst in ['FST 4', 'FST 5', 'FST 6']:
            skin_type = "Fitsdark"
        else:
            skin_type = "Unknown_Skin_Type"

        # Determine Malignancy (First Level)
        if disease in MALIGNANT_DISEASES:
            malignancy_status = "Malignant"
        elif disease in POTENTIALLY_MALIGNANT:
            # We filter Cheilitis based on dangerous descriptors
            if disease == "Cheilitis":
                descriptors = str(row['Descriptors']).lower()
                # Red flag clinical descriptors for malignant transformation
                if any(risk in descriptors for risk in ['erosion', 'ulcer', 'crust', 'pigmented']):
                    malignancy_status = "Potentially_Malignant"
                else:
                    malignancy_status = "Benign" 
            else:
                malignancy_status = "Potentially_Malignant"
        else:
            malignancy_status = "Benign"

        # Define the target folder 
        target_folder = os.path.join(DESTINATION_FOLDER, malignancy_status, skin_type)
        
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

    print("\n--- Sorting Complete ---")
    for category, count in sorted(moved_counts.items()):
        if count > 0:
            print(f"{category.replace('_', ' ')}: {count}")

if __name__ == "__main__":
    sort_skin_images()