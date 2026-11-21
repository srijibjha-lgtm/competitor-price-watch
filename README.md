# Competitor & Pricing Watch Agent

*Part of the Agentic AI in Practice project collection. All companies, people and data are fictional or sample data.*

**Business problem:** Slow, risky reaction to competitor price cuts.

**Where people stay in charge:** A pricing manager approves every change; the floor margin and the 8% weekly limit are enforced by code.

Full project write-up: [`p16_competitor_price_watch/README.md`](p16_competitor_price_watch/README.md).

## What's inside

| Path | What it is |
|---|---|
| `p16_competitor_price_watch/p16_competitor_price_watch.ipynb` | Self-contained Colab notebook (sample data built in) |
| `p16_competitor_price_watch/app.py` | Streamlit app |
| `p16_competitor_price_watch/core.py` | The project's logic, used by the app |
| `p16_competitor_price_watch/demo.py` | The notebook walkthrough as a script |
| `p16_competitor_price_watch/data/` | Sample data |
| `common/agentkit.py` | Shared toolkit: Groq model wrapper, bounded tool loop, evidence checks, approval queue, audit log |
| `common/ui.py` | Shared Streamlit helpers |
| `tools/make_marketing_data.py` | Regenerates the sample data |

## Cost: free

Uses the Groq free tier (no credit card). Create a key at console.groq.com → API Keys. Over the limit, the code waits; you are never charged.

## Run the notebook in Google Colab

1. Upload `p16_competitor_price_watch/p16_competitor_price_watch.ipynb` to Colab (File → Upload notebook).
2. Click the key icon in Colab's left sidebar, add a secret named `GROQ_API_KEY`, and allow notebook access.
3. Runtime → Run all.

## Run the app on your laptop

```bash
pip install -r requirements.txt
streamlit run p16_competitor_price_watch/app.py
```

Paste your Groq key in the sidebar, or copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill it in.

## Deploy free on Streamlit Community Cloud

1. Push this folder to a public GitHub repository (never commit `secrets.toml`).
2. On share.streamlit.io choose *Create app*, pick the repo and set the main file to `p16_competitor_price_watch/app.py`.
3. In the app's *Settings → Secrets* add `GROQ_API_KEY = "…"`.

## Notes

- If a Groq model is retired, change `DEFAULT_MODEL` / `VISION_MODEL` in `common/agentkit.py` or the model box in the app's sidebar.
- The app and notebook write logs and output files into `data/`. Re-download to reset.
- Use only sample data: free AI tiers may use inputs to improve their products.
