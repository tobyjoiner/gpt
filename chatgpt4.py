import subprocess
import os

# Configuration
source = "user@server:path/to/source/"
destination = "/path/to/destination"
log_file_path = "/path/to/download.log"

# Ensure the log file exists
if not os.path.exists(log_file_path):
    open(log_file_path, 'a').close()

# Function to check if a file has been downloaded
def is_downloaded(filename):
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if filename in line:
                return True
    return False

# Function to mark a file as downloaded
def mark_as_downloaded(filename):
    with open(log_file_path, 'a') as log_file:
        log_file.write(filename + "\n")

# Function to download files using rsync
def download_files():
    # Use rsync to list all files without actually downloading them (--dry-run)
    result = subprocess.run(['rsync', '--dry-run', '--out-format=%n', source, destination], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error listing files from source.")
        return
    
    # Split the output into file names
    files_to_download = result.stdout.split('\n')
    
    for filename in files_to_download:
        if filename and not is_downloaded(filename):
            # If file hasn't been downloaded, download it
            subprocess.run(['rsync', '-avz', f"{source}{filename}", destination])
            # Mark file as downloaded
            mark_as_downloaded(filename)
            print(f"Downloaded and logged: {filename}")
        else:
            print(f"Skipped (already downloaded): {filename}")

# Run the download process
download_files()
