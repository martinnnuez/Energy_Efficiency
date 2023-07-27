# Project: Building Energy Efficiency Analysis and Hugging Face Deployment

## [Energy Efficiency Model](https://huggingface.co/spaces/martinnnuez/Energy_Efficiency)

With the increasing importance of addressing climate change and the rise in energy costs, analyzing the energy efficiency of buildings has become crucial. In this project, our focus is to analyze and predict the heat load of buildings based on various building characteristics.

## Objective

The main goal of this project is to utilize Hugging Face's powerful Natural Language Processing (NLP) model to predict the "Heating Load" using different building attributes.

**Note:** The dataset also includes another variable, "Cooling Load," which can be predicted from the provided features. However, our primary focus will be on predicting the "Heating Load" using Hugging Face's NLP model.

## Dataset

**Data source:** [Energy Efficiency Dataset](https://www.kaggle.com/datasets/elikplim/eergy-efficiency-dataset)

The dataset was created by Angeliki Xifara (angxifara '@' gmail.com, Civil/Structural Engineer) and processed by Athanasios Tsanas (tsanasthanasis '@' gmail.com, Oxford Centre for Industrial and Applied Mathematics, University of Oxford, UK).

### Data Set Information:

The dataset comprises 768 samples and 8 features, obtained by energy analysis of 12 different building shapes simulated in Ecotect. Buildings vary in terms of glazing area, glazing area distribution, orientation, and other parameters. The aim is to predict two real-valued responses based on the eight features. Additionally, it can be treated as a multi-class classification problem by rounding the response to the nearest integer.

### Attribute Information:

The dataset contains eight attributes (X1...X8) representing building characteristics and two responses (Y1 and Y2) to be predicted.

Specifically:
* X1 Relative Compactness: This is the volume to surface ratio, where lower compactness indicates larger surface area for a given volume.
* X2 Surface Area ($m^2$)
* X3 Wall Area ($m^2$)
* X4 Roof Area ($m^2$)
* X5 Overall Height ($m$)
* X6 Orientation (2: North, 3: East, 4: South, 5: West)
* X7 Glazing Area (0%, 10%, 25%, 40% of floor area)
    * This refers to the area of transparent material, excluding the window frame.
* X8 Glazing Area Distribution (Variance - 1: Uniform, 2: North, 3: East, 4: South, 5: West)
* Y1 Heating Load ($kWh/m^2$)
* Y2 Cooling Load ($kWh/m^2$)

### Relevant Papers:

A. Tsanas, A. Xifara: 'Accurate quantitative estimation of energy performance of residential buildings using statistical machine learning tools', Energy and Buildings, Vol. 49, pp. 560-567, 2012

### For further details on the data analysis methodology:

A. Tsanas, 'Accurate telemonitoring of Parkinson's disease symptom severity using nonlinear speech signal processing and statistical machine learning', D.Phil. thesis, University of Oxford, 2012

## Getting Started

The following steps describe how to run the project. Detailed explanations of the workflow, scripts, code quality, tests, and how to use the Makefile can be found in the next section.

* Prerequisites
  * Clone the git repository
  * Run `pipenv install --dev`
  * Install git pre-commit: `pre-commit install`
  * Activate the virtual environment: `pipenv shell`
  * To run the code, the data needs to be downloaded: [Energy Efficiency Dataset](https://www.kaggle.com/datasets/elikplim/eergy-efficiency-dataset) and stored in the folders `data`

## Repository Structure

**Problem Description and Exploratory Data Analysis:** 
* EDA.ipynb: Notebook containing exploratory data analysis

**Data Preparation, Model Training, Tracking, and Deployment:** 
* Model Used: XGBoost for Regression
* Environment:
    * The required packages are saved in Pipfile
    * Run `pipenv install --dev`
    * The environment can be started with `pipenv shell`
* Starting the Server
    * Start the server for tracking and model registry: `mlflow server --backend-store-uri sqlite:///mlruns.db --default-artifact-root artifacts`
* Training
    * To run only training with experiment tracking and model registry, use `experiment_tracking.py` and run it with: `python3 experiment_tracking.py --input-data <path/to/input-data.csv> --output <path/to/output>` (and optional other parameters)
* Hyperparameter Tuning
    * Hyperparameter tuning is done via Optuna
    * The number of trials for hyperparameter tuning can be changed using the parameter `n-trials`, with the default value set to 20, e.g., `python3 experiment_tracking.py --n-trials 50`. For the final `prefect_deploy.py` file, you need to change it directly in the script.
    * Model parameters for hyperparameter tuning can also be changed via the command line, e.g., `n-estimators`, `max-depth`, `gamma`, `eta`, etc., for `experiment_tracking.py`. For the final script, they need to be changed in the script.
* Mlflow Experiment Tracking and Model Registry
    * Mlflow tracking server: sqlite database
    * Mlflow backend store: sqlite database
    * Mlflow artifacts store: local filesystem
    * The best model (lowest validation metric: RMSE) is automatically registered using Mlflow. Note: Even better would be to compare with the previously registered model and only register the new one if it is better than the previous one.
    * The experiment tracking and model registry UI can be accessed via `localhost:5000` in the browser
* Orchestration using Prefect
    * The `main` function is turned into a Prefect `flow`
    * The functions `read_data`, `normalize`, `onehot`, and `training` are turned into tasks
    * To use the Prefect UI, use `prefect orion start` and browse to `localhost:4200`
    * To start a Prefect flow (without deployment), use the script `prefect_flow.py`. It is equivalent to `experiment_tracking.py`, but includes a Prefect flow and tasks
    * A deployment is used to run the script every 5 minutes. `prefect deployment create prefect-deploy.py`
    * To run the Prefect deployment, use `prefect deployment create prefect_deploy.py`
    * Note: To create the deployment, I had to change the code slightly compared to `exp-tracking.py` and `prefect_flow.py` as the argparse is not working (and also not useful) when the flow is scheduled.
    * Create a work queue in the UI (navigate to `localhost:4200`), as shown in video 3.5 of the course
    * Spin up an agent: `prefect agent start <workqueue-id>`, e.g., `prefect agent start a4bdb288-7329-4a1c-992f-fe62cd898af9`

**Deploy Model as a Web Service on Hugging Face** 
* The model is deployed on Hugging Face Spaces
* Model and artifacts are available for use in the following Hugging Face Space: [Energy Efficiency Model](https://huggingface.co/spaces/martinnnuez/Energy_Efficiency)

**Code Quality**
* I used linting for the code quality.
* `black` was used to improve the formatting: `black .`
* `isort` was used to organize the imports: `isort .`
* In `pyproject.toml`, exceptions are defined.
* Git pre-commit hooks are defined in `.pre-commit-config.yaml`.
