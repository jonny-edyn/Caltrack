# Caltrack Airtable Web Dashboard

A live Streamlit webpage that reads the Caltrack Airtable base.

## Airtable base

- Base ID: `appD9LwNGFQLeRwOI`
- Tables: `Meals`, `Weigh-ins`, `Profile`

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p .streamlit
```

Create `.streamlit/secrets.toml`:

```toml
AIRTABLE_TOKEN = "your-airtable-personal-access-token"
AIRTABLE_BASE_ID = "appD9LwNGFQLeRwOI"
```

Then run:

```bash
streamlit run app.py
```

## Host online

1. Create a private GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Create a Streamlit Community Cloud app using `app.py`.
4. Add the same two values in the app's Secrets settings.
5. Deploy.

The Airtable token should have read access to the Caltrack base and should never be committed to GitHub.
