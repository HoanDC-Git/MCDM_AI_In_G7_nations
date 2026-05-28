import os
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_data, BASE_DIR

def run_visualization():
    print("--- Executing Data Visualization Maps and Professional Charts ---")
    
    # 1. Paths configuration
    output_fig_dir = os.path.join(BASE_DIR, 'outputs', 'figures')
    processed_data_dir = os.path.join(BASE_DIR, 'data', 'processed')
    steps_csv_dir = os.path.join(BASE_DIR, 'outputs', 'csv', 'steps')
    
    os.makedirs(output_fig_dir, exist_ok=True)

    # =========================================================================
    # OFFLINE CHART 1: G7 Final Rankings and TOPSIS Scores (Horizontal Bar)
    # =========================================================================
    ranking_csv_path = os.path.join(steps_csv_dir, '9_Final_Ranking.csv')
    if os.path.exists(ranking_csv_path):
        print("Generating Chart: Overall Rankings...")
        df_rank = pd.read_csv(ranking_csv_path)
        df_rank_sorted = df_rank.sort_values(by='TOPSIS Score', ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 5.5))
        # Premium blue gradient palette
        colors = plt.cm.Blues(np.linspace(0.4, 0.85, len(df_rank_sorted)))
        
        bars = ax.barh(df_rank_sorted['Country'], df_rank_sorted['TOPSIS Score'], color=colors, height=0.6, edgecolor='none')
        
        # Grid lines
        ax.xaxis.grid(True, linestyle='--', alpha=0.6, color='#cbd5e1')
        ax.set_axisbelow(True)
        
        # Style spines
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['left'].set_color('#94a3b8')
        ax.spines['bottom'].set_color('#94a3b8')
        ax.tick_params(colors='#475569', labelsize=11)
        
        # Annotate scores and ranks
        for i, bar in enumerate(bars):
            width = bar.get_width()
            y_val = bar.get_y() + bar.get_height()/2
            row = df_rank_sorted.iloc[i]
            ax.text(width + 0.015, y_val, f"{width:.4f} (Rank #{int(row['Rank'])})", 
                    va='center', ha='left', fontsize=11, color='#1e293b', fontweight='bold')
            
        ax.set_xlabel('TOPSIS Closeness Coefficient (Higher is Better)', fontsize=12, labelpad=12, color='#1e293b', fontweight='semibold')
        ax.set_title('Overall G7 AI Impact Evaluation (CRITIC-TOPSIS)', fontsize=15, pad=20, color='#0f172a', fontweight='bold')
        ax.set_xlim(0, 0.8)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_fig_dir, 'G7_Final_Rankings.png'), dpi=300)
        plt.close()

    # =========================================================================
    # OFFLINE CHART 2: CRITIC Criteria Weights (Horizontal Bar by Pillar)
    # =========================================================================
    weights_csv_path = os.path.join(steps_csv_dir, '4_CRITIC_Weights_Calculation.csv')
    if os.path.exists(weights_csv_path):
        print("Generating Chart: CRITIC Criteria Weights...")
        df_weights = pd.read_csv(weights_csv_path, index_col=0)
        df_weights = df_weights.dropna(subset=['CRITIC Weights'])
        
        matrix, alt_names, criteria_ids, criteria_names, types, pillars = load_data()
        
        criteria_list = []
        for i in range(len(criteria_ids)):
            c_id = criteria_ids[i]
            c_name = criteria_names[i]
            c_weight = df_weights.loc[c_id, 'CRITIC Weights']
            
            c_pillar = ""
            for p_name, indices in pillars.items():
                if i in indices:
                    c_pillar = p_name
                    break
            criteria_list.append({
                'ID': c_id,
                'Name': c_name,
                'Weight': c_weight,
                'Pillar': c_pillar
            })
        
        df_plot_weights = pd.DataFrame(criteria_list)
        df_plot_weights_sorted = df_plot_weights.sort_values(by='Weight', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 7.5))
        
        # Color palette by pillar
        pillar_colors = {
            'Economic Impact': '#2563eb',     # Blue
            'Social Impact': '#10b981',       # Emerald Green
            'Policy & Governance': '#d97706',  # Amber
            'Tech Readiness': '#7c3aed'       # Purple
        }
        
        bar_colors = [pillar_colors[row['Pillar']] for _, row in df_plot_weights_sorted.iterrows()]
        
        bars = ax.barh(df_plot_weights_sorted['Name'], df_plot_weights_sorted['Weight'], color=bar_colors, height=0.6, edgecolor='none')
        
        # Grid lines
        ax.xaxis.grid(True, linestyle='--', alpha=0.6, color='#cbd5e1')
        ax.set_axisbelow(True)
        
        # Style spines
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['left'].set_color('#94a3b8')
        ax.spines['bottom'].set_color('#94a3b8')
        ax.tick_params(colors='#475569', labelsize=10)
        
        # Annotate weights
        for bar in bars:
            width = bar.get_width()
            y_val = bar.get_y() + bar.get_height()/2
            ax.text(width + 0.003, y_val, f"{width*100:.2f}%", 
                    va='center', ha='left', fontsize=10, color='#1e293b', fontweight='bold')
            
        ax.set_xlabel('Weight Contribution (CRITIC)', fontsize=12, labelpad=12, color='#1e293b', fontweight='semibold')
        ax.set_title('CRITIC Criteria Weighting: Key Indicators of AI Impact', fontsize=15, pad=20, color='#0f172a', fontweight='bold')
        ax.set_xlim(0, 0.17)
        
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=pillar) for pillar, color in pillar_colors.items()]
        ax.legend(handles=legend_elements, loc='lower right', title='Pillars', frameon=True, fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_fig_dir, 'CRITIC_Criteria_Weights.png'), dpi=300)
        plt.close()

    # =========================================================================
    # OFFLINE CHART 3: Pillar Performance Heatmap (Countries vs Pillars)
    # =========================================================================
    analysis_csv_path = os.path.join(BASE_DIR, 'outputs', 'csv', 'analysis', 'Pillar_Dashboard.csv')
    if os.path.exists(analysis_csv_path):
        print("Generating Chart: Pillar Performance Heatmap...")
        df_pillar = pd.read_csv(analysis_csv_path)
        df_pillar_sorted = df_pillar.sort_values(by='Overall Rank')
        
        countries = df_pillar_sorted['Country'].tolist()
        pillars_list = ['Economic Impact', 'Social Impact', 'Policy & Governance', 'Tech Readiness']
        
        score_matrix = []
        for _, row in df_pillar_sorted.iterrows():
            scores = [
                row['Economic Impact Score'],
                row['Social Impact Score'],
                row['Policy & Governance Score'],
                row['Tech Readiness Score']
            ]
            score_matrix.append(scores)
            
        score_matrix = np.array(score_matrix)
        
        fig, ax = plt.subplots(figsize=(10, 6.5))
        im = ax.imshow(score_matrix, cmap='YlGnBu', aspect='auto', vmin=0, vmax=1)
        
        ax.set_xticks(np.arange(len(pillars_list)))
        ax.set_yticks(np.arange(len(countries)))
        
        ax.set_xticklabels(pillars_list, fontsize=11, color='#1e293b', fontweight='semibold')
        ax.set_yticklabels(countries, fontsize=11, color='#1e293b', fontweight='semibold')
        
        plt.setp(ax.get_xticklabels(), rotation=15, ha="right", rotation_mode="anchor")
        
        # Annotate score text inside cells
        for i in range(len(countries)):
            for j in range(len(pillars_list)):
                score = score_matrix[i, j]
                text_color = "white" if score > 0.6 else "black"
                ax.text(j, i, f"{score:.4f}", ha="center", va="center", color=text_color, fontweight='bold', fontsize=11)
                
        cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
        cbar.ax.set_ylabel("Normalized TOPSIS Score", rotation=-90, va="bottom", fontsize=11, fontweight='semibold', labelpad=10)
        cbar.ax.tick_params(labelsize=10)
        
        ax.set_title("Pillar-wise Performance Comparison (G7 Nations)", fontsize=15, pad=20, color='#0f172a', fontweight='bold')
        
        for edge in ['top', 'bottom', 'left', 'right']:
            ax.spines[edge].set_visible(False)
            
        plt.tight_layout()
        plt.savefig(os.path.join(output_fig_dir, 'G7_Pillar_Performance_Heatmap.png'), dpi=300)
        plt.close()

    # =========================================================================
    # OFFLINE CHART 4: Scenario Sensitivity Ranks (Line Plot)
    # =========================================================================
    scenario_csv_path = os.path.join(BASE_DIR, 'outputs', 'csv', 'scenario', 'Summary_Comparison.csv')
    if os.path.exists(scenario_csv_path):
        print("Generating Chart: Scenario Sensitivity Analysis...")
        df_scenario = pd.read_csv(scenario_csv_path)
        if 'Country' in df_scenario.columns:
            df_scenario.set_index('Country', inplace=True)
        elif 'Unnamed: 0' in df_scenario.columns:
            df_scenario.rename(columns={'Unnamed: 0': 'Country'}, inplace=True)
            df_scenario.set_index('Country', inplace=True)
            
        scenarios_cols = ['Original CRITIC', 'Balanced', 'Economy First', 'Social First']
        scenarios_cols = [col for col in scenarios_cols if col in df_scenario.columns]
        
        df_scenario = df_scenario[scenarios_cols]
        
        fig, ax = plt.subplots(figsize=(10, 5.5))
        
        g7_colors = {
            'Canada': '#e6194b', 
            'France': '#3cb44b', 
            'Germany': '#ffe119', 
            'Italy': '#4363d8', 
            'Japan': '#f58231', 
            'United Kingdom': '#911eb4', 
            'United States': '#46f0f0'
        }
        
        markers = {'Canada': 'o', 'France': 's', 'Germany': '^', 'Italy': 'D', 'Japan': 'v', 'United Kingdom': 'p', 'United States': 'X'}
        
        for country in df_scenario.index:
            y_ranks = df_scenario.loc[country, scenarios_cols].values
            color = g7_colors.get(country, '#4b5563')
            marker = markers.get(country, 'o')
            
            # Contrast tuning for visibility on white background
            if country == 'United States':
                color = '#0891b2'
            elif country == 'Germany':
                color = '#b58900'
                
            ax.plot(scenarios_cols, y_ranks, label=country, color=color, marker=marker, linewidth=2.5, markersize=8)
            
            # Label on ends
            ax.text(len(scenarios_cols)-0.95, y_ranks[-1], f" {country} ({y_ranks[-1]})", 
                    va='center', ha='left', color=color, fontweight='semibold', fontsize=10)
            ax.text(-0.05, y_ranks[0], f"({y_ranks[0]}) ", 
                    va='center', ha='right', color=color, fontweight='semibold', fontsize=10)
            
        ax.set_ylim(7.5, 0.5)
        ax.set_yticks(range(1, 8))
        
        ax.set_ylabel('G7 Country Rank', fontsize=12, labelpad=12, color='#1e293b', fontweight='semibold')
        ax.set_xlabel('Weight Allocation Scenarios', fontsize=12, labelpad=12, color='#1e293b', fontweight='semibold')
        ax.set_title('Sensitivity of G7 Rankings across Policy Scenarios', fontsize=15, pad=20, color='#0f172a', fontweight='bold')
        
        ax.yaxis.grid(True, linestyle='--', alpha=0.6, color='#cbd5e1')
        ax.xaxis.grid(True, linestyle=':', alpha=0.4, color='#cbd5e1')
        ax.set_axisbelow(True)
        
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['left'].set_color('#94a3b8')
        ax.spines['bottom'].set_color('#94a3b8')
        ax.tick_params(colors='#475569', labelsize=11)
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=4, title='Countries', frameon=True, fontsize=10)
        ax.set_xlim(-0.5, len(scenarios_cols)-0.5)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_fig_dir, 'Scenario_Sensitivity_Analysis.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Try to load world map data
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    print("Loading world map datasets from Natural Earth...")
    try:
        world = geopandas.read_file(url)
        world.rename(columns={"ADMIN": "name"}, inplace=True)
        # Normalize US name
        world.loc[world['name'] == 'United States of America', 'name'] = 'United States'
    except Exception as e:
        print(f"Warning: Failed to load world map dataset from network: {e}")
        print("Map visualization will be skipped. Please check internet connection.")
        return

    # Load project data
    matrix, alt_names, criteria_ids, criteria_names, types, pillars = load_data()
    
    # Get Criteria 1 (Investment) and Criteria 4 (Automation Job Risk) from data matrix
    # Note: Criteria 1 is at index 0, Criteria 4 is at index 3
    investment_vals = matrix[:, 0]
    job_risk_vals = matrix[:, 3]
    
    # Colors for individual countries (matching original script)
    g7_colors = {
        'Canada': '#e6194b', 
        'France': '#3cb44b', 
        'Germany': '#ffe119', 
        'Italy': '#4363d8', 
        'Japan': '#f58231', 
        'United Kingdom': '#911eb4', 
        'United States': '#46f0f0'
    }
    
    # Create pandas dataframes for plotting
    df_metrics = pd.DataFrame({
        'country': alt_names,
        'investment': investment_vals,
        'job_risk': job_risk_vals,
        'color': [g7_colors[c] for c in alt_names]
    })

    # =========================================================================
    # MAP 1: Private Investment in AI
    # =========================================================================
    print("Generating Map 1: Private Investment in AI...")
    world_inv = world.merge(df_metrics, left_on='name', right_on='country', how='left')
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    # Plot base world
    world_inv.plot(ax=ax, color='#E0E0E0', edgecolor='white')
    
    # Highlight G7 countries
    g7_inv = world_inv.dropna(subset=['investment'])
    g7_inv.plot(ax=ax, color=g7_inv['color'], edgecolor='white')
    
    # Annotations
    for _, row in g7_inv.iterrows():
        point = row.geometry.representative_point()
        label = f"{row['country']}\n${row['investment']:.2f}B"
        
        # Manual offset coordinates
        xy = (point.x, point.y)
        c_name = row['country']
        if c_name == 'Canada':
            xy = (-110, 58)
        elif c_name == 'France':
            xy = (-5, 42.5)
        elif c_name == 'Germany':
            xy = (20, 54)
        elif c_name == 'Italy':
            xy = (20, 38)
        elif c_name == 'Japan':
            xy = (138, 40)
        elif c_name == 'United Kingdom':
            xy = (-20, 54)
        elif c_name == 'United States':
            xy = (-100, 40)
            
        ax.annotate(text=label, xy=xy, ha='center', va='center', color='black',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5, alpha=0.7))
        
    ax.set_axis_off()
    ax.set_title('Private Investment in AI (billions of U.S. dollars)', fontdict={'fontsize': '22', 'fontweight': '3'})
    ax.set_xlim([-150, 150])
    ax.set_ylim([0, 80])
    
    inv_map_path = os.path.join(output_fig_dir, 'G7_AI_Investment_Map.png')
    fig.savefig(inv_map_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # =========================================================================
    # MAP 2: Share of Jobs at High Risk of Automation
    # =========================================================================
    print("Generating Map 2: Jobs at Risk of Automation...")
    world_jobs = world.merge(df_metrics, left_on='name', right_on='country', how='left')
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    world_jobs.plot(ax=ax, color='#E0E0E0', edgecolor='white')
    
    g7_jobs = world_jobs.dropna(subset=['job_risk'])
    g7_jobs.plot(ax=ax, color=g7_jobs['color'], edgecolor='white')
    
    # Annotations
    for _, row in g7_jobs.iterrows():
        point = row.geometry.representative_point()
        label = f"{row['country']}\n{row['job_risk']:.1f}%"
        
        # Manual offset coordinates
        xy = (point.x, point.y)
        c_name = row['country']
        if c_name == 'Canada':
            xy = (-110, 58)
        elif c_name == 'France':
            xy = (-5, 42.5)
        elif c_name == 'Germany':
            xy = (20, 54)
        elif c_name == 'Italy':
            xy = (20, 38)
        elif c_name == 'Japan':
            xy = (138, 40)
        elif c_name == 'United Kingdom':
            xy = (-20, 54)
        elif c_name == 'United States':
            xy = (-100, 40)
            
        ax.annotate(text=label, xy=xy, ha='center', va='center', color='black',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5, alpha=0.7))
        
    ax.set_axis_off()
    ax.set_title('Share of Jobs at High Risk of Automation (%)', fontdict={'fontsize': '22', 'fontweight': '3'})
    ax.set_xlim([-150, 150])
    ax.set_ylim([0, 80])
    
    jobs_map_path = os.path.join(output_fig_dir, 'G7_AI_Share_of_Jobs_Map.png')
    fig.savefig(jobs_map_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # =========================================================================
    # MAP 3: G7 Ranking Bubble Map (TOPSIS Closeness & Rank)
    # =========================================================================
    print("Generating Map 3: G7 TOPSIS Ranking Bubble Map...")
    ranking_csv_path = os.path.join(steps_csv_dir, '9_Final_Ranking.csv')
    if not os.path.exists(ranking_csv_path):
        print(f"Warning: Final Ranking CSV not found at {ranking_csv_path}. Bubble map generation skipped.")
        return
        
    df_ranking = pd.read_csv(ranking_csv_path)
    
    world_rank = world.merge(df_ranking, left_on='name', right_on='Country', how='left')
    g7_polygons = world_rank.dropna(subset=['TOPSIS Score']).copy()
    
    # Create coordinates for bubble points
    g7_bubbles = g7_polygons.copy()
    g7_bubbles['geometry'] = g7_bubbles.geometry.representative_point()
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    cmap = 'viridis_r'
    
    # Plot base world
    world.plot(ax=ax, color='#E0E0E0', edgecolor='white')
    
    # Outline G7 country borders with rank colormap
    g7_polygons.plot(ax=ax, facecolor='none', column='Rank', cmap=cmap, linewidth=1)
    
    # Plot bubble indicators on representative points
    g7_bubbles.plot(ax=ax, 
                    markersize=g7_bubbles['TOPSIS Score'] * 2000, 
                    column='Rank', 
                    cmap=cmap, 
                    alpha=0.7, 
                    legend=False)
    
    # Labels
    for _, row in g7_bubbles.iterrows():
        c_name = row['Country']
        xy = (row.geometry.x, row.geometry.y)
        
        # Manual coordinate tuning
        if c_name == 'Canada':
            xy = (-105, 62)
        elif c_name == 'United States':
            xy = (-110, 43)
        elif c_name == 'United Kingdom':
            xy = (-24, 54)
        elif c_name == 'France':
            xy = (-10, 45)
        elif c_name == 'Germany':
            xy = (17, 57)
        elif c_name == 'Italy':
            xy = (22, 42)
        elif c_name == 'Japan':
            xy = (142, 41)
            
        ax.annotate(text=f"{c_name}\n(Rank {int(row['Rank'])})", xy=xy, ha='center', va='center',
                    color='black', fontsize=11, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5, alpha=0.7))
        
    # Legend for bubble sizes
    scores_for_legend = [0.35, 0.5, 0.65]
    for score in scores_for_legend:
        ax.scatter([], [], s=score * 2000, c='gray', alpha=0.7, label=f'{score:.2f}')
        
    ax.legend(
        title='TOPSIS Score (represented by bubble size)',
        ncol=3,
        frameon=True,
        loc='lower left',
        bbox_to_anchor=(0.05, 0.15),
        borderpad=0.8,
        labelspacing=1.0,
        columnspacing=1.5,
        handletextpad=1.0,
        fontsize='large'
    )
    
    # Colorbar for ranks
    norm = plt.Normalize(vmin=g7_polygons['Rank'].min(), vmax=g7_polygons['Rank'].max())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    cbar_ax = fig.add_axes([0.5, 0.1, 0.4, 0.03])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Rank (lower is better)', size='large')
    
    ax.set_axis_off()
    ax.set_title('G7 Country Rankings by TOPSIS Closeness Coefficient', fontdict={'fontsize': '22', 'fontweight': '5'})
    ax.set_xlim([-150, 150])
    ax.set_ylim([0, 80])
    fig.subplots_adjust(bottom=0.2)
    
    bubble_map_path = os.path.join(output_fig_dir, 'G7_Ranking_BubbleMap_Custom.png')
    fig.savefig(bubble_map_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"All visualizations exported successfully to '{output_fig_dir}'\n")

if __name__ == '__main__':
    run_visualization()
