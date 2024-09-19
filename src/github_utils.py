# github_utils.py

import os


def get_github_url(row, data_directory):
    # Extract the subdirectory name from the data_directory path
    subdirectory = os.path.basename(data_directory)

    base_url = f"https://github.com/volter-ai/volter-bench/tree/main/data/{subdirectory}"

    # Format the timestamp to match the GitHub folder structure
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")

    # Extract the log file name from the logs path and remove any extra characters
    log_path = row['logs'][0] if isinstance(row['logs'], list) else row['logs']
    log_file = log_path.split('/')[-1].strip("[]'")

    # Construct the GitHub URL
    github_url = f"{base_url}/{formatted_timestamp}/new_prompt_logs/{log_file}"

    return github_url


def get_code_github_url(row, data_directory):
    # Extract the subdirectory name from the data_directory path
    subdirectory = os.path.basename(data_directory)
    base_url = f"https://github.com/volter-ai/volter-bench/tree/main/data/{subdirectory}"
    # Format the timestamp to match the GitHub folder structure
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")
    # Include the run number in the ladder path
    code_path = f"ladder/{row['ladder']}_{row['run']}/main_game"
    # Construct the full GitHub URL
    github_url = f"{base_url}/{formatted_timestamp}/{code_path}"
    return github_url
