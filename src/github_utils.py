import os
from pathlib import Path

def sanitize_branch_name(branch):
    """Convert GitHub branch name to filesystem-safe format."""
    return branch.replace('/', '-')

def get_base_github_url(data_directory, branch=None):
    """Extract the base GitHub URL based on the data directory structure."""
    parts = Path(data_directory).parts
    try:
        data_index = parts.index('data')
        agent_type = parts[data_index + 1]
        
        # Always use 'main' in the tree path, but include sanitized branch name in the data path
        sanitized_branch = sanitize_branch_name(branch) if branch else 'main'
        return f"https://github.com/volter-ai/volter-bench/tree/main/data/{agent_type}/{sanitized_branch}"
    except ValueError:
        subdirectory = os.path.basename(data_directory)
        return f"https://github.com/volter-ai/volter-bench/tree/main/data/{subdirectory}"

def get_github_url(row, data_directory):
    """Get GitHub URL for log files."""
    branch = row.get('branch', 'main')
    base_url = get_base_github_url(data_directory, branch)
    
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")
    
    log_path = row['logs'][0] if isinstance(row['logs'], list) else row['logs']
    log_file = log_path.split('/')[-1].strip("[]'")
    
    return f"{base_url}/{formatted_timestamp}/new_prompt_logs/{log_file}"

def get_code_github_url(row, data_directory):
    """Get GitHub URL for game code."""
    branch = row.get('branch', 'main')
    base_url = get_base_github_url(data_directory, branch)
    
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")
    code_path = f"ladder/{row['ladder']}_{row['run']}/main_game"
    
    return f"{base_url}/{formatted_timestamp}/{code_path}"