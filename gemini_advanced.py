import subprocess
import os
import hashlib

# Configuration
SOURCE_DIR = 'user@remote_host:/path/to/remote/files'
DESTINATION_DIR = '/path/to/local/download/folder'
TRACKING_FILE = 'download_history.txt'

def calculate_hash(filepath):
    """Calculates the MD5 hash of a file for tracking purposes."""
    with open(filepath, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def load_download_history(history_file):
    """Loads the download history from the tracking file."""
    history = {}
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            for line in f:
                filename, file_hash = line.strip().split(',')
                history[filename] = file_hash
    return history

def update_download_history(history_file, filename, file_hash):
    """Updates the download history file."""
    with open(history_file, 'a') as f:
        f.write(f"{filename},{file_hash}\n")

def main():
    # Load existing download history
    download_history = load_download_history(TRACKING_FILE)

    # Execute rsync command
    rsync_command = [
        'rsync',
        '-avz',  # Archive mode, verbose, compress
        '--progress', 
        SOURCE_DIR,
        DESTINATION_DIR
    ]
    process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Process rsync output to track downloaded files
    for line in iter(process.stdout.readline, b''):
        filename = line.decode('utf-8').split(' ')[1]  # Extract filename
        if filename in download_history:
            print(f"{filename} already exists. Skipping...")
        else:
            filepath = os.path.join(DESTINATION_DIR, filename)
            file_hash = calculate_hash(filepath)
            update_download_history(TRACKING_FILE, filename, file_hash)

if __name__ == '__main__':
    main()