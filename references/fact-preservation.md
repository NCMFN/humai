# Fact Preservation Rules

When rewriting AI-generated text to humanize it, the following rules apply:

1. **Never Change Numbers:** Any specific figures, quantities, metrics, dates, times, and years must remain unchanged. (e.g., 2021, 24,877 TWh, 39%, RMSE = 0.129 kWh).
2. **Never Change Proper Nouns:** Names of people, organizations, locations, systems, models, and protocols must be preserved exactly. (e.g., XGBoost, LightGBM, CatBoost, ARIMAX, University of Uyo, Smart Home Energy).
3. **Preserve Academic/Technical Terms:** Do not invent synonyms for established terminology. If the original says "TimeSeriesSplit cross-validation," keep it as "TimeSeriesSplit cross-validation."
4. **Preserve Acronyms:** Maintain the usage of acronyms such as STLF, RMSE, SHAP, GBDTs, SMH, HPC exactly as written.
5. **Preserve Formulas and Math Notation:** Any equations, mathematical symbols, or Greek letters must remain untouched.
6. **Citations:** Maintain the integrity of all citations and references (e.g., [1], [5], [9]). Do not remove them or alter their format.

**Objective:** The core message and factual claims must remain perfectly intact. The goal is to change *how* the information is presented (rhythm, voice, vocabulary), not *what* information is presented.