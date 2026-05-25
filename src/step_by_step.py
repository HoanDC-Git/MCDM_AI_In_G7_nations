import os
import numpy as np
import pandas as pd
from data_loader import load_data, BASE_DIR
from mcdm_solver import calculate_critic_weights, calculate_topsis

def run_step_by_step():
    print("--- Executing Step-by-Step CRITIC-TOPSIS Pipeline ---")
    
    # 1. Load data dynamically
    matrix, alt_names, criteria_ids, criteria_names, types, pillars = load_data()
    
    # Define output paths
    output_excel_dir = os.path.join(BASE_DIR, 'outputs', 'excel')
    output_csv_dir = os.path.join(BASE_DIR, 'outputs', 'csv', 'steps')
    
    os.makedirs(output_excel_dir, exist_ok=True)
    os.makedirs(output_csv_dir, exist_ok=True)
    
    excel_path = os.path.join(output_excel_dir, 'CRITIC_TOPSIS_Methodology_Steps.xlsx')
    writer = pd.ExcelWriter(excel_path, engine='openpyxl')
    
    # 2. Run CRITIC Weights
    print("Computing CRITIC Weights...")
    weights, critic_norm, std_devs, corr_matrix, conflict, info_c = calculate_critic_weights(matrix, types)
    
    # 3. Run TOPSIS
    print("Computing TOPSIS Rankings...")
    scores, topsis_norm, weighted_matrix, pis, nis, dist_pis, dist_nis = calculate_topsis(matrix, weights, types)
    
    # --- Prepare DataFrames for exporting ---
    
    # Step 1: Initial Data Matrix
    df1 = pd.DataFrame(matrix, index=alt_names, columns=criteria_ids)
    df1.to_excel(writer, sheet_name='1_Initial_Data_Matrix')
    df1.to_csv(os.path.join(output_csv_dir, '1_Initial_Data_Matrix.csv'))
    
    # Step 2: CRITIC Normalized Matrix
    df2 = pd.DataFrame(critic_norm, index=alt_names, columns=criteria_ids)
    df2.to_excel(writer, sheet_name='2_CRITIC_Normalized_Matrix')
    df2.to_csv(os.path.join(output_csv_dir, '2_CRITIC_Normalized_Matrix.csv'))
    
    # Step 3: CRITIC Correlation Matrix
    df3 = pd.DataFrame(corr_matrix, index=criteria_ids, columns=criteria_ids)
    df3.to_excel(writer, sheet_name='3_CRITIC_Correlation_Matrix')
    df3.to_csv(os.path.join(output_csv_dir, '3_CRITIC_Correlation_Matrix.csv'))
    
    # Step 4: CRITIC Weights Calculation
    df4 = pd.DataFrame({
        'Standard Deviation': std_devs,
        'Conflict (Sum(1-r))': conflict,
        'Information (C)': info_c,
        'CRITIC Weights': weights
    }, index=criteria_ids)
    df4.to_excel(writer, sheet_name='4_CRITIC_Weights_Calculation')
    df4.to_csv(os.path.join(output_csv_dir, '4_CRITIC_Weights_Calculation.csv'))
    
    # Step 5: TOPSIS Normalized Matrix
    df5 = pd.DataFrame(topsis_norm, index=alt_names, columns=criteria_ids)
    df5.to_excel(writer, sheet_name='5_TOPSIS_Normalized_Matrix')
    df5.to_csv(os.path.join(output_csv_dir, '5_TOPSIS_Normalized_Matrix.csv'))
    
    # Step 6: TOPSIS Weighted Matrix
    df6 = pd.DataFrame(weighted_matrix, index=alt_names, columns=criteria_ids)
    df6.to_excel(writer, sheet_name='6_TOPSIS_Weighted_Matrix')
    df6.to_csv(os.path.join(output_csv_dir, '6_TOPSIS_Weighted_Matrix.csv'))
    
    # Step 7: TOPSIS Ideal Solutions (PIS / NIS)
    df7 = pd.DataFrame({'Ideal Solution (PIS)': pis, 'Negative Ideal (NIS)': nis}, index=criteria_ids)
    df7.to_excel(writer, sheet_name='7_TOPSIS_Ideal_Solutions')
    df7.to_csv(os.path.join(output_csv_dir, '7_TOPSIS_Ideal_Solutions.csv'))
    
    # Step 8: TOPSIS Separation Measures
    df8 = pd.DataFrame({
        'Distance to PIS (S+)': dist_pis,
        'Distance to NIS (S-)': dist_nis,
        'Closeness Coefficient (Score)': scores
    }, index=alt_names)
    df8.to_excel(writer, sheet_name='8_TOPSIS_Separation_Measures')
    df8.to_csv(os.path.join(output_csv_dir, '8_TOPSIS_Separation_Measures.csv'))
    
    # Step 9: Final Ranking
    df9 = pd.DataFrame({
        'Country': alt_names,
        'TOPSIS Score': scores
    })
    df9_sorted = df9.sort_values(by='TOPSIS Score', ascending=False).copy()
    df9_sorted['Rank'] = range(1, len(df9_sorted) + 1)
    
    # Save sorted for viewing and printing
    print("\n==== FINAL RANKING (CRITIC-TOPSIS) ====")
    print(df9_sorted.to_string(index=False))
    print("=======================================\n")
    
    # Save ranking sorted by Country to keep consistent index, but also write sorted version
    # The original StepByStep.py sorted by Country when saving to excel, but kept Rank column correct
    final_df_to_save = df9_sorted.sort_values(by='Country')
    final_df_to_save.to_excel(writer, sheet_name='9_Final_Ranking', index=False)
    
    # Let's save both versions in CSV for convenience: sorted by rank, and sorted by country name
    # The original 9_Final_Ranking.csv was sorted by Rank! Let's check G7_Ranking_BubbleMap_Custom which reads Country
    # Wait, the original DataVisualizeCircle.py reads 'Country' and merges, so sorting doesn't affect merge, but order in CSV might be good.
    # Let's write the rank-sorted file to CSV as 9_Final_Ranking.csv
    df9_sorted.to_csv(os.path.join(output_csv_dir, '9_Final_Ranking.csv'), index=False)
    
    writer.close()
    print(f"All steps exported successfully to Excel: '{excel_path}' and CSVs in '{output_csv_dir}'\n")

if __name__ == '__main__':
    run_step_by_step()
