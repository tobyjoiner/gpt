import os
import subprocess
import json


def download_files(remote_host, remote_path, local_path, log_file):
  """
  Downloads files using rsync and keeps track of downloaded files in a log.

  Args:
      remote_host: The hostname or IP address of the remote server.
      remote_path: The path to the directory on the remote server.
      local_path: The path to the local directory where files will be downloaded.
      log_file: The path to the file where downloaded files are logged.
  """

  # Load downloaded files list (empty list on first run)
  downloaded_files = []
  if os.path.exists(log_file):
    with open(log_file, 'r') as f:
      downloaded_files = json.load(f)

  # Build rsync command with archive flag and excluding already downloaded files
  rsync_command = ["rsync", "-av", f"{remote_host}:{remote_path}", local_path]
  exclude_list = " ".join(downloaded_files)
  if exclude_list:
    rsync_command.extend(["--exclude", exclude_list])

  # Run rsync process
  process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, error = process.communicate()

  # Update downloaded files list and save it to log
  if process.returncode == 0:
    for filename in output.decode().splitlines():
      if filename.startswith("sending file"):
        downloaded_files.append(filename.split(" ")[-1])
    with open(log_file, 'w') as f:
      json.dump(downloaded_files, f)
  else:
    print(f"Error downloading files: {error.decode()}")


# Define download parameters (replace with your actual values)
remote_host = "your_remote_host"
remote_path = "/path/to/remote/directory"
local_path = "/path/to/local/directory"
log_file = "downloaded_files.log"

# Run download function
download_files(remote_host, remote_path, local_path, log_file)