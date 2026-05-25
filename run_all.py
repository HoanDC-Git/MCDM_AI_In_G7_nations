import os
import sys

# Ensure src directory is in the Python search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from excel_to_json import extract_excel_sheets
from step_by_step import run_step_by_step
from analysis import run_pillar_analysis
from scenario_analysis import run_scenario_analysis
from visualization import run_visualization

def main():
    print("======================================================================")
    print("         MCDM G7 AI IMPACT - INTEGRATED WORKFLOW RUNNER")
    print("======================================================================\n")
    
    try:
        # Step 1: Data extraction from Excel to CSV/JSON
        print("[STEP 1/5] Extracting raw data sheets...")
        extract_excel_sheets()
        print("Step 1 completed.\n")
        
        # Step 2: Run CRITIC-TOPSIS Step-by-Step methodology
        print("[STEP 2/5] Running CRITIC-TOPSIS Step-by-Step calculations...")
        run_step_by_step()
        print("Step 2 completed.\n")
        
        # Step 3: Run Pillar Analysis (Economic, Social, Policy, Tech Readiness)
        print("[STEP 3/5] Running Pillar Analysis...")
        run_pillar_analysis()
        print("Step 3 completed.\n")
        
        # Step 4: Run Scenario Analysis (Sensitivity simulation)
        print("[STEP 4/5] Running Scenario Analysis...")
        run_scenario_analysis()
        print("Step 4 completed.\n")
        
        # Step 5: Run Data Visualization map generation
        print("[STEP 5/5] Generating G7 map visualizations...")
        run_visualization()
        print("Step 5 completed.\n")
        
        print("======================================================================")
        print("  CONGRATULATIONS! ALL MCDM CALCULATIONS AND ANALYSIS FINISHED")
        print("  All data outputs have been successfully saved into 'outputs/'")
        print("======================================================================")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
