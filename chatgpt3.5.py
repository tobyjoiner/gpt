import subprocess

def download_files(source, destination, file_list):
    # Load previously downloaded files
    try:
        with open('downloaded_files.txt', 'r') as f:
            downloaded_files = set(f.read().splitlines())
    except FileNotFoundError:
        downloaded_files = set()

    # Filter files that haven't been downloaded yet
    files_to_download = [file for file in file_list if file not in downloaded_files]

    if not files_to_download:
        print("No new files to download.")
        return

    # Download files using rsync
    rsync_command = ['rsync', '-avz', '--progress', source, destination]
    rsync_command.extend(files_to_download)

    try:
        subprocess.run(rsync_command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error downloading files:", e)
    else:
        # Update the list of downloaded files
        downloaded_files.update(files_to_download)
        with open('downloaded_files.txt', 'w') as f:
            f.write('\n'.join(downloaded_files))

# Example usage
source = 'user@example.com:/remote/source/directory/'
destination = '/local/destination/directory/'
file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # List of files to download

download_files(source, destination, file_list)
