from pathlib import Path

import pandas as pd
from flask import current_app


def jobs_df():
    path = Path(current_app.config["DATA_PATH"])

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path).fillna("")


def skills_df():
    path = Path(current_app.config["SKILL_PATH"])

    if not path.exists():
        return pd.DataFrame(columns=["skill", "job_count"])

    return pd.read_csv(path).fillna("")
