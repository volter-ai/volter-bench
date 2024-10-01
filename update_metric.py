import os
import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
THRESHOLD = 0.95

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

def generate_slack_payload(metrics):
    color = "danger" if metrics['overall_success_rate'] < THRESHOLD else "good"
    text = f"<!here> Success rate is below {THRESHOLD:.0%}!" if metrics['overall_success_rate'] < THRESHOLD else "Latest Benchmark Results"
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Latest Benchmark Results"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Overall Success Rate:*\n{metrics['overall_success_rate']:.2%}"},
                {"type": "mrkdwn", "text": f"*Top Model:*\n{metrics['top_model']}"},
                {"type": "mrkdwn", "text": f"*Latest Run Timestamp:*\n{metrics['latest_timestamp']}"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Agent Ladder Success Rates:*"
            }
        }
    ]
    
    for _, row in metrics['agent_ladder_success_rates'].iterrows():
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{row['agent_id']} - {row['ladder']}:* {row['success_rate']:.2%}"
            }
        })
    
    payload = {
        "text": text,
        "blocks": blocks,
        "attachments": [{"color": color}]
    }
    
    return json.dumps(payload)

if __name__ == "__main__":
    try:
        latest_results = load_latest_results()
        metrics = calculate_metrics(latest_results)
        slack_payload = generate_slack_payload(metrics)
        print(f"::set-output name=slack_payload::{slack_payload}")
    except Exception as e:
        error_payload = json.dumps({
            "text": f"Error in update_metrics.py: {str(e)}",
            "blocks": [{
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Error in update_metrics.py: {str(e)}"}
            }]
        })
        print(f"::set-output name=slack_payload::{error_payload}")