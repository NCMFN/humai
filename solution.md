Based on a detailed analysis of the provided notebook screenshots (spanning data preprocessing, exploratory data analysis, feature engineering, and modeling), I have identified the weaknesses in the current ensemble approach and designed a robust solution.

Below is an improved workflow, complete with optimized code separated into cells, suitable for immediate use in Google Colab.

---

### 1. Analysis of the Baseline Approach & Weaknesses
From your notebook's "Data Analysis Key Findings" and "Ensemble Model Performance" sections:
*   **Simple Averaging Flaw:** The current ensemble uses a simple unweighted average of LightGBM, XGBoost, and CatBoost. Because LightGBM significantly outperforms the others (MAE: 0.4624 vs CatBoost MAE: 0.4705), weighting them equally drags down the ensemble's overall performance to 0.4645, making it worse than LightGBM alone.
*   **Suboptimal Validation:** The comparison and ensemble currently predict directly on `y_test`. To learn how to weight models effectively without data leakage, we need to optimize weights on a true Validation Set (`y_val`) or use out-of-fold predictions.
*   **Preprocessing Missing Robust Scaling:** Time-series models (and sometimes boosting models depending on variance) benefit from robust scaling, especially when combining features with vastly different ranges (like `global_active_power`, `sub_metering_X`, and `Energy Consumption (kWh)`).

### 2. Strategy for the Improved Ensemble
To guarantee the ensemble consistently outperforms individual models, we implement two advanced techniques:
1.  **Optimized Weighted Averaging (SciPy Minimize):** Instead of `(0.33, 0.33, 0.33)`, we use `scipy.optimize.minimize` to mathematically find the exact weights that minimize the MAE/RMSE on a chronological validation set. This penalizes the weaker models (like CatBoost/ARIMA) and rewards the stronger predictors (LightGBM).
2.  **Stacking Regressor with Time-Series Cross-Validation:** We employ a meta-learner (`Ridge` regression) to learn the optimal combination of base predictions. Crucially, we use `TimeSeriesSplit` to prevent future data from leaking into past predictions during the cross-validation phase of stacking.

---

### Google Colab Code Implementation

Paste the following code cells sequentially into your Google Colab notebook.

#### **CELL 1: Data Loading & Preprocessing (Improved)**
*This cell recreates your `merge_asof` logic but adds robust scaling and proper chronological train/validation/test splitting.*

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler

# 1. Load Data
hpc_path = "/content/drive/MyDrive/household_power_consumption - Copy.csv"
smh_path = "/content/drive/MyDrive/smart_home_energy_consumption_large.csv"
hpc_df = pd.read_csv(hpc_path)
smh_df = pd.read_csv(smh_path)

# 2. Process timestamps (As per your existing logic)
smh_df['Timestamp'] = pd.to_datetime(smh_df['Date'] + ' ' + smh_df['Time'])
smh_df = smh_df.drop(['Date', 'Time'], axis=1)

# hpc_df timestamp assignment (fixed date '2007-01-01' as observed in your EDA)
hpc_df['Timestamp'] = pd.to_datetime('2007-01-01 ' + hpc_df['time'])
hpc_df = hpc_df.drop(['Date', 'time'], axis=1)

# Sort both by Timestamp for merge_asof
smh_df = smh_df.sort_values('Timestamp')
hpc_df = hpc_df.sort_values('Timestamp')

# 3. Merge DataFrames
combined_df = pd.merge_asof(smh_df, hpc_df, on='Timestamp', direction='nearest', suffixes=('_smh', '_hpc'))

# 4. Feature Engineering (Lags, Rolling, Time-based)
combined_df['hour'] = combined_df['Timestamp'].dt.hour
combined_df['dayofweek'] = combined_df['Timestamp'].dt.dayofweek
combined_df['month'] = combined_df['Timestamp'].dt.month

# Categorical Encoding
combined_df = pd.get_dummies(combined_df, columns=['Appliance Type', 'Season'], drop_first=True)

# Lags & Rolling Statistics (Fixing Data Leakage)
# Crucial: Shift rolling windows so the current row's target is NOT included in the feature!
combined_df['Energy_lag_1'] = combined_df['Energy Consumption (kWh)'].shift(1)
combined_df['Energy_rolling_mean_24'] = combined_df['Energy Consumption (kWh)'].shift(1).rolling(window=24).mean()
combined_df['Energy_rolling_std_24'] = combined_df['Energy Consumption (kWh)'].shift(1).rolling(window=24).std()

# Handle missing values from lags/rolling via forward fill and dropna
# Avoid backward fill (bfill) as it leaks future data into the past.
combined_df = combined_df.ffill().dropna()

# 5. Define X and y
# Drop constant sub_metering columns as identified in your EDA
X = combined_df.drop(columns=['Timestamp', 'Energy Consumption (kWh)', 'sub_metering_1', 'sub_metering_2', 'sub_metering_3'])
y = combined_df['Energy Consumption (kWh)']

# 6. Chronological Train / Validation / Test Split
# It is critical NOT to use standard train_test_split for time-series!
train_size = int(len(X) * 0.70)
val_size = int(len(X) * 0.15)

X_train_raw, y_train = X.iloc[:train_size], y.iloc[:train_size]
X_val_raw, y_val = X.iloc[train_size:train_size+val_size], y.iloc[train_size:train_size+val_size]
X_test_raw, y_test = X.iloc[train_size+val_size:], y.iloc[train_size+val_size:]

# 7. Robust Scaling (Fixing Distribution Leakage)
# Scaler MUST be fit only on the training data to prevent test distribution leakage
scaler = RobustScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train_raw), columns=X.columns, index=X_train_raw.index)
X_val = pd.DataFrame(scaler.transform(X_val_raw), columns=X.columns, index=X_val_raw.index)
X_test = pd.DataFrame(scaler.transform(X_test_raw), columns=X.columns, index=X_test_raw.index)

print(f"Data Shapes -> Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
```

#### **CELL 2: Hyperparameter-Tuned Base Models**
*We instantiate the models with parameters slightly tuned for time-series and train them on the `train` set. We also include a tuned ARIMA model using Exogenous features.*

```python
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import time

print("Training Optimized Base Models...")

# 1. LightGBM (Best Performer)
model_lgbm = LGBMRegressor(random_state=42, n_estimators=500, learning_rate=0.05, max_depth=8, colsample_bytree=0.8, n_jobs=-1)
model_lgbm.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric='mae', callbacks=[])

# 2. XGBoost
model_xgb = XGBRegressor(random_state=42, n_estimators=500, learning_rate=0.05, max_depth=6, colsample_bytree=0.8, n_jobs=-1)
model_xgb.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

# 3. CatBoost
model_cat = CatBoostRegressor(random_state=42, iterations=500, learning_rate=0.05, depth=6, verbose=0)
model_cat.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=50)

# 4. ARIMA (Tuned with Exogenous variables)
# We use order (1,0,1) with exogenous variables (ARIMAX).
print("Training ARIMA model (this may take a moment)...")
model_arima = ARIMA(y_train.values, exog=X_train.values, order=(1,0,1))
arima_fit = model_arima.fit()

# Generate Predictions
# For simplicity in iteration, we separate the dictionary holding the scikit-learn models
tree_models = {'LightGBM': model_lgbm, 'XGBoost': model_xgb, 'CatBoost': model_cat}
val_preds = {}
test_preds = {}

# Predict tree models
for name, model in tree_models.items():
    val_preds[name] = model.predict(X_val)
    test_preds[name] = model.predict(X_test)

# Predict ARIMA
# ARIMA prediction needs exogenous features for the forecasting horizon
val_preds['ARIMA'] = arima_fit.forecast(steps=len(X_val), exog=X_val.values)
# Since ARIMA is a sequential time-series model, predicting test requires extending the model or re-fitting.
# For simplicity in this ensemble evaluation, we forecast from the end of training across both val and test periods,
# but it's more accurate to forecast sequentially. We'll forecast the test set from the end of the fitted data:
# First, append val to train to fit a new ARIMA or forecast further ahead.
# Given we are comparing standard test metrics, we'll forecast the test period:
arima_fit_full = ARIMA(np.concatenate([y_train.values, y_val.values]),
                       exog=np.concatenate([X_train.values, X_val.values]),
                       order=(1,0,1)).fit()
test_preds['ARIMA'] = arima_fit_full.forecast(steps=len(X_test), exog=X_test.values)

all_model_names = list(tree_models.keys()) + ['ARIMA']

print("\n--- Base Model Test Performance ---")
for name in all_model_names:
    mae = mean_absolute_error(y_test, test_preds[name])
    rmse = np.sqrt(mean_squared_error(y_test, test_preds[name]))
    print(f"{name} -> MAE: {mae:.4f} | RMSE: {rmse:.4f}")
```

#### **CELL 3: Improved Ensemble - Optimized Weighted Averaging**
*Instead of simple averaging, we use SciPy to find the optimal model weights based on validation performance.*

```python
from scipy.optimize import minimize

print("Optimizing Ensemble Weights based on Validation Set...")

# Objective function: Minimize Validation MAE
def mae_objective(weights, preds, true_values):
    ensemble_pred = np.zeros_like(true_values)
    for w, pred in zip(weights, preds):
        ensemble_pred += w * pred
    return mean_absolute_error(true_values, ensemble_pred)

val_pred_list = [val_preds[name] for name in all_model_names]
test_pred_list = [test_preds[name] for name in all_model_names]

# Initial guess (Equal weights)
initial_weights = [1/len(all_model_names)] * len(all_model_names)

# Constraints: weights must sum to 1, and be between 0 and 1
constraints = ({'type': 'eq', 'fun': lambda w: 1 - sum(w)})
bounds = [(0, 1) for _ in range(len(all_model_names))]

# Optimize using SLSQP
result = minimize(mae_objective, initial_weights, args=(val_pred_list, y_val),
                  method='SLSQP', bounds=bounds, constraints=constraints)

optimal_weights = result.x
print(f"Optimal Model Weights: {dict(zip(all_model_names, np.round(optimal_weights, 4)))}")

# Evaluate Optimized Ensemble on Test Set
weighted_test_pred = np.zeros_like(y_test)
for w, pred in zip(optimal_weights, test_pred_list):
    weighted_test_pred += w * pred

opt_weight_mae = mean_absolute_error(y_test, weighted_test_pred)
opt_weight_rmse = np.sqrt(mean_squared_error(y_test, weighted_test_pred))
print(f"\n✅ Optimized Weighted Ensemble -> MAE: {opt_weight_mae:.4f} | RMSE: {opt_weight_rmse:.4f}")
```

#### **CELL 4: Improved Ensemble - Time-Series Stacking Regressor**
*A more advanced technique where a meta-learner dynamically learns how to combine the base model predictions.*

```python
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit

print("Training Stacking Regressor (Time-Series Cross-Validation)...")

# Combine train and val sets for the stacking model's cross-validation
X_train_stack = pd.concat([X_train, X_val])
y_train_stack = pd.concat([y_train, y_val])

# TimeSeriesSplit prevents future data from leaking into past predictions during CV
tscv = TimeSeriesSplit(n_splits=5)

# Define estimators (using slightly fewer estimators for speed in CV)
# Note: StackingRegressor doesn't natively support statsmodels ARIMA.
# We use the three strong tree models for the stacking layer,
# while our Optimized Weighted Averaging (in Cell 3) includes ARIMA.
estimators = [
    ('lgbm', LGBMRegressor(random_state=42, n_estimators=200, n_jobs=-1, verbose=-1)),
    ('xgb', XGBRegressor(random_state=42, n_estimators=200, n_jobs=-1)),
    ('cat', CatBoostRegressor(random_state=42, iterations=200, verbose=0))
]

# Meta-learner: Ridge Regression
stacking_model = StackingRegressor(
    estimators=estimators,
    final_estimator=Ridge(alpha=1.0),
    cv=tscv,
    n_jobs=-1
)

stacking_model.fit(X_train_stack, y_train_stack)
stack_test_pred = stacking_model.predict(X_test)

stack_mae = mean_absolute_error(y_test, stack_test_pred)
stack_rmse = np.sqrt(mean_squared_error(y_test, stack_test_pred))
print(f"✅ Stacking Ensemble -> MAE: {stack_mae:.4f} | RMSE: {stack_rmse:.4f}")
```

#### **CELL 5: Final Evaluation & Visualization**
*A clean visualization to demonstrate how the improved ensembles compare to the base models.*

```python
import matplotlib.pyplot as plt

print("\n=== FINAL MODEL PERFORMANCE SUMMARY ===")
metrics = {}
for name in all_model_names:
    metrics[name] = {
        'MAE': mean_absolute_error(y_test, test_preds[name]),
        'RMSE': np.sqrt(mean_squared_error(y_test, test_preds[name]))
    }

metrics['Opt Weighted Ensemble'] = {'MAE': opt_weight_mae, 'RMSE': opt_weight_rmse}
metrics['Stacking Ensemble'] = {'MAE': stack_mae, 'RMSE': stack_rmse}

results_df = pd.DataFrame(metrics).T.sort_values(by='MAE')
print(results_df)

# Plotting the results
plt.figure(figsize=(12, 6))
bars = plt.bar(results_df.index, results_df['MAE'], color=['#ff9999' if 'Ensemble' not in x else '#66b3ff' for x in results_df.index])
plt.axhline(y=metrics['LightGBM']['MAE'], color='red', linestyle='--', label='Best Base Model (LightGBM) Baseline')

plt.title('Model MAE Comparison (Lower is Better)', fontsize=14)
plt.ylabel('Mean Absolute Error (MAE)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend()

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.005, round(yval, 4), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()
```