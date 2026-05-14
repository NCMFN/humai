import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.patches as patches

# 1. Load data
print("Step 1: Loading Data...")
df = pd.read_csv('/app/flood.csv')
features_to_keep = [
    'MonsoonIntensity', 'TopographyDrainage', 'RiverManagement', 'Deforestation',
    'Urbanization', 'ClimateChange', 'DamsQuality', 'Siltation', 'AgriculturalPractices',
    'Encroachments', 'DrainageSystems', 'CoastalVulnerability', 'Landslides', 'Watersheds',
    'FloodProbability'
]
df = df[features_to_keep]

print("Shape of data:", df.shape)
print("\nAll column names:")
print(list(df.columns))
print("\nFull .describe():")
print(df.describe(include='all').to_string())
print("\nMissing value count:")
print(df.isnull().sum())

# 2. Tertile binning of FloodProbability -> 3-class CIRS (Low / Medium / High)
print("\nStep 2: Tertile Binning...")
tertiles = df['FloodProbability'].quantile([0.3333, 0.6667]).values
print(f"Tertile thresholds: Low <= {tertiles[0]:.4f} < Medium <= {tertiles[1]:.4f} < High")

def assign_class(prob):
    if prob <= tertiles[0]:
        return 0 # Low
    elif prob <= tertiles[1]:
        return 1 # Medium
    else:
        return 2 # High

df['CIRS_Class'] = df['FloodProbability'].apply(assign_class)
class_labels = {0: 'Low', 1: 'Medium', 2: 'High'}

print("\nClass balance:")
balance = df['CIRS_Class'].value_counts().sort_index().rename(class_labels)
print(balance)

# Target Distribution Plot
plt.figure(figsize=(8, 5))
sns.countplot(x='CIRS_Class', data=df, palette='viridis', hue='CIRS_Class', legend=False)
plt.title('Target Distribution (CIRS Classes)')
plt.xticks(ticks=[0, 1, 2], labels=['Low', 'Medium', 'High'])
plt.xlabel('CIRS Class')
plt.ylabel('Count')
plt.savefig('target_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Correlation Heatmap Plot
plt.figure(figsize=(12, 10))
corr_matrix = df.drop(columns=['CIRS_Class']).corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
plt.title('Correlation Heatmap')
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Feature Distributions by Class
features = [col for col in df.columns if col not in ['FloodProbability', 'CIRS_Class']]
fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(20, 16))
axes = axes.flatten()
for i, feature in enumerate(features):
    sns.kdeplot(data=df, x=feature, hue='CIRS_Class', ax=axes[i], common_norm=False, palette='viridis', warn_singular=False)
    axes[i].set_title(f'{feature} Distribution')
for j in range(len(features), len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
plt.savefig('feature_distributions_by_class.png', dpi=150, bbox_inches='tight')
plt.close()


# 3. 80/20 stratified train/test split
print("\nStep 3: Train/Test Split...")
X = df.drop(columns=['FloodProbability', 'CIRS_Class'])
y = df['CIRS_Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4. StandardScaler (fit on train only)
print("\nStep 4: Scaling Data...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train 3 models
print("\nStep 5: Training Models with GridSearchCV...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Logistic Regression
lr = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42)
lr_params = {'C': [0.01, 0.1, 1, 10]}
lr_grid = GridSearchCV(lr, lr_params, scoring='f1_weighted', cv=cv, n_jobs=-1)
print("Training Logistic Regression...")
lr_grid.fit(X_train_scaled, y_train)

# Random Forest
rf = RandomForestClassifier(random_state=42)
rf_params = {'n_estimators': [50, 100], 'max_depth': [10, 20, None], 'min_samples_split': [2, 5]}
rf_grid = GridSearchCV(rf, rf_params, scoring='f1_weighted', cv=cv, n_jobs=-1)
print("Training Random Forest...")
rf_grid.fit(X_train_scaled, y_train)

# XGBoost
xgb = XGBClassifier(objective='multi:softprob', num_class=3, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
xgb_params = {'n_estimators': [50, 100], 'max_depth': [3, 5, 7], 'learning_rate': [0.01, 0.1, 0.2]}
xgb_grid = GridSearchCV(xgb, xgb_params, scoring='f1_weighted', cv=cv, n_jobs=-1)
print("Training XGBoost...")
xgb_grid.fit(X_train_scaled, y_train)


# 6. Evaluate each model
print("\nStep 6: Evaluating Models...")
models = {
    'Logistic Regression': lr_grid.best_estimator_,
    'Random Forest': rf_grid.best_estimator_,
    'XGBoost': xgb_grid.best_estimator_
}

results = []
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (name, model) in enumerate(models.items()):
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_w = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_m = f1_score(y_test, y_pred, average='macro', zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted')

    results.append({
        'Model': name,
        'Accuracy': acc,
        'Precision (Weighted)': prec,
        'Recall (Weighted)': rec,
        'F1-Weighted': f1_w,
        'F1-Macro': f1_m,
        'ROC-AUC (OvR Weighted)': roc_auc
    })

    print(f"\n--- {name} ---")
    print(f"Best Params: {model.get_params() if name == 'Logistic Regression' else (rf_grid.best_params_ if name == 'Random Forest' else xgb_grid.best_params_)}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low', 'Medium', 'High']))

    # Confusion Matrix (row-normalised percentages)
    cm = confusion_matrix(y_test, y_pred, normalize='true') * 100
    sns.heatmap(cm, annot=True, fmt=".1f", cmap="Blues", ax=axes[idx],
                xticklabels=['Low', 'Medium', 'High'], yticklabels=['Low', 'Medium', 'High'])
    axes[idx].set_title(f'{name} CM (%)')
    axes[idx].set_xlabel('Predicted')
    axes[idx].set_ylabel('True')

plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.close()

# 7. Print complete untruncated comparison table; save as model_performance.csv
print("\nStep 7: Comparison Table...")
results_df = pd.DataFrame(results)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(results_df.to_string(index=False))
results_df.to_csv('model_performance.csv', index=False)


# 8. Select best model by F1-Weighted
print("\nStep 8: Selecting Best Model...")
best_model_name = results_df.sort_values(by='F1-Weighted', ascending=False).iloc[0]['Model']
best_model = models[best_model_name]
print(f"Best Model based on F1-Weighted: {best_model_name}")

# Model Comparison Bar Chart
results_df.set_index('Model')[['Accuracy', 'F1-Weighted', 'ROC-AUC (OvR Weighted)']].plot(kind='bar', figsize=(10, 6))
plt.title('Model Comparison')
plt.ylabel('Score')
plt.xticks(rotation=0)
plt.legend(loc='lower right')
plt.savefig('model_comparison_bar_chart.png', dpi=150, bbox_inches='tight')
plt.close()


# 9. Plot feature importance for ALL 3 models side-by-side
print("\nStep 9: Feature Importance...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# LR
lr_importance = np.mean(np.abs(models['Logistic Regression'].coef_), axis=0)
lr_imp_df = pd.DataFrame({'Feature': features, 'Importance': lr_importance}).sort_values('Importance', ascending=True)
axes[0].barh(lr_imp_df['Feature'], lr_imp_df['Importance'], color='skyblue')
axes[0].set_title('Logistic Regression (Mean |coef|)')

# RF
rf_importance = models['Random Forest'].feature_importances_
rf_imp_df = pd.DataFrame({'Feature': features, 'Importance': rf_importance}).sort_values('Importance', ascending=True)
axes[1].barh(rf_imp_df['Feature'], rf_imp_df['Importance'], color='lightgreen')
axes[1].set_title('Random Forest (feature_importances_)')

# XGB
xgb_importance = models['XGBoost'].feature_importances_
xgb_imp_df = pd.DataFrame({'Feature': features, 'Importance': xgb_importance}).sort_values('Importance', ascending=True)
axes[2].barh(xgb_imp_df['Feature'], xgb_imp_df['Importance'], color='salmon')
axes[2].set_title('XGBoost (feature_importances_)')

plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()


# 10. Simulate 4 scenarios using the best model
print("\nStep 10: Scenario Simulation...")
baseline_means = X_train.mean().to_dict()

# Normal (baseline means)
scenario_normal = baseline_means.copy()

# Extreme Rainfall (MonsoonIntensity=10, Watersheds=9, Siltation=9)
scenario_er = baseline_means.copy()
scenario_er.update({'MonsoonIntensity': 10, 'Watersheds': 9, 'Siltation': 9})

# Infrastructure Failure (DrainageSystems=10, RiverManagement=10, DamsQuality=10)
scenario_if = baseline_means.copy()
scenario_if.update({'DrainageSystems': 10, 'RiverManagement': 10, 'DamsQuality': 10})

# Worst-Case Combined (All prior + CoastalVulnerability=10, Deforestation=10)
scenario_wc = scenario_er.copy()
scenario_wc.update({'DrainageSystems': 10, 'RiverManagement': 10, 'DamsQuality': 10, 'CoastalVulnerability': 10, 'Deforestation': 10})

scenarios = [
    ('Normal', scenario_normal),
    ('Extreme Rainfall', scenario_er),
    ('Infrastructure Failure', scenario_if),
    ('Worst-Case Combined', scenario_wc)
]

scenario_results = []
for name, scenario_data in scenarios:
    # Convert to DataFrame to ensure correct order
    df_scenario = pd.DataFrame([scenario_data])[features]

    # Scale
    scaled_scenario = scaler.transform(df_scenario)

    # Predict
    pred_class = best_model.predict(scaled_scenario)[0]
    pred_proba = best_model.predict_proba(scaled_scenario)[0]

    scenario_results.append({
        'Scenario': name,
        'Predicted Class': class_labels[pred_class],
        'Prob_Low': pred_proba[0],
        'Prob_Medium': pred_proba[1],
        'Prob_High': pred_proba[2]
    })

    print(f"\nScenario: {name}")
    print(f"Predicted Class: {class_labels[pred_class]}")
    print(f"Probabilities: Low={pred_proba[0]:.4f}, Medium={pred_proba[1]:.4f}, High={pred_proba[2]:.4f}")

# Scenario Probability Chart
scenario_df = pd.DataFrame(scenario_results)
scenario_df.set_index('Scenario')[['Prob_Low', 'Prob_Medium', 'Prob_High']].plot(kind='bar', stacked=True, figsize=(10, 6), color=['#1f77b4', '#ff7f0e', '#d62728'])
plt.title('Scenario Probabilities')
plt.ylabel('Probability')
plt.xticks(rotation=45)
plt.legend(title='CIRS Class')
plt.savefig('scenario_probability_chart.png', dpi=150, bbox_inches='tight')
plt.close()


# 11. Generate a system architecture diagram (matplotlib only, no graphviz binary)
print("\nStep 11: Architecture Diagram...")
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')

boxes = [
    (0.5, 0.9, '1. Load & Filter Data\n(flood.csv, 14 features)'),
    (0.5, 0.75, '2. Tertile Binning\n(Target: FloodProbability -> Low/Med/High)'),
    (0.5, 0.6, '3. Data Splitting\n(80/20 Stratified Split)'),
    (0.5, 0.45, '4. StandardScaler\n(Fit on Train, Transform Train/Test)'),
    (0.2, 0.3, '5a. Logistic Regression\n(GridSearchCV: C)'),
    (0.5, 0.3, '5b. Random Forest\n(GridSearchCV: n_est, depth, min_split)'),
    (0.8, 0.3, '5c. XGBoost\n(GridSearchCV: n_est, depth, lr)'),
    (0.5, 0.15, '6. Model Evaluation & Selection\n(Select Best by F1-Weighted)'),
    (0.5, 0.0, '7. Scenario Simulation\n(Normal, Extreme, Infra, Worst-case)')
]

for x, y, text in boxes:
    ax.add_patch(patches.Rectangle((x - 0.15, y - 0.05), 0.3, 0.1, fill=True, color='lightblue', ec='black'))
    ax.text(x, y, text, ha='center', va='center', fontsize=9, wrap=True)

# Arrows
arrows = [
    (0.5, 0.85, 0.5, 0.8),
    (0.5, 0.7, 0.5, 0.65),
    (0.5, 0.55, 0.5, 0.5),
    (0.5, 0.4, 0.2, 0.35),
    (0.5, 0.4, 0.5, 0.35),
    (0.5, 0.4, 0.8, 0.35),
    (0.2, 0.25, 0.5, 0.2),
    (0.5, 0.25, 0.5, 0.2),
    (0.8, 0.25, 0.5, 0.2),
    (0.5, 0.1, 0.5, 0.05)
]

for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', lw=1.5))

plt.title('CIRS Prediction Pipeline Architecture')
plt.savefig('architecture_diagram.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nPipeline Complete!")
