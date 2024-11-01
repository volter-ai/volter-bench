import argparse
import json
import os
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
THRESHOLD = 0.8  # 80%

def get_subdirectories(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def get_branch_directories(benchmark_dir):
    """Get all branch directories for a given benchmark."""
    return [d for d in os.listdir(benchmark_dir) if os.path.isdir(os.path.join(benchmark_dir, d))]

def load_data(data_directory, branch='main'):
    """Load data from the specified branch directory."""
    all_data = []
    branch_path = os.path.join(data_directory, branch)
    
    if not os.path.exists(branch_path):
        print(f"Warning: Branch path {branch_path} does not exist")
        return pd.DataFrame()
        
    for root, dirs, files in os.walk(branch_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path)
                    df['file_timestamp'] = os.path.basename(os.path.dirname(file_path))
                    df['branch'] = branch  # Add branch information
                    all_data.append(df)
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def calculate_overall_success_rate(df):
    total_runs = len(df)
    total_successes = (df['status'] == 'success').sum()
    success_rate = total_successes / total_runs if total_runs > 0 else 0
    return success_rate, total_successes, total_runs

def calculate_agent_ladder_success_rates(df):
    success_rates = df.groupby(['agent_id', 'ladder', 'branch']).agg({
        'status': lambda x: (x == 'success').mean(),
    }).reset_index()
    success_rates.columns = ['agent_id', 'ladder', 'branch', 'success_rate']
    return success_rates

def load_latest_results(benchmark: str | None = None, branch: str = 'main'):
    subdirs = get_subdirectories(DATA_DIR)
    all_data = pd.DataFrame()

    for subdir in subdirs:
        # filter out for a specific benchmark
        if benchmark and subdir != benchmark:
            continue
        data_directory = os.path.join(DATA_DIR, subdir)
        subdir_data = load_data(data_directory, branch)
        if not subdir_data.empty:
            subdir_data['benchmark'] = subdir
            all_data = pd.concat([all_data, subdir_data], ignore_index=True)

    if all_data.empty:
        raise Exception(f"No data found in branch '{branch}' for benchmark '{benchmark}'")

    latest_file_timestamp = all_data['file_timestamp'].max()
    latest_run_data = all_data[all_data['file_timestamp'] == latest_file_timestamp]

    return latest_run_data

def calculate_metrics(df):
    overall_success_rate, total_successes, total_runs = calculate_overall_success_rate(df)

    # Identify the top model based on total successes
    successes_per_agent = df[df['status'] == 'success'].groupby('agent_id').size()
    if not successes_per_agent.empty:
        top_model = successes_per_agent.idxmax()
    else:
        top_model = "N/A"

    latest_timestamp = df['file_timestamp'].iloc[0]
    branch = df['branch'].iloc[0]  # Get branch information

    agent_ladder_success_rates = calculate_agent_ladder_success_rates(df)

    return {
        'overall_success_rate': float(overall_success_rate),
        'total_successes': int(total_successes),
        'total_runs': int(total_runs),
        'top_model': top_model,
        'latest_timestamp': latest_timestamp,
        'branch': branch,
        'agent_ladder_success_rates': agent_ladder_success_rates
    }

def generate_slack_payload(metrics, job_status=None, build_url=None):
    color = "danger" if metrics['overall_success_rate'] < THRESHOLD else "good"
    text = f"Latest Benchmark Results (Branch: {metrics['branch']})"

    numerator = metrics['total_successes']
    denominator = metrics['total_runs']
    fraction_str = f"{numerator}/{denominator}"
    percentage_str = f"{metrics['overall_success_rate']:.2%}"

    fields = [
        {
            "title": "Overall Success Rate",
            "value": f"{percentage_str} ({fraction_str})",
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
            "short": True
        }
    ]

    for _, row in metrics['agent_ladder_success_rates'].iterrows():
        fields.append({
            "title": f"{row['agent_id']} - {row['ladder']} ({row['branch']})",
            "value": f"{row['success_rate']:.2%}",
            "short": True
        })

    if job_status:
        fields.append({
            "title": "Job Status",
            "value": job_status.capitalize(),
            "short": True
        })
    if build_url:
        fields.append({
            "title": "Build URL",
            "value": f"<{build_url}|View Build>",
            "short": False
        })

    return {
        "text": text,
        "attachments": [
            {
                "color": color,
                "fields": fields
            }
        ]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process benchmark results and generate Slack payload.")
    parser.add_argument("--benchmark_name", type=str, default="bench_one_shot_core", help="Name of the benchmark to process")
    parser.add_argument("--branch", type=str, default="main", help="Branch to process (default: main)")
    args = parser.parse_args()

    try:
        job_status = os.getenv('JOB_STATUS')
        build_url = os.getenv('BUILD_URL')

        latest_results = load_latest_results(benchmark=args.benchmark_name, branch=args.branch)
        metrics = calculate_metrics(latest_results)
        slack_payload = generate_slack_payload(metrics, job_status=job_status, build_url=build_url)

        print(json.dumps(slack_payload, indent=2))
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"slack_payload={json.dumps(slack_payload)}\n")
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