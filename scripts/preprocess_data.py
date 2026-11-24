from pathlib import Path
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "pakistan_job_market_dataset.csv"
OUT_DIR = ROOT / "data" / "processed"


def text_clean(value):
    if pd.isna(value):
        return ""
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9+#.\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def city_clean(value):
    if pd.isna(value):
        return "Unknown"
    value = str(value).strip().lower()
    fixes = {
        "karachi": "Karachi", "lahore": "Lahore", "islamabad": "Islamabad",
        "rawalpindi": "Rawalpindi", "faisalabad": "Faisalabad", "multan": "Multan",
        "peshawar": "Peshawar", "quetta": "Quetta", "hyderabad": "Hyderabad",
        "sialkot": "Sialkot", "gujranwala": "Gujranwala", "sukkur": "Sukkur",
        "bahawalpur": "Bahawalpur", "abbottabad": "Abbottabad"
    }
    return fixes.get(value, value.title())


def salary_split(value):
    nums = re.findall(r"\d[\d,]*", str(value))
    nums = [int(x.replace(",", "")) for x in nums]
    if len(nums) >= 2:
        return nums[0], nums[1]
    if len(nums) == 1:
        return nums[0], nums[0]
    return np.nan, np.nan


def skill_list(value):
    if pd.isna(value):
        return []
    skills = []
    for item in str(value).split(","):
        item = re.sub(r"\s+", " ", item.strip())
        if item:
            skills.append(item)
    return sorted(set(skills))


def role_category(title, sector):
    text = text_clean(title)
    sec = text_clean(sector)

    if any(x in text for x in ["data scientist", "machine learning", "ml engineer", "ai engineer", "artificial intelligence", "deep learning"]):
        return "AI & Data Science"
    if any(x in text for x in ["data analyst", "business analyst", "analyst", "bi analyst", "power bi"]):
        return "Data / BI Analyst"
    if any(x in text for x in ["software", "developer", "engineer", "frontend", "backend", "full stack", "python", "java", "react", "flutter"]):
        return "Software Development"
    if any(x in text for x in ["finance", "account", "audit", "bank", "compliance"]):
        return "Finance"
    if any(x in text for x in ["marketing", "sales", "seo", "content", "social media"]):
        return "Marketing & Sales"
    if any(x in text for x in ["teacher", "lecturer", "trainer", "instructor"]):
        return "Education"
    if any(x in text for x in ["doctor", "nurse", "medical", "pharmacist", "health"]):
        return "Healthcare"
    if "it" in sec or "technology" in sec:
        return "Technology"

    return "Other"


def get_column(df, name, default=""):
    if name in df.columns:
        return df[name]
    return pd.Series([default] * len(df))


def main():
    raw = pd.read_csv(RAW_PATH)
    raw.columns = [str(c).strip() for c in raw.columns]

    clean = pd.DataFrame()
    clean["job_id"] = range(1, len(raw) + 1)
    clean["title"] = get_column(raw, "Job Title", "Unknown").fillna("Unknown").astype(str).str.strip()
    clean["company"] = get_column(raw, "Company", "Unknown").fillna("Unknown").astype(str).str.strip().str.title()
    clean["city"] = get_column(raw, "City", "Unknown").apply(city_clean)
    clean["sector"] = get_column(raw, "Sector", "Unknown").fillna("Unknown").astype(str).str.strip()
    clean["salary_range"] = get_column(raw, "Salary Range (PKR)", "Not Mentioned").fillna("Not Mentioned").astype(str)
    clean[["salary_min", "salary_max"]] = clean["salary_range"].apply(lambda x: pd.Series(salary_split(x)))
    clean["salary_avg"] = clean[["salary_min", "salary_max"]].mean(axis=1)
    clean["required_skills"] = get_column(raw, "Required Skills", "").fillna("").astype(str)
    clean["skill_list"] = clean["required_skills"].apply(skill_list)
    clean["skills_text"] = clean["skill_list"].apply(lambda x: ", ".join(x))
    clean["skill_count"] = clean["skill_list"].apply(len)
    clean["experience_required"] = get_column(raw, "Experience Required", "Not Mentioned").fillna("Not Mentioned").astype(str).str.strip()
    clean["job_type"] = get_column(raw, "Job Type", "Not Mentioned").fillna("Not Mentioned").astype(str).str.strip()
    clean["education_level"] = get_column(raw, "Education Level", "Not Mentioned").fillna("Not Mentioned").astype(str).str.strip()
    clean["gender_preference"] = get_column(raw, "Gender Preference", "No Preference").fillna("No Preference").astype(str).str.strip()
    clean["vacancies"] = pd.to_numeric(get_column(raw, "Number of Vacancies", 0), errors="coerce").fillna(0).astype(int)
    clean["posted_date"] = pd.to_datetime(get_column(raw, "Posted Date", ""), errors="coerce")
    clean["application_deadline"] = pd.to_datetime(get_column(raw, "Application Deadline", ""), errors="coerce")
    clean["days_to_apply"] = (clean["application_deadline"] - clean["posted_date"]).dt.days
    clean["role_category"] = clean.apply(lambda row: role_category(row["title"], row["sector"]), axis=1)
    clean["clean_title"] = clean["title"].apply(text_clean)
    clean["clean_skills"] = clean["required_skills"].apply(text_clean)

    clean = clean.drop_duplicates(subset=["title", "company", "city", "required_skills"]).reset_index(drop=True)
    clean["job_id"] = range(1, len(clean) + 1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUT_DIR / "clean_jobs.csv", index=False)

    skills = clean["skills_text"].str.split(", ").explode().dropna()
    skills = skills[skills.astype(str).str.strip() != ""]
    skill_counts = skills.value_counts().reset_index()
    skill_counts.columns = ["skill", "job_count"]
    skill_counts.to_csv(OUT_DIR / "skill_counts.csv", index=False)

    city_counts = clean["city"].value_counts().reset_index()
    city_counts.columns = ["city", "job_count"]
    city_counts.to_csv(OUT_DIR / "city_counts.csv", index=False)

    sector_counts = clean["sector"].value_counts().reset_index()
    sector_counts.columns = ["sector", "job_count"]
    sector_counts.to_csv(OUT_DIR / "sector_counts.csv", index=False)

    role_counts = clean["role_category"].value_counts().reset_index()
    role_counts.columns = ["role_category", "job_count"]
    role_counts.to_csv(OUT_DIR / "role_counts.csv", index=False)

    print("Preprocessing completed.")
    print(f"Clean rows: {len(clean)}")


if __name__ == "__main__":
    main()
