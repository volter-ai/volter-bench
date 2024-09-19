# calculations.py

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
