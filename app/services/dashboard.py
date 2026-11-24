from app.services.store import jobs_df, skills_df


def home_snapshot():
    df = jobs_df()
    skills = skills_df()

    if df.empty:
        return {
            "jobs": 0,
            "companies": 0,
            "cities": 0,
            "sectors": 0,
            "vacancies": 0,
            "skills": [],
        }

    return {
        "jobs": len(df),
        "companies": df["company"].nunique(),
        "cities": df["city"].nunique(),
        "sectors": df["sector"].nunique(),
        "vacancies": int(df["vacancies"].astype(int).sum()),
        "skills": skills.head(8).to_dict("records"),
    }


def dashboard_data():
    df = jobs_df()
    skills = skills_df()

    if df.empty:
        return {}

    salary = df[df["salary_avg"] != ""].copy()
    salary["salary_avg"] = salary["salary_avg"].astype(float)

    return {
        "summary": {
            "jobs": len(df),
            "companies": df["company"].nunique(),
            "cities": df["city"].nunique(),
            "sectors": df["sector"].nunique(),
            "vacancies": int(df["vacancies"].astype(int).sum()),
            "avg_salary": round(salary["salary_avg"].mean(), 0) if not salary.empty else 0,
        },
        "top_cities": list(df["city"].value_counts().head(8).items()),
        "top_sectors": list(df["sector"].value_counts().head(8).items()),
        "top_roles": list(df["role_category"].value_counts().head(8).items()),
        "top_skills": skills.head(15).to_dict("records"),
        "job_types": list(df["job_type"].value_counts().head(6).items()),
        "education": list(df["education_level"].value_counts().head(6).items()),
        "experience": list(df["experience_required"].value_counts().head(6).items()),
    }


def filtered_jobs(city="", sector="", limit=120):
    df = jobs_df()

    if df.empty:
        return [], {"cities": [], "sectors": []}

    filters = {
        "cities": sorted(df["city"].dropna().unique().tolist()),
        "sectors": sorted(df["sector"].dropna().unique().tolist()),
    }

    if city:
        df = df[df["city"] == city]

    if sector:
        df = df[df["sector"] == sector]

    cols = [
        "title",
        "company",
        "city",
        "sector",
        "role_category",
        "salary_range",
        "experience_required",
        "job_type",
        "education_level",
        "skills_text",
    ]

    return df[cols].head(limit).to_dict("records"), filters
