# %% [markdown]
# # Predicting Community Isolation Risk During Extreme Tropical Rainfall
#
# **Objective:** Develop a machine learning regression model to predict a Community Isolation Risk Score,
# defined as the expected number of hours a residential area becomes impassable during extreme tropical rainfall events.

# %% [markdown]
# ## 1. Data Preparation
# Extract ZIP file and Load datasets using Pandas

# %%
import os
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import shap

# Set visual preferences for plots
plt.rcParams.update({'font.size': 11, 'figure.dpi': 300})

# %%
def extract_and_load_data(zip_path, extract_dir='./data'):
    """
    Extracts the dataset ZIP file and loads the CSV files into Pandas DataFrames.
    """
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    print(f"Extracting {zip_path} to {extract_dir}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Extraction complete.")
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return None, None, None

    # Walk through the extracted directory to find the CSV files
    # This handles cases where files are nested inside a subfolder
    train_path, test_path, submission_path = None, None, None
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file == 'train.csv':
                train_path = os.path.join(root, file)
            elif file == 'test.csv':
                test_path = os.path.join(root, file)
            elif file == 'sample_submission.csv':
                submission_path = os.path.join(root, file)

    train_df, test_df, submission_df = None, None, None

    if train_path and os.path.exists(train_path):
        train_df = pd.read_csv(train_path)
        print(f"Loaded train data: {train_df.shape}")
    else:
        print("train.csv not found in the extracted files.")

    if test_path and os.path.exists(test_path):
        test_df = pd.read_csv(test_path)
        print(f"Loaded test data: {test_df.shape}")
    else:
        print("test.csv not found in the extracted files.")

    if submission_path and os.path.exists(submission_path):
        submission_df = pd.read_csv(submission_path)
        print(f"Loaded sample submission data: {submission_df.shape}")
    else:
        print("sample_submission.csv not found in the extracted files.")

    return train_df, test_df, submission_df

# %%
# Define path to the uploaded dataset
# Note: Update this path to where the actual dataset ZIP is located
dataset_zip_path = 'dataset.zip'

# Extract and load
# train_data, test_data, sample_submission = extract_and_load_data(dataset_zip_path)

# %% [markdown]
# ## 2. Data Cleaning & Exploratory Data Analysis (EDA)
# Inspect structure, missing values, distributions, and correlation.

# %%
def perform_basic_cleaning(df):
    """
    Perform initial data cleaning: handle missing values and potential basic outliers.
    """
    if df is None:
        return None

    df_clean = df.copy()

    # Check for missing values
    missing_cols = df_clean.columns[df_clean.isnull().any()]
    if len(missing_cols) > 0:
        print(f"Missing values found in: {list(missing_cols)}")
        # For simplicity, fill numeric with median and categorical with mode
        for col in missing_cols:
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            else:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        print("Missing values filled.")
    else:
        print("No missing values found.")

    return df_clean

# Clean datasets
# train_data_clean = perform_basic_cleaning(train_data)
# test_data_clean = perform_basic_cleaning(test_data)

# %%
def perform_eda(df, target_col):
    """
    Generates exploratory data analysis plots and correlations.
    """
    if df is None or target_col not in df.columns:
        print("Data or target column not available for EDA.")
        return

    # 1. Distribution of the Target Variable
    plt.figure(figsize=(8, 5))
    sns.histplot(df[target_col], kde=True, bins=30)
    plt.title(f'Distribution of {target_col}')
    plt.xlabel(target_col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    # 2. Correlation Matrix Heatmap (Numerical features only)
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 1:
        plt.figure(figsize=(12, 10))
        corr_matrix = numeric_df.corr()
        # Mask the upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=False, cmap='coolwarm',
                    vmax=1.0, vmin=-1.0, linewidths=0.5, fmt='.2f')
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.show()

        # 3. Top Correlations with Target
        print(f"Top 10 features correlated with {target_col}:")
        top_corr = corr_matrix[target_col].abs().sort_values(ascending=False).head(11)
        print(top_corr[1:]) # Exclude self-correlation

# Assuming target is either 'FloodProbability' or we create 'IsolationRiskScore' later
# perform_eda(train_data_clean, 'FloodProbability')

# %% [markdown]
# ## 3. Feature Engineering
# Normalize / scale numerical features, encode categorical variables, and derive new risk features.

# %%
def feature_engineering(train_df, test_df, target_col='FloodProbability'):
    """
    Prepares data for modeling by scaling features and engineering new domain-specific variables.
    """
    if train_df is None or test_df is None:
        return None, None, None, None

    # Create working copies
    X_train = train_df.copy()
    X_test = test_df.copy()

    # 1. Create Isolation Risk Score (if targeting hours of inaccessibility)
    # If the target is simply FloodProbability (0 to 1), we can proxy an isolation score.
    # E.g., assume a max of 72 hours of isolation, score = Probability * 72
    # The requirement allows either using FloodProbability or transforming it.
    # We will use 'IsolationRiskScore' as the target.
    if target_col in X_train.columns:
        X_train['IsolationRiskScore'] = X_train[target_col] * 72.0
        y_train = X_train.pop('IsolationRiskScore')
        # We don't need the original probability column for modeling
        X_train = X_train.drop(columns=[target_col], errors='ignore')
    else:
        # Fallback if target is already IsolationRiskScore or similar
        y_train = X_train.pop('IsolationRiskScore') if 'IsolationRiskScore' in X_train.columns else X_train.pop(X_train.columns[-1])

    # Remove target from test if it exists (e.g., in a leak)
    X_test = X_test.drop(columns=[target_col, 'IsolationRiskScore'], errors='ignore')

    # Drop ID columns if they exist
    ids_to_drop = ['id', 'Id', 'ID']
    train_ids = None
    test_ids = None
    for id_col in ids_to_drop:
        if id_col in X_train.columns:
            train_ids = X_train.pop(id_col)
        if id_col in X_test.columns:
            test_ids = X_test.pop(id_col)

    # 2. Derive Additional Features (if specific columns are available)
    # The dataset features mentioned: MonsoonIntensity, DrainageSystems, DeterioratingInfrastructure, Elevation, RoadAccess
    for df in [X_train, X_test]:
        # Infrastructure Vulnerability Index
        infra_cols = ['DeterioratingInfrastructure', 'DrainageSystems']
        if all(col in df.columns for col in infra_cols):
            # Higher deteriorating infra and lower drainage quality = higher vulnerability
            df['InfrastructureVulnerability'] = df['DeterioratingInfrastructure'] / (df['DrainageSystems'] + 1)

        # Severe Rainfall Impact
        rain_cols = ['MonsoonIntensity', 'TopographyDrainage'] # guessing related col
        if all(col in df.columns for col in rain_cols):
            df['SevereRainfallImpact'] = df['MonsoonIntensity'] * df['TopographyDrainage']

        # Overall Risk Proxy
        if 'MonsoonIntensity' in df.columns and 'DrainageSystems' in df.columns:
            df['RainToDrainageRatio'] = df['MonsoonIntensity'] / (df['DrainageSystems'] + 1)

    # 3. Categorical Encoding
    cat_cols = X_train.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        # Use simple get_dummies for categorical encoding
        X_train = pd.get_dummies(X_train, columns=cat_cols, drop_first=True)
        X_test = pd.get_dummies(X_test, columns=cat_cols, drop_first=True)
        # Ensure train and test have the same dummy columns
        X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

    # 4. Normalize / Scale Numerical Features
    # Note: Fitting scaler ONLY on training data to prevent data leakage (as per memory constraints)
    scaler = StandardScaler()
    num_cols = X_train.select_dtypes(include=[np.number]).columns

    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    return X_train, X_test, y_train, test_ids

# Execute feature engineering
# X_train_scaled, X_test_scaled, y_train, test_ids = feature_engineering(train_data_clean, test_data_clean)

# %% [markdown]
# ## 4. Model Development
# Train and compare Linear Regression, Random Forest Regressor, and Gradient Boosting (XGBoost).

# %%
def train_and_evaluate_models(X, y):
    """
    Splits the data into train/validation sets, trains models, and returns them along with their metrics.
    """
    if X is None or y is None:
        return None, None

    # Split the data into training and validation sets
    X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1, objective='reg:squarederror')
    }

    results = {}
    trained_models = {}

    print("Training and Evaluating Models...\n" + "-"*40)
    for name, model in models.items():
        # Train model
        model.fit(X_tr, y_tr)
        trained_models[name] = model

        # Predict on validation set
        preds = model.predict(X_val)

        # Calculate metrics
        rmse = mean_squared_error(y_val, preds, squared=False)
        mae = mean_absolute_error(y_val, preds)
        r2 = r2_score(y_val, preds)

        results[name] = {'RMSE': rmse, 'MAE': mae, 'R2': r2}

        print(f"[{name}]")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  MAE:  {mae:.4f}")
        print(f"  R²:   {r2:.4f}\n")

    return trained_models, results

# trained_models, eval_results = train_and_evaluate_models(X_train_scaled, y_train)

# %% [markdown]
# ## 5. Model Interpretation (SHAP)
# Explain key drivers of isolation risk using SHAP values.

# %%
def interpret_model_shap(model, X_sample, model_name="Model"):
    """
    Generates SHAP summary plot for the selected model.
    """
    if model is None or X_sample is None:
        return

    print(f"Generating SHAP interpretation for {model_name}...")

    if isinstance(model, LinearRegression):
        explainer = shap.LinearExplainer(model, X_sample)
        shap_values = explainer.shap_values(X_sample)
    elif isinstance(model, RandomForestRegressor):
        explainer = shap.TreeExplainer(model)
        # Random Forest SHAP can be slow; use subset
        sample_size = min(1000, X_sample.shape[0])
        subset_X = X_sample.sample(n=sample_size, random_state=42)
        shap_values = explainer.shap_values(subset_X)
        X_sample = subset_X
    else:
        # XGBoost
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)

    plt.figure()
    shap.summary_plot(shap_values, X_sample, show=False)
    plt.title(f'SHAP Summary Plot - {model_name}')
    plt.tight_layout()
    plt.show()

# Best model selection (example: choosing XGBoost if available)
# if trained_models and 'XGBoost' in trained_models:
#     # We use a sample of the training data for SHAP interpretation
#     interpret_model_shap(trained_models['XGBoost'], X_train_scaled.sample(min(1000, len(X_train_scaled))), "XGBoost")

# %% [markdown]
# ## 6. Prediction & Submission
# Generate predictions on the test dataset and format them according to the sample submission file.

# %%
def create_submission(model, X_test, submission_df, test_ids, output_path='submission.csv'):
    """
    Generates predictions using the best model and saves the submission file.
    """
    if model is None or X_test is None or submission_df is None:
        print("Required inputs missing to create a submission.")
        return

    print("Generating predictions on test data...")
    predictions = model.predict(X_test)

    # Clip predictions if they represent hours (e.g., minimum 0)
    predictions = np.clip(predictions, 0, None)

    sub = submission_df.copy()

    # Update the target column in the sample submission
    # Depending on the column name in sample submission (e.g., 'FloodProbability' or 'IsolationRiskScore')
    target_col = sub.columns[-1]

    if len(predictions) == len(sub):
        sub[target_col] = predictions

        # If test IDs are available and 'id' is in submission, replace to ensure order is correct
        if test_ids is not None and sub.columns[0].lower() in ['id']:
             sub[sub.columns[0]] = test_ids.values

        sub.to_csv(output_path, index=False)
        print(f"Submission saved to {output_path}")
        print(sub.head())
    else:
        print(f"Length mismatch: predictions ({len(predictions)}) vs submission template ({len(sub)}).")

# Create submission using the best model (e.g. XGBoost)
# if trained_models and 'XGBoost' in trained_models:
#    create_submission(trained_models['XGBoost'], X_test_scaled, sample_submission, test_ids)

# %%
