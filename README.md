# G7 AI Impact Evaluation using MCDM (CRITIC-TOPSIS)

This repository contains a **Decision Science** project evaluating and ranking the impact of Artificial Intelligence (AI) on the G7 nations (**Canada, France, Germany, Italy, Japan, United Kingdom, United States**). 

The evaluation uses a Multiple-Criteria Decision-Making (**MCDM**) approach combining the **CRITIC** method for objective weight calculation with the **TOPSIS** method for final ranking.

---

## 📌 Project Overview

AI is reshaping global economies and societies. This project assesses G7 countries across **13 key criteria** grouped into **4 analytical pillars**:

1. **Economic Impact**: AI investment, startup creation, labor productivity growth, and job risk of automation.
2. **Social Impact**: Employment in digital-intensive sectors, income inequality (Gini), and AI adoption in public healthcare.
3. **Policy & Governance**: Maturity of national AI strategy, privacy laws, and government AI readiness index.
4. **Tech Readiness**: Fixed broadband speed, AI research publication rates, and SME adoption of AI.

---

## 🛠️ Methodology

### 1. CRITIC (Criteria Importance Through Intercriteria Correlation)
CRITIC is an objective weighting method that determines criteria importance by examining:
* **Contrast intensity**: Measured by the standard deviation of normalized criterion values.
* **Conflict between criteria**: Measured by the correlation coefficient between criteria.
Criteria with higher standard deviations and lower correlations with others are assigned larger weights.

### 2. TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
TOPSIS ranks alternatives based on their geometric distance in a normalized vector space:
* **Positive Ideal Solution (PIS)**: The best possible values across all benefit criteria and worst for cost criteria.
* **Negative Ideal Solution (NIS)**: The worst possible values across all benefit criteria and best for cost criteria.
Alternatives are ranked by their **closeness coefficient**, indicating how close they are to PIS and how far from NIS.

---

## 📂 Directory Structure

The repository is organized as follows:

```text
MCDM-G7-AI-Impact/
├── data/                             # Data files
│   ├── raw/                          # Raw datasets
│   │   ├── G7_AI_Impact_Data.xlsx    # Principal spreadsheet containing all G7 data
│   │   └── G7_AI_Impact_Criteria.json # JSON file defining criteria parameters
│   └── processed/                    # Extracted CSV datasets for scripting
│       ├── Criteria.csv              # Definitions, types, and pillars of criteria
│       ├── Data.csv                  # The G7 decision matrix (raw values)
│       └── Data_Permuted.csv         # Permuted G7 data
│
├── src/                              # Python source scripts
│   ├── data_loader.py                # Helper script to load data and criteria settings dynamically
│   ├── mcdm_solver.py                # Generic CRITIC and TOPSIS calculation engine
│   ├── step_by_step.py               # Computes and logs detailed intermediate steps of calculations
│   ├── analysis.py                   # Computes rankings within each individual Pillar
│   ├── scenario_analysis.py          # Sensitivity analysis across weight allocation scenarios
│   ├── visualization.py              # Generates geographic heatmap and bubble map figures
│   └── excel_to_json.py              # Utility to extract Excel sheets to CSV/JSON files
│
├── outputs/                          # Calculated outputs (committed sample results)
│   ├── csv/                          # Intermediate and final CSV tables
│   │   ├── steps/                    # Detailed calculation matrix sheets
│   │   ├── analysis/                 # Pillar-specific scores
│   │   └── scenario/                 # Sensitivity results for different weight scenarios
│   ├── excel/                        # Consolidated Excel reports (.xlsx)
│   │   ├── CRITIC_TOPSIS_Methodology_Steps.xlsx
│   │   ├── Pillar_Analysis_Results.xlsx
│   │   └── Scenario_Analysis_Results.xlsx
│   └── figures/                      # Generated analytical map plots (.png)
│       ├── G7_AI_Investment_Map.png
│       ├── G7_AI_Share_of_Jobs_Map.png
│       └── G7_Ranking_BubbleMap_Custom.png
│
├── docs/                             # Project documentation and papers
│   ├── Figures_Description.docx      # Narrative notes on data visualization
│   └── report_AI_in_G7_nations_MCDM.pdf  # Formal academic report
│
├── run_all.py                        # Master pipeline script to execute everything sequentially
├── .gitignore                        # Files to ignore in git commits
└── requirements.txt                  # Python package dependencies
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/MCDM-G7-AI-Impact.git
   cd MCDM-G7-AI-Impact
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

To execute the entire calculation pipeline (data extraction, step-by-step math, pillar analysis, scenario sensitivity analysis, and plotting G7 maps) with a single command, run the master script:

```bash
python run_all.py
```

### Running Individual Components

You can also run specific scripts under `src/` to focus on particular analysis components:

* **Calculate step-by-step CRITIC-TOPSIS matrices**:
  ```bash
  python src/step_by_step.py
  ```
  Generates `CRITIC_TOPSIS_Methodology_Steps.xlsx` and CSV tables under `outputs/csv/steps/`.

* **Calculate G7 performance within specific pillars**:
  ```bash
  python src/analysis.py
  ```
  Generates `Pillar_Analysis_Results.xlsx` and CSV dashboards under `outputs/csv/analysis/`.

* **Simulate G7 rankings under different policy weighting scenarios**:
  ```bash
  python src/scenario_analysis.py
  ```
  Simulates "Economy First", "Social First", and "Balanced" weight distributions and saves results to `outputs/excel/Scenario_Analysis_Results.xlsx` and `outputs/csv/scenario/`.

* **Replot map visualizations**:
  ```bash
  python src/visualization.py
  ```
  Downloads G7 geographic features and regenerates PNG maps in `outputs/figures/`.
# MCDM_AI_In_G7_nations
# MCDM_AI_In_G7_nations
