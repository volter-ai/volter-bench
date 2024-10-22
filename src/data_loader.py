import os
import pandas as pd
from datetime import datetime
from pathlib import Path

def get_agent_types(base_dir):
    """Get all agent type directories in the base directory."""
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def get_branches(base_dir, agent_type):
    """Get all branch directories for a given agent type."""
    agent_path = os.path.join(base_dir, agent_type)
    return [d for d in os.listdir(agent_path) if os.path.isdir(os.path.join(agent_path, d))]

def load_data(directory):
    """
    Load data from CSV files in the given directory structure.
    Handles both new structure (data/agent_type/branch_name/*) and legacy structure.
    """
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'results.csv':
                csv_files.append(os.path.join(root, file))
    
    all_data = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            
            # Extract path components
            path_parts = Path(file).parts
            
            # Extract timestamp from the file path (always second to last directory)
            timestamp_dir = path_parts[-2]
            df['file_timestamp'] = datetime.strptime(timestamp_dir, "%Y-%m-%d-%H-%M-%S")
            
            # Extract branch and agent type information
            # Find the index of 'data' in the path
            try:
                data_index = path_parts.index('data')
                if len(path_parts) > data_index + 2:  # If we have enough path components
                    df['agent_type'] = path_parts[data_index + 1]
                    df['branch'] = path_parts[data_index + 2]
                else:
                    # Legacy structure
                    df['agent_type'] = path_parts[data_index + 1]
                    df['branch'] = 'main'  # Default to main for legacy data
            except ValueError:
                # Fallback for cases where 'data' is not in path
                df['agent_type'] = 'unknown'
                df['branch'] = 'main'
            
            all_data.append(df)
        except Exception as e:
            print(f"Error loading file {file}: {e}")
    
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()