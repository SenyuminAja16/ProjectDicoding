# Project Dicoding Bike-sharing-dataset

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir Bike-sharing-dataset
cd Bike-sharing-dataset
mkdir dashboard
cd dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```
