from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "clean_jobs.csv"
FIG_DIR = ROOT / "outputs" / "figures"


def save_bar(series, title, xlabel, ylabel, filename):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def main():
    df = pd.read_csv(DATA_PATH)

    skills = df["skills_text"].str.split(", ").explode().dropna()
    skills = skills[skills.astype(str).str.strip() != ""].value_counts()

    save_bar(df["city"].value_counts().head(10), "Top 10 Cities by Jobs", "City", "Jobs", "top_cities.png")
    save_bar(df["sector"].value_counts().head(10), "Top 10 Sectors by Jobs", "Sector", "Jobs", "top_sectors.png")
    save_bar(df["role_category"].value_counts().head(8), "Role Category Distribution", "Role", "Jobs", "role_categories.png")
    save_bar(skills.head(15), "Top 15 Required Skills", "Skill", "Jobs", "top_skills.png")
    save_bar(df["experience_required"].value_counts().head(8), "Experience Requirement Distribution", "Experience", "Jobs", "experience_distribution.png")

    print("EDA charts generated.")


if __name__ == "__main__":
    main()
