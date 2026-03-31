import graphviz

dot = graphviz.Digraph(comment='Community Isolation Risk Prediction Architecture', format='png')
dot.attr(rankdir='TD', dpi='300', size='10,10', bgcolor='white', fontname='Helvetica')

# Set default node attributes
dot.attr('node', shape='box', style='filled', fontname='Helvetica', color='#333333', penwidth='1.5')
dot.attr('edge', color='#666666', penwidth='1.5', fontname='Helvetica')

# Data Nodes
dot.node('A', 'Raw Dataset ZIP\n(Dataset Upload)', fillcolor='#f9f2fb')
dot.node('C1', 'train.csv', fillcolor='#f9f2fb', shape='cylinder')
dot.node('C2', 'test.csv', fillcolor='#f9f2fb', shape='cylinder')
dot.node('C3', 'sample_submission.csv', fillcolor='#f9f2fb', shape='cylinder')

# Process Nodes
dot.node('B', 'Data Extraction', fillcolor='#e6f2ff')
dot.node('D', 'Data Cleaning &\nHandling Missing Values', fillcolor='#e6f2ff')
dot.node('E', 'Exploratory Data Analysis (EDA)', fillcolor='#e6f2ff')
dot.node('F', 'Insights\n(Plots & Correlations)', fillcolor='#fff2e6', shape='note')
dot.node('G', 'Feature Engineering\n(Scaling, Encoding, Target Transform)', fillcolor='#e6f2ff')

# Feature Outputs
dot.node('G1', 'Scaled Numerical Features', fillcolor='#e6ffe6')
dot.node('G2', 'Derived Features\n(Vulnerability, Impact)', fillcolor='#e6ffe6')
dot.node('G3', 'Target Transformation\n(Isolation Risk Score)', fillcolor='#e6ffe6')

# Modeling Nodes
dot.node('H', 'Model Training &\nValidation Split (80/20)', fillcolor='#e6f2ff')
dot.node('I1', 'Linear Regression\n(Baseline)', fillcolor='#e6ffe6', shape='component')
dot.node('I2', 'Random Forest Regressor\n(Ensemble)', fillcolor='#e6ffe6', shape='component')
dot.node('I3', 'XGBoost Regressor\n(Gradient Boosting)', fillcolor='#e6ffe6', shape='component')

# Evaluation & Output Nodes
dot.node('J', 'Model Evaluation\n(RMSE, MAE, R²)', fillcolor='#e6f2ff')
dot.node('K', 'Model Interpretation\n(SHAP Values)', fillcolor='#e6f2ff')
dot.node('L', 'Feature Importance &\nInsight Generation', fillcolor='#f9f2fb')
dot.node('M', 'Predict on Test Data\n(Select Best Model)', fillcolor='#e6f2ff')
dot.node('N', 'Final submission.csv', fillcolor='#f9f2fb', shape='note')

# Edges
dot.edge('A', 'B')
dot.edge('B', 'C1')
dot.edge('B', 'C2')
dot.edge('B', 'C3')

dot.edge('C1', 'D')
dot.edge('C2', 'D')

dot.edge('D', 'E')
dot.edge('E', 'F', label=' generates')

dot.edge('D', 'G')
dot.edge('G', 'G1')
dot.edge('G', 'G2')
dot.edge('G', 'G3')

dot.edge('G1', 'H')
dot.edge('G2', 'H')
dot.edge('G3', 'H')

dot.edge('H', 'I1')
dot.edge('H', 'I2')
dot.edge('H', 'I3')

dot.edge('I1', 'J')
dot.edge('I2', 'J')
dot.edge('I3', 'J')

dot.edge('J', 'K')
dot.edge('K', 'L')

dot.edge('J', 'M', label=' Best Model')
dot.edge('C3', 'M')
dot.edge('M', 'N')

dot.render('architecture_diagram', view=False)
print("Architecture diagram saved as architecture_diagram.png")
