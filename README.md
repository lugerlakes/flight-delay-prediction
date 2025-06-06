# ✈️ Flight Delay Prediction

Predictive analytics project aimed at estimating the likelihood of delays in flights operated from/to Santiago Airport (SCL) in 2017. Includes exploratory data analysis, feature engineering, supervised model training, and robust evaluation with a reproducible approach.

## 🧠 Goals
- Analyze flight delays at SCL airport during 2017
- Create meaningful synthetic features
- Train classification models to predict delays
- Evaluate performance and identify key drivers of delay

## 📁 Project Structure
```
flight-delay-prediction/
├── data/ # Original and processed datasets
│ ├── raw/ # Raw CSV files (original flight data)
│ └── processed/ # Cleaned data with engineered features
├── models/ # Serialized trained models
├── notebooks/ # Jupyter notebooks for EDA and modeling
│ └── solution.ipynb # Main notebook with full workflow
├── reports/ # Final reports and visualizations
│ └── figures/ # Saved plots from EDA and modeling
├── src/ # Modular source code for reuse
│ ├── init.py
│ ├── data/ # Data loading and preprocessing logic
│ │ ├── load_data.py
│ │ └── preprocess.py
│ ├── features/ # Feature engineering scripts
│ │ └── build_features.py
│ ├── models/ # Training and evaluation scripts
│ │ ├── train_model.py
│ │ └── evaluate_model.py
│ └── visualization/ # Custom visualizations
│ └── visualize.py
├── tests/ # Unit and integration tests
│ ├── test_features.py
│ ├── test_visualize.py
│ └── test_visualize_advanced.py
├── .gitignore # Files/folders to exclude from git
├── LICENSE # Project license
├── README.md # Project overview and documentation
└── requirements.txt # Project dependencies
```
---
## 📦 Installation
This project requires **Python = 3.10**
1. Clone the repository:
```bash
   git clone https://github.com/lugerlakes/flight-delay-prediction.git
   cd flight-delay-prediction
```
2. Create and activate a virtual environment
- (Option A) with venv:
```bash
    python -m venv .flight-delay-prediction
    .\.flight-delay-prediction\Scripts\activate  # On Windows
    source .flight-delay-prediction/bin/activate # On macOS/Linux
```
- (Option B) Or use conda:
```bash
    conda create --name flight-delay-prediction python=3.10
    conda activate flight-delay-prediction
```
3. Install dependencies:
```bash
    pip install -r requirements.txt
```
---

### Key Dependencies
- Python:
    - pandas
    - numpy
    - matplotlib
    - seaborn
    - scikit-learn
    - xgboost
    - jupyter

## 🚀 How to Run

### 🔍 Exploratory Analysis and Modeling

Open the notebook:
```bash
jupyter notebook notebooks/solution.ipynb
```
Follow the sections for:

- Data loading and cleaning

- Feature engineering

- Exploratory data analysis (EDA)

- Model training and evaluation

## ✅ Run tests and visualizations
From the project root:
```bash
# Run feature pipeline test
python tests/test_features.py
```
```bash
# Run EDA visualizations
python tests/test_visualize.py
```
```bash
# Run advanced grouped plots
python tests/test_visualize_advanced.py
```
Visual outputs will be saved to reports/figures/.