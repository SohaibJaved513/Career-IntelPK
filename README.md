# CareerIntelPK - Pakistan Career Intelligence Platform

CareerIntelPK is a Flask-based data analysis and CV skill-gap project built on a Pakistan job-market dataset. It cleans the raw dataset, performs EDA, extracts high-demand skills, shows dashboard insights, and compares a student's CV with market requirements.

## Features

- Dataset preprocessing with Pandas
- Salary range cleaning
- City and sector standardization
- Skill extraction from the dataset
- Role category creation
- EDA output files and charts
- Flask dashboard
- Job explorer with filters
- CV upload and analysis
- Missing skill detection
- Role match scoring
- 30-day learning roadmap
- Clean responsive frontend

## Folder Structure

```text
CareerIntelPK_Complete_Project/
├── app/
│   ├── routes.py
│   ├── services/
│   ├── templates/
│   └── static/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── outputs/
├── scripts/
├── tests/
├── uploads/
├── run.py
├── config.py
└── requirements.txt
```

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/preprocess_data.py
python scripts/run_eda.py
python run.py
```

Open:

```text
http://127.0.0.1:5000/
```

## Test

```bash
python tests/smoke_test.py
```

## Pages

- `/` Home
- `/dashboard` EDA dashboard
- `/jobs` Job explorer
- `/analyzer` CV analyzer
- `/about` Project case study

## Dataset Path

```text
data/raw/pakistan_job_market_dataset.csv
```

## Resume Bullet

Built CareerIntelPK, a Flask-based Pakistan job-market intelligence platform that performs data cleaning, EDA, skill extraction, dashboard reporting, and CV skill-gap analysis using Python, Pandas, Flask, and responsive frontend design.

## Notes

The code is intentionally simple and readable for a student portfolio while keeping a clean project structure.
