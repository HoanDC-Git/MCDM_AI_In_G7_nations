import os
import numpy as np
import pandas as pd
from data_loader import load_data, BASE_DIR
from mcdm_solver import calculate_critic_weights, calculate_topsis

def run_scenario_analysis():
    print("--- Executing Scenario Analysis ---")
    
    # 1. Load data
    matrix, alt_names, criteria_ids, criteria_names, types, pillars = load_data()
    
    # Define output directories
    output_excel_dir = os.path.join(BASE_DIR, 'outputs', 'excel')
    output_csv_dir = os.path.join(BASE_DIR, 'outputs', 'csv', 'scenario')
    
    os.makedirs(output_excel_dir, exist_ok=True)
    os.makedirs(output_csv_dir, exist_ok=True)
    
    # 2. Calculate original CRITIC weights
    original_critic_weights, _, _, _, _, _ = calculate_critic_weights(matrix, types)
    
    # 3. Define scenarios
    scenarios = {
        "Economy First": {
            "Economic Impact": 0.50,
            "Social Impact": 0.20,
            "Policy & Governance": 0.15,
            "Tech Readiness": 0.15
        },
        "Social First": {
            "Economic Impact": 0.20,
            "Social Impact": 0.50,
            "Policy & Governance": 0.15,
            "Tech Readiness": 0.15
        },
        "Balanced": {
            "Economic Impact": 0.25,
            "Social Impact": 0.25,
            "Policy & Governance": 0.25,
            "Tech Readiness": 0.25
        }
    }
    
    # Add Original CRITIC scenario for comparison
    # Calculate sum of CRITIC weights for each pillar to set target weights
    scenarios['Original CRITIC'] = {
        p: float(np.sum(original_critic_weights[indices])) for p, indices in pillars.items()
    }
    
    # Create Excel writer
    excel_path = os.path.join(output_excel_dir, 'Scenario_Analysis_Results.xlsx')
    writer = pd.ExcelWriter(excel_path, engine='openpyxl')
    
    all_rankings = {}
    
    # 4. Calculate ranking for each scenario
    for scenario_name, pillar_targets in scenarios.items():
        print(f"Calculating for scenario: {scenario_name}...")
        
        # Build weight vector for current scenario
        scenario_weights = np.zeros_like(original_critic_weights)
        for pillar_name, target_weight in pillar_targets.items():
            indices = pillars[pillar_name]
            original_sum = np.sum(original_critic_weights[indices])
            
            # Distribute target weight to criteria proportional to original CRITIC weights
            if original_sum > 0:
                scenario_weights[indices] = (original_critic_weights[indices] / original_sum) * target_weight
            else:
                # Fallback if sum is 0
                scenario_weights[indices] = target_weight / len(indices)
                
        # Run TOPSIS with scenario weights
        scores, _, _, _, _, _, _ = calculate_topsis(matrix, scenario_weights, types)
        
        # Create DataFrame
        results_df = pd.DataFrame({
            'Country': alt_names,
            'Score': scores
        })
        results_df_sorted = results_df.sort_values(by='Score', ascending=False).copy()
        results_df_sorted['Rank'] = range(1, len(results_df_sorted) + 1)
        
        # Save scenario results
        # Write to Excel sheet
        results_df_sorted.round(4).to_excel(writer, sheet_name=scenario_name, index=False)
        # Write to CSV file
        results_df_sorted.round(4).to_csv(os.path.join(output_csv_dir, f'{scenario_name}.csv'), index=False)
        
        # Record rankings for final comparison (indexed by Country)
        all_rankings[scenario_name] = results_df_sorted.set_index('Country')['Rank']
        
    # 5. Generate and save summary comparison table
    summary_df = pd.DataFrame(all_rankings)
    summary_df = summary_df.sort_index() # Sort by country name alphabetically
    
    # Save comparison table
    summary_df.to_excel(writer, sheet_name='Summary_Comparison')
    summary_df.to_csv(os.path.join(output_csv_dir, 'Summary_Comparison.csv'))
    
    writer.close()
    
    print("\n==== SCENARIO RANKING COMPARISON SUMMARY ====")
    print(summary_df)
    print("=============================================\n")
    print(f"Scenario analysis results saved to Excel: '{excel_path}' and CSVs in '{output_csv_dir}'\n")

if __name__ == '__main__':
    run_scenario_analysis()
