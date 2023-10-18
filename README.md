## face_sort
Simple command line tool to sort faces based on different criteria

## Description

This Python script sorts images based on gender, ethnicity, and age. It reads images from a given input folder and moves or copies them to an output folder, organizing them into nested subfolders based on the identified attributes.

## Requirements

- Python 3.x
- DeepFace library
- tqdm library

To install the required Python packages, run:

```bash
pip install deepface tqdm
```
## Usage

Basic Usage
To run the script, navigate to the folder containing the script in your terminal and execute:

```bash
python face_sort.py [input_folder]
```

Replace [input_folder] with the path to the folder containing the images you want to sort.

## Optional Parameters
* --output_folder [folder_name]: Specify an alternate destination folder. Default is output.
* -cp: Copy images instead of moving.
* --dry_run: Simulate the sorting process without moving or copying files.
* -bk: Backup original images.

## Examples
Run script with default output folder and move files:

```bash
python face_sort.py /path/to/input_folder
```

Run script with a custom output folder and copy files:

```bash
python face_sort.py /path/to/input_folder --output_folder /path/to/output_folder -cp
```

## Optional Features

* Dry Run: To see what the script will do without actually moving or copying any files, use the --dry_run option.
* Backup: To create a backup of the original images, use the -bk option.
