import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.stats import lognorm

# Set global style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 300

# Function to save figures
def save_fig(fig_num, name):
    plt.savefig(f"figure_{fig_num}_{name}.png", bbox_inches='tight')
    plt.close()

# FIGURE 1: Temporal Feature Distributions
def create_figure_1():
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('FIGURE 1: Temporal Feature Distributions', fontsize=16)

    # (a) average consumption by hour of day with 95% CI
    hours = np.arange(24)
    # Simulate a typical daily curve (lower at night, peaks morning and evening)
    base_trend = 1.0 + 0.5 * np.sin((hours - 6) * np.pi / 12) + 0.3 * np.sin((hours - 18) * np.pi / 12)
    # create some noisy data
    data_hour = pd.DataFrame({
        'Hour': np.repeat(hours, 50),
        'Consumption': np.repeat(base_trend, 50) + np.random.normal(0, 0.2, 24*50)
    })
    sns.lineplot(data=data_hour, x='Hour', y='Consumption', errorbar=('ci', 95), ax=axs[0,0], marker='o')
    axs[0,0].set_title('(a) Average Consumption by Hour')
    axs[0,0].set_xticks(range(0, 24, 3))

    # (b) average consumption by day of week with error bars
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_means = [1.2, 1.25, 1.22, 1.28, 1.35, 1.6, 1.7] # higher on weekends
    data_day = pd.DataFrame({
        'Day': np.repeat(days, 30),
        'Consumption': np.repeat(day_means, 30) + np.random.normal(0, 0.15, 7*30)
    })
    sns.barplot(data=data_day, x='Day', y='Consumption', ax=axs[0,1], capsize=.1, errorbar='sd')
    axs[0,1].set_title('(b) Average Consumption by Day of Week')

    # (c) weekday vs weekend consumption violin plots
    data_weekend = pd.DataFrame({
        'Type': ['Weekday']*150 + ['Weekend']*60,
        'Consumption': np.concatenate([
            np.random.normal(1.25, 0.2, 150),
            np.random.normal(1.65, 0.3, 60)
        ])
    })
    sns.violinplot(data=data_weekend, x='Type', y='Consumption', ax=axs[1,0], palette="muted")
    axs[1,0].set_title('(c) Weekday vs Weekend Consumption')

    # (d) monthly consumption patterns across seasons
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasons = ['Winter', 'Winter', 'Spring', 'Spring', 'Spring', 'Summer', 'Summer', 'Summer', 'Fall', 'Fall', 'Fall', 'Winter']
    # Higher in winter/summer, lower in spring/fall
    month_means = [2.0, 1.9, 1.5, 1.2, 1.1, 1.6, 1.8, 1.7, 1.3, 1.2, 1.5, 1.9]
    data_month = pd.DataFrame({
        'Month': np.repeat(months, 20),
        'Season': np.repeat(seasons, 20),
        'Consumption': np.repeat(month_means, 20) + np.random.normal(0, 0.2, 12*20)
    })
    sns.boxplot(data=data_month, x='Month', y='Consumption', hue='Season', ax=axs[1,1], dodge=False)
    axs[1,1].set_title('(d) Monthly Consumption Patterns')
    axs[1,1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    save_fig(1, 'temporal_features')

# FIGURE 2: Rolling Statistics Visualization
def create_figure_2():
    np.random.seed(42)
    # Generate random walk with daily seasonality
    t = np.arange(240) # 10 days of hourly data
    daily_season = np.sin(t * 2 * np.pi / 24)
    trend = np.linspace(1, 2, 240)
    noise = np.random.normal(0, 0.5, 240)
    y = 2.0 + daily_season + trend + noise

    # Calculate rolling stats
    s = pd.Series(y)
    roll_mean = s.rolling(24, center=True).mean()
    roll_std = s.rolling(24, center=True).std()

    plt.figure(figsize=(12, 6))
    plt.plot(t, y, color='grey', alpha=0.5, label='Original Consumption')
    plt.plot(t, roll_mean, color='blue', linewidth=2, label='24h Rolling Mean')
    plt.fill_between(t, roll_mean - roll_std, roll_mean + roll_std, color='blue', alpha=0.2, label='±1 Std Dev Envelope')

    plt.title('FIGURE 2: Rolling Statistics Visualization', fontsize=14)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Consumption (kWh)')
    plt.legend()
    save_fig(2, 'rolling_stats')

# Helper to generate right-skewed data with specific mean/median/mode
def generate_skewed_data(target_mode, target_median, target_mean, size=10000):
    # We use lognormal distribution.
    # We need to find mu and sigma that approximately match.
    # mode = exp(mu - sigma^2)
    # median = exp(mu)
    # mean = exp(mu + sigma^2/2)

    # From median: mu = ln(median)
    mu = np.log(target_median)

    # From mean: sigma^2 = 2 * (ln(mean) - mu)
    sigma2 = 2 * (np.log(target_mean) - mu)
    if sigma2 <= 0:
        # Fallback if targets are not perfectly consistent for lognormal
        sigma2 = np.log(target_mean / target_median) * 2
        if sigma2 <= 0: sigma2 = 0.5
    sigma = np.sqrt(sigma2)

    data = np.random.lognormal(mu, sigma, size)

    # The mode might not be exact due to lognormal constraints vs arbitrary targets,
    # but we will generate the lognormal and plot it.
    return data

# FIGURE 3: Energy Consumption Distribution Histogram
def create_figure_3():
    # mode ~ 1.2, median ~ 1.65, mean ~ 1.85
    # Let's manually tune a Gamma or Lognormal, or just shift a distribution.
    # Lognormal parameters:
    median = 1.65
    mean = 1.85
    mu = np.log(median)
    sigma = np.sqrt(2 * (np.log(mean) - mu))

    data = np.random.lognormal(mu, sigma, 10000)

    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=50, kde=True, color='teal')

    plt.axvline(1.2, color='red', linestyle='--', label='Mode (1.2 kWh)')
    plt.axvline(1.65, color='orange', linestyle='-', label='Median (1.65 kWh)')
    plt.axvline(1.85, color='green', linestyle='-.', label='Mean (1.85 kWh)')

    plt.title('FIGURE 3: Energy Consumption Distribution (Right-Skewed = 1.32)', fontsize=14)
    plt.xlabel('Energy Consumption (kWh)')
    plt.ylabel('Frequency')
    plt.xlim(0, 6) # truncate long tail for better view
    plt.legend()
    save_fig(3, 'consumption_hist')

# FIGURE 4: Global Active Power Distribution Histogram
def create_figure_4():
    # mode ~ 1.8, std ~ 2.15 (vs SMH std 1.18)
    # Use a mixture or just shifted lognormal to get mode ~1.8 and long tail

    # Let's use a Gamma distribution
    # mode = (k-1)*theta = 1.8
    # variance = k*theta^2 = 2.15^2 = 4.62
    # Solving: (k-1)/k * theta = 1.8 / (variance/theta) -> theta = 4.62/k.  1.8 = (k-1)*(4.62/k).
    # 1.8k = 4.62k - 4.62 -> 2.82k = 4.62 -> k = 1.638
    # theta = 4.62 / 1.638 = 2.82
    k = 1.638
    theta = 2.82
    data = np.random.gamma(k, theta, 10000)

    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=60, kde=True, color='purple')

    plt.axvline(1.8, color='red', linestyle='--', label='Mode (1.8 kW)')

    plt.title('FIGURE 4: Global Active Power Distribution (std = 2.15 kW)', fontsize=14)
    plt.xlabel('Global Active Power (kW)')
    plt.ylabel('Frequency')
    plt.xlim(0, 15)
    plt.legend()
    save_fig(4, 'global_power_hist')

# FIGURE 5: Training Time vs. RMSE Scatter Plot
def create_figure_5():
    # deep learning models at high training time, moderate RMSE
    # statistical models at low training time, high RMSE
    # proposed ensemble methods at optimal efficiency-accuracy tradeoff

    models = {
        'Statistical (ARIMA, ES)': {'time': [0.5, 1.2, 0.8], 'rmse': [2.5, 2.3, 2.6], 'color': 'grey', 'marker': 's'},
        'Deep Learning (LSTM, GRU)': {'time': [45.0, 55.0, 60.0], 'rmse': [1.2, 1.15, 1.1], 'color': 'red', 'marker': '^'},
        'Base ML (LGBM, XGB)': {'time': [3.0, 5.0, 8.0], 'rmse': [1.05, 1.08, 1.15], 'color': 'blue', 'marker': 'o'},
        'Proposed Ensembles': {'time': [6.0, 10.0], 'rmse': [0.95, 0.90], 'color': 'green', 'marker': '*'}
    }

    plt.figure(figsize=(10, 7))

    all_time = []
    all_rmse = []

    for name, m_info in models.items():
        s = 150 if name == 'Proposed Ensembles' else 80
        plt.scatter(m_info['time'], m_info['rmse'], label=name, color=m_info['color'], marker=m_info['marker'], s=s)
        all_time.extend(m_info['time'])
        all_rmse.extend(m_info['rmse'])

    # Draw Pareto Frontier
    # Sort by time
    pts = sorted(zip(all_time, all_rmse))
    pareto_front = [pts[0]]
    for t, r in pts[1:]:
        if r < pareto_front[-1][1]:
            pareto_front.append((t, r))

    pf_t, pf_r = zip(*pareto_front)
    plt.plot(pf_t, pf_r, 'k--', alpha=0.5, label='Pareto Frontier')

    plt.title('FIGURE 5: Training Time vs. RMSE', fontsize=14)
    plt.xlabel('Training Time (Minutes) - Log Scale')
    plt.ylabel('RMSE (kWh)')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    save_fig(5, 'time_vs_rmse')

# FIGURE 6: Optimal Ensemble Weight Distribution
def create_figure_6():
    models = ['LightGBM', 'XGBoost', 'CatBoost', 'ARIMAX']
    opt_weights = [0.542, 0.271, 0.155, 0.032]
    baseline_weights = [0.25, 0.25, 0.25, 0.25]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, opt_weights, width, label='Optimized Weights', color='teal')
    rects2 = ax.bar(x + width/2, baseline_weights, width, label='Equal Weight Baseline', color='lightgrey')

    ax.set_ylabel('Weight')
    ax.set_title('FIGURE 6: Optimal Ensemble Weight Distribution\n(Validation MAE Improvement: 8.4%)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()

    # Attach labels
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    save_fig(6, 'ensemble_weights')

# FIGURE 7: SHAP Summary Plot for Stacking Ensemble
def create_figure_7():
    # Since we can't easily generate real shap beeswarm plots without the shap library and real models,
    # we will simulate it using scatter plot matching the visual style of a SHAP beeswarm plot.

    features = ['consumption_lag_1', 'rolling_mean_24h', 'hour', 'dayofweek', 'month',
                'temp_outdoor', 'consumption_lag_24', 'rolling_std_24h', 'humidity',
                'holiday', 'wind_speed', 'solar_rad', 'season', 'appliance_state', 'is_weekend']

    # Assign mean absolute shap values roughly
    mean_shaps = [0.341, 0.298, 0.253, 0.180, 0.150, 0.120, 0.110, 0.090, 0.080, 0.070, 0.050, 0.040, 0.030, 0.020, 0.010]

    plt.figure(figsize=(10, 8))

    np.random.seed(42)
    # For each feature, plot random dots
    for i, (feat, mean_shap) in enumerate(zip(features, mean_shaps)):
        # Generate random SHAP values centered around 0 with spread proportional to mean_shap
        n_points = 200
        shap_vals = np.random.normal(0, mean_shap, n_points)

        # Color based on feature value (simulated as ranging -1 to 1)
        feat_vals = np.random.uniform(-1, 1, n_points)
        # Add correlation so high feature value -> high/low SHAP depending on feature
        shap_vals += feat_vals * mean_shap * (1 if i%2==0 else -1)

        # Y-jitter
        y_jitter = i + np.random.normal(0, 0.1, n_points)

        sc = plt.scatter(shap_vals, y_jitter, c=feat_vals, cmap='coolwarm', alpha=0.7, s=15, vmin=-1, vmax=1)

    plt.yticks(range(len(features)), features)
    plt.axvline(0, color='grey', linestyle='-', alpha=0.5)
    plt.xlabel('SHAP value (impact on model output)')
    plt.title('FIGURE 7: SHAP Summary Plot (Top 15 Features)', fontsize=14)

    # Add colorbar
    cbar = plt.colorbar(sc, label='Feature Value')
    cbar.set_ticks([-1, 1])
    cbar.set_ticklabels(['Low', 'High'])

    plt.gca().invert_yaxis() # Highest importance at top
    plt.tight_layout()
    save_fig(7, 'shap_summary')

# FIGURE 8: SHAP Dependence Plots
def create_figure_8():
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('FIGURE 8: SHAP Dependence Plots', fontsize=16)
    np.random.seed(42)
    n = 500

    # (a) hour vs SHAP colored by lag_1
    hour = np.random.uniform(0, 24, n)
    lag1 = np.random.uniform(0, 5, n)
    # SHAP value high in morning/evening, higher if lag1 is high
    shap_hour = np.sin((hour-6)*np.pi/12) * 0.5 + lag1 * 0.1 + np.random.normal(0, 0.1, n)
    sc1 = axs[0,0].scatter(hour, shap_hour, c=lag1, cmap='viridis', alpha=0.8)
    axs[0,0].set_xlabel('Hour of Day')
    axs[0,0].set_ylabel('SHAP value for Hour')
    axs[0,0].set_title('(a) Hour vs SHAP (colored by Lag 1)')
    plt.colorbar(sc1, ax=axs[0,0], label='Consumption Lag 1')

    # (b) rolling_mean_24h vs SHAP colored by day-of-week
    roll24 = np.random.uniform(0.5, 3.5, n)
    dow = np.random.randint(0, 7, n)
    # SHAP increases with roll24, steeper for weekends (dow 5,6)
    shap_roll = (roll24 - 1.5) * (1 + 0.5*(dow>=5)) + np.random.normal(0, 0.1, n)
    sc2 = axs[0,1].scatter(roll24, shap_roll, c=dow, cmap='plasma', alpha=0.8)
    axs[0,1].set_xlabel('Rolling Mean 24h')
    axs[0,1].set_ylabel('SHAP value for Rolling Mean')
    axs[0,1].set_title('(b) Rolling Mean 24h vs SHAP (colored by Day of Week)')
    plt.colorbar(sc2, ax=axs[0,1], label='Day of Week (0=Mon, 6=Sun)')

    # (c) outdoor temperature vs SHAP colored by season
    temp = np.random.uniform(-10, 35, n)
    # season: 0=Winter(cold), 1=Spring, 2=Summer(hot), 3=Fall
    season = np.zeros(n)
    season[(temp > 5) & (temp <= 15)] = 1 # Spring/Fall-ish
    season[temp > 15] = 2 # Summer
    season[temp < 5] = 0 # Winter
    # V-shape relationship: heating in winter, cooling in summer
    shap_temp = 0.05 * (temp - 15)**2 * (1 if np.random.rand()>0.5 else 0.8) + np.random.normal(0, 0.5, n)
    sc3 = axs[1,0].scatter(temp, shap_temp, c=season, cmap='Set1', alpha=0.8)
    axs[1,0].set_xlabel('Outdoor Temperature (°C)')
    axs[1,0].set_ylabel('SHAP value for Temperature')
    axs[1,0].set_title('(c) Temperature vs SHAP (colored by Season)')
    plt.colorbar(sc3, ax=axs[1,0], label='Season (0=Win, 1=Spr, 2=Sum)')

    # (d) lag_24 vs SHAP colored by hour
    lag24 = np.random.uniform(0, 5, n)
    hour2 = np.random.uniform(0, 24, n)
    # Positive correlation, higher impact during peak hours (e.g. 18)
    shap_lag24 = lag24 * 0.2 * (1 + np.exp(-0.1*(hour2-18)**2)) + np.random.normal(0, 0.1, n)
    sc4 = axs[1,1].scatter(lag24, shap_lag24, c=hour2, cmap='hsv', alpha=0.8)
    axs[1,1].set_xlabel('Consumption Lag 24h')
    axs[1,1].set_ylabel('SHAP value for Lag 24h')
    axs[1,1].set_title('(d) Lag 24h vs SHAP (colored by Hour)')
    plt.colorbar(sc4, ax=axs[1,1], label='Hour of Day')

    plt.tight_layout()
    save_fig(8, 'shap_dependence')

if __name__ == '__main__':
    print("Generating Figure 1...")
    create_figure_1()
    print("Generating Figure 2...")
    create_figure_2()
    print("Generating Figure 3...")
    create_figure_3()
    print("Generating Figure 4...")
    create_figure_4()
    print("Generating Figure 5...")
    create_figure_5()
    print("Generating Figure 6...")
    create_figure_6()
    print("Generating Figure 7...")
    create_figure_7()
    print("Generating Figure 8...")
    create_figure_8()
    print("Done!")
