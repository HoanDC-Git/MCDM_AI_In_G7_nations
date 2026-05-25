import os
import numpy as np
import pandas as pd
from data_loader import load_data, BASE_DIR
from mcdm_solver import calculate_critic_weights, calculate_topsis

def run_pillar_analysis():
    print("--- Executing Pillar Analysis ---")
    
    # 1. Load data
    matrix, alt_names, criteria_ids, criteria_names, types, pillars = load_data()
    
    # Define output directories
    output_excel_dir = os.path.join(BASE_DIR, 'outputs', 'excel')
    output_csv_dir = os.path.join(BASE_DIR, 'outputs', 'csv', 'analysis')
    
    os.makedirs(output_excel_dir, exist_ok=True)
    os.makedirs(output_csv_dir, exist_ok=True)
    
    # 2. Compute CRITIC weights and Overall TOPSIS score
    weights_critic, _, _, _, _, _ = calculate_critic_weights(matrix, types)
    overall_scores, _, _, _, _, _, _ = calculate_topsis(matrix, weights_critic, types)
    
    # Prepare overall dataframe
    overall_df = pd.DataFrame({
        'Country': alt_names,
        'Overall Score': overall_scores
    }).sort_values(by='Overall Score', ascending=False)
    overall_df['Overall Rank'] = range(1, len(overall_df) + 1)
    overall_df.set_index('Country', inplace=True)
    
    # 3. Analyze each pillar separately
    pillar_rankings = {}
    
    print("Analyzing G7 ranking within each Pillar...")
    for pillar_name, criteria_indices in pillars.items():
        # Subset matrix, weights, types for current pillar
        sub_matrix = matrix[:, criteria_indices]
        sub_weights = weights_critic[criteria_indices]
        sub_types = types[criteria_indices]
        
        # Re-normalize weights so that they sum to 1.0 within the pillar
        sum_sub_weights = np.sum(sub_weights)
        if sum_sub_weights > 0:
            norm_sub_weights = sub_weights / sum_sub_weights
        else:
            norm_sub_weights = np.ones_like(sub_weights) / len(sub_weights)
            
        # Run TOPSIS on this pillar's subset
        pillar_scores, _, _, _, _, _, _ = calculate_topsis(sub_matrix, norm_sub_weights, sub_types)
        
        # Create DataFrame
        pillar_df = pd.DataFrame({
            'Country': alt_names,
            f'{pillar_name} Score': pillar_scores
        }).sort_values(by=f'{pillar_name} Score', ascending=False)
        pillar_df[f'{pillar_name} Rank'] = range(1, len(pillar_df) + 1)
        pillar_df.set_index('Country', inplace=True)
        
        pillar_rankings[pillar_name] = pillar_df
        
    # 4. Join overall dashboard with pillar dashboards
    # Sort final dashboard by Overall Rank
    final_dashboard = overall_df.copy()
    for pillar_name, pillar_df in pillar_rankings.items():
        final_dashboard = final_dashboard.join(pillar_df)
        
    # Re-order columns: Overall Rank, Overall Score, then Pillar Rank, Pillar Score
    final_dashboard = final_dashboard.sort_index() # Sort by country name first to match original structure
    columns_ordered = ['Overall Rank', 'Overall Score']
    for pillar_name in pillars.keys():
        columns_ordered.extend([f'{pillar_name} Rank', f'{pillar_name} Score'])
    final_dashboard = final_dashboard[columns_ordered]
    
    # 5. Export results to Excel and CSV
    excel_path = os.path.join(output_excel_dir, 'Pillar_Analysis_Results.xlsx')
    
    print("Writing Pillar Analysis results...")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        final_dashboard.round(4).to_excel(writer, sheet_name='Pillar_Dashboard')
        # Save individual CSV dashboard
        final_dashboard.round(4).to_csv(os.path.join(output_csv_dir, 'Pillar_Dashboard.csv'))
        
        for pillar_name, pillar_df in pillar_rankings.items():
            sheet_name = f'Rank_{pillar_name.replace(" ", "_")}'
            # Write to Excel
            pillar_df.sort_index().round(4).to_excel(writer, sheet_name=sheet_name)
            # Write to CSV
            csv_filename = f'Rank_{pillar_name.replace(" ", "_")}.csv'
            pillar_df.sort_index().round(4).to_csv(os.path.join(output_csv_dir, csv_filename))
            
    # Set pandas display settings for console output
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    print("\n==== PILLAR ANALYSIS SUMMARY DASHBOARD ====")
    print(final_dashboard.round(4))
    print("============================================\n")
    print(f"Pillar analysis results saved to Excel: '{excel_path}' and CSVs in '{output_csv_dir}'\n")

if __name__ == '__main__':
    run_pillar_analysis()
