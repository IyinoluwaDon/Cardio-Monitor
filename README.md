# Cardio Monitor: Cleveland Heart-Disease Data Explorer

A Streamlit application that explores the bundled 303-record Cleveland heart-disease dataset and trains a 13-input K-nearest-neighbors classifier from `heart.csv` when the app starts. The interface combines dataset visualizations, an input form, and model output; `model.py` contains feature preparation and prediction code.

## Run locally

```sh
python -m venv .venv
# Activate .venv, then:
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the model and input-contract checks with `python -m pytest -q`. `DOCUMENTATION.md` contains additional project notes.
