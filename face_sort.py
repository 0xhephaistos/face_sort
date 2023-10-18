import os
import argparse
import shutil
from deepface import DeepFace
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def classify_age(age):
    if age <= 17:
        return "child"
    elif age <= 35:
        return "young"
    elif age <= 55:
        return "mid_age"
    else:
        return "old"

def process_image(image_name, input_folder, output_folder, copy, dry_run, backup):
    try:
        image_path = os.path.join(input_folder, image_name)

        # Analyze image with DeepFace
        obj = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], detector_backend="retinaface")
        
        # Debugging: Log DeepFace output
        logging.info(f"DeepFace Output for {image_name}: {obj}")

        gender = obj[0]['dominant_gender']
        ethnicity = obj[0]['dominant_race']
        age = obj[0]['age']
        age_group = classify_age(age)

        # Create and set destination folder
        destination_folder = os.path.join(output_folder, gender, ethnicity, age_group)
        os.makedirs(destination_folder, exist_ok=True)
        
        destination_path = os.path.join(destination_folder, image_name)
        
        if dry_run:
            logging.info(f"[Dry Run] Would have moved {image_path} to {destination_path}")
            return
        
        # Backup if required
        if backup:
            backup_folder = os.path.join(output_folder, 'backup')
            os.makedirs(backup_folder, exist_ok=True)
            shutil.copy(image_path, os.path.join(backup_folder, image_name))
        
        # Copy or move the image to the destination folder
        if copy:
            shutil.copy(image_path, destination_path)
        else:
            shutil.move(image_path, destination_path)

        logging.info(f"Successfully processed {image_name}")

    except Exception as e:
        logging.error(f"Failed to process {image_name}. Error: {str(e)}")

def main(input_folder, output_folder, copy, dry_run, backup):
    images = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))]
    
    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda x: process_image(x, input_folder, output_folder, copy, dry_run, backup), images), total=len(images)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort images based on attributes.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing images.')
    parser.add_argument('--output_folder', type=str, default='output', help='Destination folder for sorted images.')
    parser.add_argument('-cp', action='store_true', help='Copy images instead of moving.')
    parser.add_argument('--dry_run', action='store_true', help='Simulates the sorting without actually moving or copying files.')
    parser.add_argument('-bk', action='store_true', help='Backup original images.')
    
    args = parser.parse_args()
    main(args.input_folder, args.output_folder, args.cp, args.dry_run, args.bk)
