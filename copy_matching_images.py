import os
import shutil

# --- CONFIGURATION ---
# The folder containing the names you want to look for
REFERENCE_FOLDER = r"D:\3rd sem\Research Ideas\Resnet Dataset\Fitsdark\4DDIG_20260309_142516\D\3rd sem\Research Ideas\Resnet Dataset\Fitsdark\benign dark"

# The folder you want to search through to find the actual files
SOURCE_FOLDER = r"D:\3rd sem\Research\fitzpatrick17k\Fitz17k-sorted\Benign\Fitsdark"

# The folder where the matched images will be pasted
DESTINATION_FOLDER = r"D:\3rd sem\Research Ideas\Resnet Dataset\Fitsdark\dark ben"

def copy_matching_images_robust():
    if not os.path.exists(DESTINATION_FOLDER):
        os.makedirs(DESTINATION_FOLDER)
        print(f"Created destination folder: {DESTINATION_FOLDER}")

    # Step 1: Read image names (Normalized: lowercase and spaces removed)
    reference_names = set()
    try:
        for filename in os.listdir(REFERENCE_FOLDER):
            if os.path.isfile(os.path.join(REFERENCE_FOLDER, filename)):
                base_name, _ = os.path.splitext(filename)
                
                # Normalize: Make it lowercase and strip invisible spaces
                reference_names.add(base_name.strip().lower())
    except FileNotFoundError:
        print(f"Error: Reference folder not found.")
        return

    print(f"Loaded {len(reference_names)} unique image names to look for.")

    # Step 2: Search the Source Folder RECURSIVELY
    copied_count = 0
    print("Scanning source folder and all subfolders... (This might take a moment)")
    
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for filename in files:
            source_path = os.path.join(root, filename)
            base_name, _ = os.path.splitext(filename)
            
            # Normalize the source name so it perfectly matches the reference
            normalized_base = base_name.strip().lower()
            
            if normalized_base in reference_names:
                dest_path = os.path.join(DESTINATION_FOLDER, filename)
                
                # Prevent crashing if two subfolders have files with the exact same name
                if os.path.exists(dest_path):
                    continue 

                try:
                    shutil.copy2(source_path, dest_path)
                    copied_count += 1
                except Exception as e:
                    print(f"Error copying {filename}: {e}")

    # --- SUMMARY ---
    print(f"\nTask Complete! Successfully found and copied {copied_count} files.")

if __name__ == "__main__":
    copy_matching_images_robust()