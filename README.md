# Cardio Monitor — Heart Dataset Explorer

A Streamlit application for exploring a 13-input K-nearest-neighbors model trained on the bundled Cleveland heart-disease dataset. It presents the source class and model score without assigning an unverified clinical risk meaning.

## What is included

- Interactive input form and dataset visualizations
- Model is trained from `heart.csv` when the app starts
- No database or user-input persistence

## Run locally

```sh
python -m venv .venv
# Activate .venv, then:
python -m pip install -r requirements.txt
streamlit run app.py
```

## Verify

python -m pip install pytest
python -m pytest -q

## Repository map

`app.py` is the Streamlit interface. `model.py` handles data preparation and prediction. `heart.csv` is the bundled dataset; `tests/` covers the model/input contract. `DOCUMENTATION.md` retains additional project notes.

## Evidence and limitations

The bundled data contains 303 records and the model code runs locally. Tests exercise training and input validation; the internal split is not an independent clinical evaluation.

Educational use only; not a medical device or medical advice. The CSV does not establish a trustworthy clinical codebook for class 0/1. Confirm dataset provenance and license before redistribution, and do not use predictions to make care decisions.

## License

See [LICENSE](LICENSE) for the repository license. Dataset and pretrained-model licenses may be separate.
