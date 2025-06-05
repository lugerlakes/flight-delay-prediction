# ✈️ Flight Delay Prediction

Predictive analytics project aimed at estimating the likelihood of delays in flights operated from/to Santiago Airport (SCL) in 2017. Includes exploratory data analysis, feature engineering, supervised model training, and robust evaluation with a reproducible approach.

## 📁 Project Structure

```
flight-delay-prediction/
├── data/                       # Data directory
│   ├── raw/                    # Original/raw data
│   └── processed/              # Processed data with engineered features
├── models/                     # Trained or serialized models
├── notebooks/                  # Jupyter Notebooks for exploration and modeling
│   └── flight_delay_prediction.ipynb          # Main analysis notebook
├── reports/                    # Generated analysis reports and final visuals
│   └── figures/                # Plots and charts for reporting and EDA
├── src/                        # Source code for use in this project
│   ├── __init__.py             # Makes src a Python module
│   ├── data/                   # Data loading and cleaning scripts
│   │   ├── load_data.py        # Functions to load raw and processed data
│   │   └── preprocess.py       # Data cleaning and preparation logic
│   ├── features/               # Feature engineering code
│   │   └── build_features.py   # Scripts to create and export features
│   ├── models/                 # Model training and evaluation logic
│   │   ├── train_model.py      # Model training pipeline
│   │   └── evaluate_model.py   # Evaluation and validation utilities
│   └── visualization/          # Custom visualization functions
│       └── visualize.py        # Plots for EDA and results presentation
├── .gitignore                  # Files and folders to be ignored by git
├── LICENSE                     # License for the project
├── README.md                   # Project overview and documentation
└── requirements.txt            # List of Python dependencies
```
## Environment Setup
This project requires **Python ≥ 3.11**

---

1. **Clone the repository:**
 ```bash
    git clone https://github.com/lugerlakes/flight-delay-prediction.git
    cd covid-nhmm
```
2. Create and activate the virtual environment:

```bash
    python3 -m venv flight-delay-prediction
    source flight-delay-prediction/bin/activate
```
3. Install dependencies:

```bash
    pip install -r requirements.txt
```
---

## Key Dependencies
- Python:
    - pandas
    - numpy
    - matplotlib
    - seaborn
    - scikit-learn
    - xgboost
    - jupyter

