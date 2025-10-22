import subprocess
import sys
import os
import shutil

# ASCII Art Banner
ascii_banner = r"""
       /$$                                                                            /$$
      | $$                                                                           | $$
  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$$  /$$$$$$   /$$$$$$$
 /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$_____//$$_____/ /$$__  $$ /$$__  $$
| $$  | $$| $$$$$$$$| $$  \ $$| $$  \__/| $$$$$$$$|  $$$$$$|  $$$$$$ | $$$$$$$$| $$  | $$
| $$  | $$| $$_____/| $$  | $$| $$      | $$_____/ \____  $$\____  $$| $$_____/| $$  | $$
|  $$$$$$$|  $$$$$$$| $$$$$$$/| $$      |  $$$$$$$ /$$$$$$$//$$$$$$$/|  $$$$$$$|  $$$$$$$
 \_______/ \_______/| $$____/ |__/       \_______/|_______/|_______/  \_______/ \_______/
                    | $$                                                                 
                    | $$                                                                 
                    |__/                                                                                                       
"""

# Mapping of MIME types to their typical file extensions
mime_extensions = {
    'application/x-lz4': '.lz4',
    'application/x-xz': '.xz',
    'application/zip': '.zip',
    'application/x-7z-compressed': '.7z',
    'application/gzip': '.gz',
    'application/x-bzip2': '.bz2',
    'application/zstd': '.zst',
    'application/x-zstd': '.zst',
    'application/x-rar': '.rar',
    'application/x-rar-compressed': '.rar',
    'application/x-tar': '.tar',
    'application/x-gtar': '.tar',
}

def detect_file_type(filepath):
    """
    Detect the MIME type of a file using the 'file' command.
    Returns the MIME type as a string.
    """
    result = subprocess.run(['file', '--mime-type', filepath], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running file command: {result.stderr}")
        sys.exit(1)
    # Output format: filename: mime/type
    mime_type = result.stdout.split(':')[-1].strip()
    return mime_type

def ensure_extension(filepath, mime_type):
    """
    If the file does not have the expected extension for its MIME type,
    rename it to include the correct extension.
    Returns the (possibly new) filepath.
    """
    ext = mime_extensions.get(mime_type)
    if not ext:
        return filepath
    if not filepath.endswith(ext):
        new_filepath = filepath + ext
        print(f"Renaming '{filepath}' to '{new_filepath}' for proper extension.")
        shutil.move(filepath, new_filepath)
        return new_filepath
    return filepath

def decompress_file(filepath, mime_type):
    """
    Decompress the file using the appropriate tool based on its MIME type.
    For archive formats, returns a list of all new files extracted.
    For single-file decompressors, returns the decompressed file.
    """
    decompressors = {
        'application/x-lz4': lambda f: ['lz4', '-d', f],
        'application/x-xz': lambda f: ['unxz', f],
        'application/zip': lambda f: ['unzip', '-o', f],
        'application/x-7z-compressed': lambda f: ['7z', 'x', f],
        'application/gzip': lambda f: ['gunzip', f],
        'application/x-bzip2': lambda f: ['bunzip2', f],
        'application/zstd': lambda f: ['zstd', '-d', f],
        'application/x-zstd': lambda f: ['zstd', '-d', f],
        'application/x-rar': lambda f: ['unrar', 'x', '-o+', f],
        'application/x-rar-compressed': lambda f: ['unrar', 'x', '-o+', f],
        'application/x-tar': lambda f: ['tar', '-xf', f],
        'application/x-gtar': lambda f: ['tar', '-xf', f],
    }
    if mime_type not in decompressors:
        return []
    cmd = decompressors[mime_type](filepath)
    print(f"Decompressing using: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error decompressing file: {result.stderr}")
        sys.exit(1)
    # For archive formats, return all new files in the current directory (excluding the archive itself)
    if mime_type in [
        'application/zip',
        'application/x-7z-compressed',
        'application/x-rar',
        'application/x-rar-compressed',
        'application/x-tar',
        'application/x-gtar'
    ]:
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f != filepath]
        return files
    else:
        # For single-file decompressors, remove known compression extensions
        ext = mime_extensions.get(mime_type, '')
        if ext and filepath.endswith(ext):
            next_file = filepath[:-len(ext)]
        else:
            next_file = filepath
        return [next_file]

if __name__ == "__main__":
    # Print ASCII art banner
    print('\n- Made by 0xshr00msz -\n')
    print(ascii_banner)
    print('Ensure to isolate this script together with the compressed file only.\n')
    # Check for correct usage
    if len(sys.argv) != 2:
        print("Usage: python decompress.py <file>\n")
        sys.exit(1)
    # Initialize queue with the input file
    queue = [sys.argv[1]]
    # Track processed files to avoid loops
    processed = set()
    # Main loop: process files until queue is empty
    while queue:
        filepath = queue.pop(0)
        # Skip if not a file or already processed
        if not os.path.isfile(filepath) or filepath in processed:
            continue
        # Detect MIME type
        mime_type = detect_file_type(filepath)
        print(f"Detected MIME type: {mime_type} for file: {filepath}")
        # Ensure file has correct extension
        filepath = ensure_extension(filepath, mime_type)
        # Decompress and get new files
        new_files = decompress_file(filepath, mime_type)
        processed.add(filepath)
        # Add new files to queue if not already processed
        for f in new_files:
            if f not in processed and os.path.isfile(f):
                queue.append(f)
    print("Decompression complete. No more compressed files detected.")
