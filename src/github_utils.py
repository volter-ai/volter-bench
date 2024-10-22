import os
from pathlib import Path

def get_base_github_url(data_directory):
    """Extract the base GitHub URL based on the data directory structure."""
    parts = Path(data_directory).parts
    try:
        data_index = parts.index('data')
        agent_type = parts[data_index + 1]
        branch = parts[data_index + 2] if len(parts) > data_index + 2 else 'main'
        
        # Use the actual branch name in the GitHub URL
        return f"https://github.com/volter-ai/volter-bench/tree/{branch}/data/{agent_type}/{branch}"
    except ValueError:
        # Fallback to legacy structure
        subdirectory = os.path.basename(data_directory)
        return f"https://github.com/volter-ai/volter-bench/tree/main/data/{subdirectory}"

def get_github_url(row, data_directory):
    """Get GitHub URL for log files."""
    base_url = get_base_github_url(data_directory)
    
    # Format the timestamp to match the GitHub folder structure
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")
    
    # Extract the log file name from the logs path and remove any extra characters
    log_path = row['logs'][0] if isinstance(row['logs'], list) else row['logs']
    log_file = log_path.split('/')[-1].strip("[]'")
    
    # Construct the GitHub URL
    return f"{base_url}/{formatted_timestamp}/new_prompt_logs/{log_file}"

def get_code_github_url(row, data_directory):
    """Get GitHub URL for game code."""
    base_url = get_base_github_url(data_directory)
    
    # Format the timestamp to match the GitHub folder structure
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")
    
    # Include the run number in the ladder path
    code_path = f"ladder/{row['ladder']}_{row['run']}/main_game"
    
    # Construct the full GitHub URL
    return f"{base_url}/{formatted_timestamp}/{code_path}"