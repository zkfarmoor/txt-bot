import pathlib
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_file_to_txt(source_file, target_file):
    """
    Copies the contents of the source file to a new file with a modified .txt extension in the target directory.
    """
    try:
        with open(source_file, 'rb') as src, open(target_file, 'wb') as tgt:
            tgt.write(src.read())
        logging.info(f"Successfully converted {source_file} to {target_file}")
    except Exception as e:
        logging.error(f"Failed to convert {source_file} to {target_file}: {e}")

def convert_files_to_txt(source_folder, target_folder_base):
    """
    Convert all files in the source folder to .txt files in a new target folder,
    preserving the directory structure and creating the target folder based on source folder name.
    Excludes image files such as .png, .jpg, .svg, and Markdown files (.md).
    
    Args:
    source_folder (str): The path to the source directory.
    target_folder_base (str): The base path where the new target directory will be created.
    """
    source = pathlib.Path(source_folder)
    target_folder = pathlib.Path(target_folder_base) / (source.name + "_txt")
    
    # Ensure the target directory exists
    target_folder.mkdir(parents=True, exist_ok=True)
    
    # List of file extensions to exclude
    excluded_extensions = {'.png', '.jpg', '.jpeg', '.svg', '.md'}

    # Iterate over all files in the source directory
    for file in source.rglob('*'):
        if file.is_file() and file.suffix.lower() not in excluded_extensions:  # Ensure it's a file and not an excluded type
            # Construct the new path in the target directory
            relative_path = file.relative_to(source)
            if file.suffix:  # Check if there is an extension
                new_file_name = f"{relative_path.stem}({file.suffix}).txt"
            else:
                new_file_name = f"{relative_path.stem}.txt"
            new_file_path = target_folder.joinpath(relative_path.with_name(new_file_name))
            
            # Create any necessary directories
            new_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert the file to a .txt extension with the original extension included in the name
            convert_file_to_txt(file, new_file_path)
        else:
            logging.info(f"Skipped conversion for excluded file {file}")

def main():
    print("Script started...")
    parser = argparse.ArgumentParser(description="Convert files to .txt format while preserving the folder structure and cloning original, excluding image files.")
    parser.add_argument("source_folder", type=str, help="Path to the source directory")
    parser.add_argument("target_folder_base", type=str, help="Base path for the new target directory")
    
    args = parser.parse_args()
    
    print(f"Converting files from {args.source_folder} to {args.target_folder_base}")
    convert_files_to_txt(args.source_folder, args.target_folder_base)
    print("Conversion complete.")

if __name__ == "__main__":
    main()

