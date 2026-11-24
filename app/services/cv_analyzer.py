from app.services.cv_parser import extract_text
from app.services.store import jobs_df, skills_df
from app.services.text_utils import find_skills


ROLE_SKILLS = {
    "AI & Data Science": ["Python", "Machine Learning", "Power BI", "SQL", "Data Analysis", "Forecasting", "Statistics", "Data Collection Tools"],
    "Data / BI Analyst": ["MS Excel", "SQL", "Power BI", "Financial Analysis", "Reporting", "Data Collection Tools", "SPSS"],
    "Software Development": ["Python", "PHP", "FastAPI", "Git", "Flutter", "React Native", "SQL", "Redis"],
    "Finance": ["MS Excel", "Financial Analysis", "Financial Modeling", "IFRS", "Credit Appraisal", "Risk Management"],
    "Marketing & Sales": ["Market Research", "Marketing Analytics", "Sales Strategy", "Negotiation", "Nielsen"],
    "Education": ["Classroom Management", "Lesson Planning", "Training Delivery", "E-Learning Platforms"],
}


def role_score(user_skills, role_skills):
    if not role_skills:
        return 0

    user = {s.lower() for s in user_skills}
    role = {s.lower() for s in role_skills}

    return round(len(user.intersection(role)) / len(role) * 100, 1)


def roadmap(missing):
    if not missing:
        return [
            "Week 1: Improve your GitHub README and add screenshots.",
            "Week 2: Record a short demo video of your project.",
            "Week 3: Practice explaining your dataset, EDA, and preprocessing decisions.",
            "Week 4: Apply to internships using this project as your main portfolio proof.",
        ]

    selected = missing[:4]

    while len(selected) < 4:
        selected.append("Project Documentation")

    return [
        f"Week 1: Learn and practice {selected[0]} with one small notebook task.",
        f"Week 2: Add {selected[1]} into a mini project or dashboard.",
        f"Week 3: Use {selected[2]} in your current portfolio project.",
        f"Week 4: Polish {selected[3]}, update GitHub, and prepare interview answers.",
    ]


def analyze_cv(path):
    text = extract_text(path)

    skills_table = skills_df()
    known_skills = skills_table["skill"].dropna().unique().tolist()

    user_skills = find_skills(text, known_skills)
    market_skills = skills_table.head(20)["skill"].tolist()
    missing = [skill for skill in market_skills if skill not in user_skills]

    scores = []
    for role, skills in ROLE_SKILLS.items():
        scores.append({
            "role": role,
            "score": role_score(user_skills, skills),
        })

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    best_role = scores[0]["role"] if scores else "Data / BI Analyst"

    if market_skills:
        match = round((len(set(user_skills).intersection(set(market_skills))) / len(set(market_skills))) * 100, 1)
    else:
        match = 0

    df = jobs_df()
    recommended_jobs = []

    if not df.empty and user_skills:
        mask = df["skills_text"].apply(lambda value: any(skill.lower() in str(value).lower() for skill in user_skills))
        recommended_jobs = df[mask][["title", "company", "city", "sector", "skills_text"]].head(6).to_dict("records")

    return {
        "filename": path.name,
        "match_score": match,
        "skills": user_skills,
        "missing": missing[:10],
        "role_scores": scores,
        "best_role": best_role,
        "roadmap": roadmap(missing),
        "recommended_jobs": recommended_jobs,
        "preview": text[:500],
    }
