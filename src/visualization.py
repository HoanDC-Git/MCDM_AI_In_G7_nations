import os
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_data, BASE_DIR

def run_visualization():
    print("--- Executing Data Visualization Maps ---")
    
    # 1. Paths configuration
    output_fig_dir = os.path.join(BASE_DIR, 'outputs', 'figures')
    processed_data_dir = os.path.join(BASE_DIR, 'data', 'processed')
    steps_csv_dir = os.path.join(BASE_DIR, 'outputs', 'csv', 'steps')
    
    os.makedirs(output_fig_dir, exist_ok=True)
    
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
