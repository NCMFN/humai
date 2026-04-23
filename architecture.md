# Community Isolation Risk Prediction Architecture

This document outlines the high-level system architecture and data flow for the Community Isolation Risk modeling pipeline.

## System Architecture Diagram

```mermaid
graph TD
    %% Define Styles
    classDef data fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#bbf,stroke:#333,stroke-width:2px;
    classDef model fill:#bfb,stroke:#333,stroke-width:2px;
    classDef output fill:#fbf,stroke:#333,stroke-width:2px;

    %% Data Inputs
    A[Raw Dataset ZIP]:::data --> B(Data Extraction)
    B --> C1[train.csv]:::data
    B --> C2[test.csv]:::data
    B --> C3[sample_submission.csv]:::data

    %% Preprocessing
    C1 --> D(Data Cleaning & Handling Missing Values):::process
    C2 --> D

    %% EDA
    D --> E(Exploratory Data Analysis)
    E --> |Plots & Correlations| F{Insights}

    %% Feature Engineering
    D --> G(Feature Engineering):::process
    G --> |Scaling & Encoding| G1[Scaled Features]
    G --> |Derived Features| G2[Vulnerability & Impact Indices]
    G --> |Target Transformation| G3[Isolation Risk Score Proxy]

    %% Modeling
    G1 --> H(Model Training & Validation Split):::model
    G2 --> H
    G3 --> H

    H --> I1[Linear Regression]:::model
    H --> I2[Random Forest Regressor]:::model
    H --> I3[XGBoost Regressor]:::model

    I1 --> J(Model Evaluation: RMSE, MAE, R²):::process
    I2 --> J
    I3 --> J

    %% Interpretation
    J --> K(Model Interpretation: SHAP Values):::process
    K --> L[Feature Importance & Insight Generation]:::output

    %% Prediction & Submission
    J --> |Select Best Model| M(Predict on Test Data):::process
    C3 --> M
    M --> N[Final Submission.csv]:::output
```

### Component Details
1. **Data Inputs:** Raw uploaded ZIP dataset containing `train.csv`, `test.csv`, and `sample_submission.csv`.
2. **Preprocessing:** Handling missing values, cleaning outliers, and preparing data.
3. **Exploratory Data Analysis (EDA):** Visualizing distributions, calculating feature correlation matrices to identify initial feature importance.
4. **Feature Engineering:** Scaling numerical fields, encoding categorical variables, deriving vulnerability and weather impact indices, and generating an 'Isolation Risk Score' proxy from 'FloodProbability' target.
5. **Modeling:** A split validation approach to train and compare baseline Linear Regression, Random Forest, and Gradient Boosting (XGBoost).
6. **Model Evaluation:** Computing regression metrics: RMSE, MAE, R².
7. **Interpretation:** Utilizing SHAP values on the best model to provide explainability for the drivers of community isolation risk.
8. **Prediction & Submission:** Generating final Isolation Risk predictions for the test set and structuring the output based on `sample_submission.csv`.
