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
├── data/ # Data directory
│ ├── raw/ # Original/raw data
│ └── processed/ # Processed data with engineered features
├── models/ # Trained or serialized models
├── notebooks/ # Jupyter notebooks for exploration and modeling
│ └── solution.ipynb # Main notebook with EDA, features and modeling
├── reports/ # Generated reports and final visual outputs
│ └── figures/ # Visualizations saved from EDA or modeling
├── src/ # Source code for modular and reusable logic
│ ├── init.py 
│ ├── data/ # Data loading and preprocessing scripts
│ │ ├── load_data.py # Function to read raw CSV files
│ │ └── preprocess.py # Parsing and cleaning logic
│ ├── features/ # Feature engineering logic
│ │ └── build_features.py # Functions to create and export features
│ ├── models/ # Model training and evaluation logic
│ │ ├── train_model.py # Training pipeline
│ │ └── evaluate_model.py # Evaluation metrics and analysis
│ └── visualization/ # Custom visualization utilities
│ └── visualize.py # EDA and reporting plots
├── tests/ # Unit tests and exploratory script runners
│ ├── test_features.py # Test feature generation pipeline
│ ├── test_visualize.py # Basic EDA visualization checks
│ └── test_visualize_advanced.py # Advanced visual analytics by category
├── .gitignore # Files/directories to ignore in version control
├── LICENSE # License file
├── README.md # Project documentation and structure
└── requirements.txt # Python dependencies
```
---
## 📦 Installation
This project requires **Python = 3.10**
1. Clone the repository:
```bash
   git clone https://github.com/lugerlakes/flight-delay-prediction.git
   cd flight-delay-prediction
```
2. - (Option A) Create and activate a virtual environment with venv:
```bash
    python -m venv .flight-delay-prediction
    .\.flight-delay-prediction\Scripts\activate  # On Windows
    source .flight-delay-prediction/bin/activate # On macOS/Linux
```
- (Option B) Or use conda to create the environment:
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