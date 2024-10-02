import os
import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
THRESHOLD = 0.8  # 80%

def get_subdirectories(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def load_data(data_directory):
    all_data = []
    for root, dirs, files in os.walk(data_directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                df['file_timestamp'] = os.path.basename(os.path.dirname(file_path))
                all_data.append(df)
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def calculate_success_rates(df):
    success_rates = df.groupby('agent_id').agg({
        'status': lambda x: (x == 'success').mean(),
    }).reset_index()
    success_rates.columns = ['agent_id', 'success_rate']
    return success_rates

def calculate_agent_ladder_success_rates(df):
    success_rates = df.groupby(['agent_id', 'ladder']).agg({
        'status': lambda x: (x == 'success').mean(),
    }).reset_index()
    success_rates.columns = ['agent_id', 'ladder', 'success_rate']
    return success_rates

def load_latest_results():
    subdirs = get_subdirectories(DATA_DIR)
    all_data = pd.DataFrame()
    
    for subdir in subdirs:
        data_directory = os.path.join(DATA_DIR, subdir)
        subdir_data = load_data(data_directory)
        if not subdir_data.empty:
            subdir_data['benchmark'] = subdir
            all_data = pd.concat([all_data, subdir_data], ignore_index=True)
    
    if all_data.empty:
        raise Exception("No data found in any subdirectory")
    
    latest_file_timestamp = all_data['file_timestamp'].max()
    latest_run_data = all_data[all_data['file_timestamp'] == latest_file_timestamp]
    
    return latest_run_data

def calculate_metrics(df):
    overall_success_rates = calculate_success_rates(df)
    overall_success_rate = overall_success_rates['success_rate'].mean()
    top_model = overall_success_rates.loc[overall_success_rates['success_rate'].idxmax(), 'agent_id']
    latest_timestamp = df['file_timestamp'].iloc[0]
    
    agent_ladder_success_rates = calculate_agent_ladder_success_rates(df)
    
    return {
        'overall_success_rate': overall_success_rate,
        'top_model': top_model,
        'latest_timestamp': latest_timestamp,
        'agent_ladder_success_rates': agent_ladder_success_rates
    }

def generate_slack_payload(metrics, job_status=None, build_url=None):
    # Determine the color based on the success rate
    color = "danger" if metrics['overall_success_rate'] < THRESHOLD else "good"
    
    # Text for fallback
    text = f"GitHub Action build result: {job_status}\n{build_url if build_url else ''}"
    
    # Pretext for the attachment
    pretext = "Latest Benchmark Results"
    
    # Construct fields for the attachment
    fields = [
        {
            "title": "Overall Success Rate",
            "value": f"{metrics['overall_success_rate']:.2%}",
            "short": True
        },
        {
            "title": "Top Model",
            "value": metrics['top_model'],
            "short": True
        },
        {
            "title": "Latest Run Timestamp",
            "value": metrics['latest_timestamp'],
            "short": False
        }
    ]
    
    # Add Agent Ladder Success Rates
    for _, row in metrics['agent_ladder_success_rates'].iterrows():
        fields.append({
            "title": f"{row['agent_id']} - {row['ladder']}",
            "value": f"{row['success_rate']:.2%}",
            "short": True
        })
    
    # Append additional information if available
    additional_fields = []
    if job_status:
        additional_fields.append({
            "title": "Job Status",
            "value": job_status.capitalize(),
            "short": True
        })
    if build_url:
        additional_fields.append({
            "title": "Build URL",
            "value": f"<{build_url}|View Build>",
            "short": False
        })
    fields.extend(additional_fields)
    
    # Construct the payload
    payload = {
        "text": text,
        "attachments": [
            {
                "pretext": pretext,
                "color": color,
                "fields": fields
            }
        ]
    }
    
    return payload

if __name__ == "__main__":
    try:
        latest_results = load_latest_results()
        metrics = calculate_metrics(latest_results)
        
        # Capture GitHub Actions environment variables for job status and build URL
        job_status = os.getenv('JOB_STATUS', 'success')  # Default to 'success' if not set
        build_url = os.getenv('BUILD_URL', '')
        
        slack_payload = generate_slack_payload(metrics, job_status, build_url)
        
        # Write the output to GITHUB_OUTPUT
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            # Use json.dumps to serialize the payload
            f.write(f"{json.dumps(slack_payload)}")
    except Exception as e:
        error_payload = {
            "text": f"Error in update_metrics.py: {str(e)}",
            "attachments": [
                {
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Error",
                            "value": f"```\n{str(e)}\n```",
                            "short": False
                        }
                    ]
                }
            ]
        }
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"slack_payload={json.dumps(error_payload)}\n")
