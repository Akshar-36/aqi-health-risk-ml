# AQI and Health Risk Prediction Using Machine Learning

## Project Overview
This project predicts Air Quality Index (AQI) values and associated respiratory health risks in India using machine learning models. It integrates environmental data from CPCB with health statistics, performing data preprocessing, exploratory analysis, and modeling to assess health risks and aid policy decisions.

---

## Repository Structure

- `India_AQI_Health_Pipeline.ipynb`  
  Main Jupyter notebook that includes data loading, preprocessing, modeling, evaluation, and visualization steps.

- `Data_loading.py`  
  Python script to load and merge various raw datasets such as CPCB AQI data and health records.

- `Data_processing.py`  
  Contains data cleaning, feature engineering (e.g., month mapping), missing value handling, and type conversion functions.

- `requirements.txt`  
  Lists necessary Python packages and dependencies for reproducing the environment.

---

## Getting Started

### Prerequisites
- Python 3.8 or above  
Recommended packages include `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, and `seaborn`.

---

### File Setup & Data Paths

- Raw datasets (CPCB AQI data, health statistics) should be placed inside a `data/` directory within the repo (you need to create this).
- File paths in scripts/notebooks use relative paths like `'data/cpcb_aqi.csv'` to load data.
- Adjust file names and paths in `Data_loading.py` if your data is named or stored differently.

---

### Running the Project

1. **Load Data:** Execute `Data_loading.py` or run the data loading cells in the notebook to import raw datasets.  
2. **Preprocess Data:** Clean, merge, handle missing values, and engineer features using `Data_processing.py` functions or notebook cells.  
3. **Exploratory Data Analysis:** Visualize distributions and correlations to understand data patterns.  
4. **Train-Test Split:** Split data using an 80:20 ratio with fixed random seed (`random_state=42`) for reproducibility.  
5. **Modeling:** Train Random Forest and XGBoost models on the training data.  
6. **Evaluation:** Assess model performance with R² and MSE metrics; plot actual vs predicted values.  
7. **Health Risk Assessment:** Use model predictions to estimate respiratory cases and visualize on maps/charts.  
8. **Result Presentation:** Prepare final visualizations and reports.

---

## Notes & Tips

- Make sure your data files have consistent formats (dates, locations, column names) as expected by the preprocessing code.  
- Customize feature selections and hyperparameters in the notebook to optimize model results.

---

## Contact and Contributions

For questions or contributions, please open an issue or submit a pull request. This project is intended for academic research and can be extended with additional datasets or forecasting methods.


