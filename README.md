# 100-App Product Ops Research

## Run

Requires Python 3.10+.

```bash
python research.py
python -m http.server 8080
```

Open `http://localhost:8080/index.html`.

## Outputs

- `apps.csv`: normalized 100-app input set
- `research.csv`: skimmable research matrix
- `research.json`: machine-readable matrix used by the page
- `index.html`: self-explanatory case study

## Agent/pipeline

`research.py` is the reproducible classification pipeline. It normalizes the app set and classifies auth, access, API breadth, known MCP support, buildability and evidence. Official docs are used to correct the script in a verification pass. No paid app accounts or credentials are required.

The pipeline is designed for agent-assisted execution: app discovery and classification are deterministic and rerunnable, while uncertain auth, gate, and MCP claims are retained for human/documentation verification rather than presented as confirmed facts.

## Architecture

1. `apps.csv` is the normalized research input.
2. `research.py` performs reproducible deterministic classification.
3. Official documentation URLs are attached to each app.
4. The HTML consumes `research.json` and provides search, filters, sorting, charts, and downloads.
5. Paid-account or partner-gated findings are reported as findings, not research failures.

## Verification

The page reports a 30-app documentation spot-check and distinguishes the first pass from the corrected pass. It also explicitly labels categories and app records where public evidence was missing or an approval/paid-plan gate is the main finding. The full check list is available in `verification.csv`.
