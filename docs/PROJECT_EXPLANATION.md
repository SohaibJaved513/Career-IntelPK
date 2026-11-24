# CareerIntelPK Project Explanation

## Dataset

The project uses the uploaded Kaggle CSV file:

`data/raw/pakistan_job_market_dataset.csv`

Raw rows: 10500
Clean rows after preprocessing: 10500

## What I Did

1. Loaded the job-market dataset using Pandas.
2. Checked columns, missing values, and record counts.
3. Cleaned city names, company names, salary ranges, dates, vacancies, and skills.
4. Converted salary ranges into minimum, maximum, and average salary fields.
5. Split the required skills column into individual skills.
6. Created role categories from job titles and sectors.
7. Saved clean CSV files for the Flask app.
8. Built dashboard pages using Flask templates.
9. Added a CV analyzer that reads PDF, DOCX, or TXT files.
10. Compared CV skills with top market skills and generated a learning roadmap.

## Main Output Files

- `data/processed/clean_jobs.csv`
- `data/processed/skill_counts.csv`
- `data/processed/city_counts.csv`
- `data/processed/sector_counts.csv`
- `data/processed/role_counts.csv`
- `outputs/figures/*.png`

## Simple Pipeline

Raw Data → Cleaning → EDA → Skill Counts → Flask Dashboard → CV Analyzer
