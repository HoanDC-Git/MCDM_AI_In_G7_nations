import os
import json
import pandas as pd
import numpy as np

# Resolve base directory (project root) to make paths robust
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_data():
    """
    Loads decision matrix, country names, criteria info, and pillar configuration.
    
    Returns:
        matrix (np.ndarray): The decision matrix (7 countries x 13 criteria).
        alt_names (list): List of country names.
        criteria_ids (list): List of criteria identifiers (e.g., Criteria 1).
        criteria_names (list): List of detailed criteria descriptions.
        types (np.ndarray): Criterion types (1 for Benefit, -1 for Cost/Non-benefit).
        pillars (dict): Mapping from pillar name to list of criterion indices (0-based).
    """
    # 1. Load the decision matrix
    data_path = os.path.join(DATA_DIR, 'processed', 'Data.csv')
    df_data = pd.read_csv(data_path, index_col=0)
    alt_names = df_data.index.tolist()
    matrix = df_data.values.astype(float)
    criteria_ids = df_data.columns.tolist()

    # 2. Load criteria metadata from JSON
    json_path = os.path.join(DATA_DIR, 'raw', 'G7_AI_Impact_Criteria.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        criteria_metadata = json.load(f)

    # 3. Process metadata
    criteria_names = []
    types_list = []
    pillars = {}
    criteria_count = 0

    for item in criteria_metadata:
        c_id = item.get(" ")
        if c_id and str(c_id).strip().startswith("Criteria"):
            criteria_names.append(item["Criteria Name"].strip())
            
            # Benefit vs Non-benefit
            benefit_type = item["Benefit/Non-benefit"].strip().lower()
            if benefit_type == 'benefit':
                types_list.append(1)
            else:
                types_list.append(-1)
            
            # Pillar grouping
            pillar_name = item["Pillar"].strip()
            if pillar_name not in pillars:
                pillars[pillar_name] = []
            pillars[pillar_name].append(criteria_count)
            criteria_count += 1

    types = np.array(types_list, dtype=int)

    return matrix, alt_names, criteria_ids, criteria_names, types, pillars
