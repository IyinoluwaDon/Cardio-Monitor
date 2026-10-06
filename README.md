<h1><img src="static/heartlogo.png" width="50px" /> Cardio Monitor</h1>

**A Streamlit web app that estimates your risk of heart disease from 13 clinical inputs.**

Built and maintained by **[Iyinoluwa Don-Taiwo](https://github.com/IyinoluwaDon)**.

The model is a K-Nearest Neighbors classifier (k = 7, min-max scaling) trained on the UCI Cleveland heart disease dataset (`heart.csv`, 303 records). It reaches about **90% accuracy** on a held-out 20% test split.

> **Disclaimer:** This is an educational project. It is not medical advice. See a doctor if you have symptoms or concerns.

## Features

- Predict page with a clean form for all 13 inputs
- Low-risk or high-risk result with a model confidence estimate
- Charts that compare your values to the typical low-risk group
- "About heart disease" page covering types, symptoms, risk factors, and prevention
- No database. Nothing you enter is stored. The model trains from `heart.csv` when the app starts

## Run it locally

```bash
git clone https://github.com/IyinoluwaDon/Cardio-Monitor.git
cd Cardio-Monitor
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL that Streamlit prints (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud

1. Push this repo to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Pick the repo, set the main file to `app.py`, and deploy.

## Project structure

```
Cardio-Monitor/
├── app.py              # Streamlit interface (Predict and About pages)
├── model.py            # Data loading, encoding maps, model training, prediction
├── heart.csv           # Training data
├── requirements.txt
├── static/             # Logo and About page slides
├── .streamlit/         # Theme config
└── heart disease prediction/   # Original EDA and research notebooks
```

## How it works

1. `model.py` loads `heart.csv`, scales every feature to 0-1, and fits a KNN classifier.
2. `app.py` turns your form answers into the same numeric codes the dataset uses.
3. The model returns a class (1 = low risk, 0 = high risk) and the share of neighbors that voted low risk.
4. Streamlit caches the trained model, so predictions are instant after the first load.

## What changed from the original Flask version

- Moved the whole interface from Flask and HTML templates to Streamlit
- Removed MongoDB, the hit counters, and all stored user data
- Removed the pickled model files, which break on current scikit-learn. The model now trains from the CSV at startup
- Fixed sex encoding. The old code sent `Male` but checked for `male`, so every user was scored as female
- Fixed the `thal` encoding so it matches the dataset (1 fixed, 2 normal, 3 reversible)
- Fixed the chest pain mismatch between the prediction and chart code
- Relabeled the chart baseline as the typical low-risk value. The old "Normal Value" was actually the high-risk group average

## Credits and license

Copyright (c) 2026 Iyinoluwa Don-Taiwo, Streamlit edition.

This project is a derivative of the original Flask app [Cardio-Monitor](https://github.com/shsarv/Cardio-Monitor) by Sarvesh Kumar Sharma, created as a Big Data Analytics course project. The EDA notebooks in `heart disease prediction/` come from that original work. See [LICENSE](LICENSE).

Dataset: UCI Heart Disease (Cleveland).
