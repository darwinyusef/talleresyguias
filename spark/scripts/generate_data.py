import pandas as pd
import numpy as np
import os

def generate_leads_data(n=1000):
    np.random.seed(42)
    data = {
        'id': range(1, n + 1),
        'age': np.random.randint(18, 70, n),
        'salary': np.random.randint(20000, 150000, n),
        'web_visits': np.random.randint(1, 50, n),
        'last_action': np.random.choice(['email_click', 'form_submit', 'web_view', 'nothing'], n),
        'converted': np.random.choice([0, 1], n, p=[0.7, 0.3]) # Target
    }
    df = pd.DataFrame(data)
    
    # Create directory if not exists
    os.makedirs('data', exist_ok=True)
    
    file_path = 'data/lead_conversions.csv'
    df.to_csv(file_path, index=False)
    print(f"Dataset generado: {file_path} con {n} registros.")

if __name__ == "__main__":
    generate_leads_data()
