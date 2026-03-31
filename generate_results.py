import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set visual preferences for high-quality Overleaf outputs (based on memory constraints)
plt.rcParams.update({'font.size': 11, 'figure.dpi': 300, 'axes.labelsize': 12, 'axes.titlesize': 14})
sns.set_theme(style="whitegrid", context="paper")

def generate_mock_results():
    """
    Since the dataset was unavailable, we generate an illustrative results table
    that a user would see after running the pipeline.
    """

    # Example metrics (Isolation Risk Score: 0 to 72 hours)
    data = {
        'Model': ['Linear Regression', 'Random Forest Regressor', 'XGBoost Regressor'],
        'RMSE (Hours)': [12.45, 8.32, 7.85],
        'MAE (Hours)': [9.80, 6.15, 5.92],
        'R² Score': [0.62, 0.78, 0.81]
    }

    df = pd.DataFrame(data)

    # 1. Save to CSV
    csv_path = 'model_performance_results.csv'
    df.to_csv(csv_path, index=False)
    print(f"Results table saved to {csv_path}")

    # 2. Generate a visual table (Image)
    fig, ax = plt.subplots(figsize=(6, 2), dpi=300)
    ax.axis('tight')
    ax.axis('off')

    # Style the table
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)

    # Header styling
    for i in range(len(df.columns)):
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(0, i)].set_facecolor('#4c72b0')

    plt.title('Model Performance Comparison\n(Predicting Isolation Risk Score)', pad=20, weight='bold')
    plt.tight_layout()
    table_img_path = 'results_table.png'
    plt.savefig(table_img_path, bbox_inches='tight')
    plt.close()
    print(f"Results table image saved to {table_img_path}")

    # 3. Generate a grouped bar chart
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Melt the dataframe for seaborn plotting
    df_melted_error = df.melt(id_vars='Model', value_vars=['RMSE (Hours)', 'MAE (Hours)'],
                              var_name='Metric', value_name='Error (Lower is Better)')

    df_melted_r2 = df.melt(id_vars='Model', value_vars=['R² Score'],
                           var_name='Metric', value_name='Score (Higher is Better)')

    # Plot Error Metrics (RMSE, MAE)
    sns.barplot(data=df_melted_error, x='Model', y='Error (Lower is Better)', hue='Metric',
                palette='Set2', ax=axes[0])
    axes[0].set_title('Prediction Error Metrics')
    axes[0].set_ylabel('Hours')
    axes[0].set_xlabel('')
    axes[0].tick_params(axis='x', rotation=15)
    for p in axes[0].patches:
        axes[0].annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    # Plot R2 Score
    sns.barplot(data=df_melted_r2, x='Model', y='Score (Higher is Better)',
                palette='Blues_d', ax=axes[1], legend=False)
    axes[1].set_title('Model Fit (R² Score)')
    axes[1].set_ylabel('R²')
    axes[1].set_xlabel('')
    axes[1].set_ylim(0, 1.0)
    axes[1].tick_params(axis='x', rotation=15)
    for p in axes[1].patches:
        axes[1].annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.suptitle('Comparison of Models for Community Isolation Risk', fontsize=16, weight='bold')
    plt.tight_layout()
    chart_img_path = 'results_chart.png'
    plt.savefig(chart_img_path, bbox_inches='tight')
    plt.close()
    print(f"Results chart image saved to {chart_img_path}")

if __name__ == "__main__":
    generate_mock_results()
