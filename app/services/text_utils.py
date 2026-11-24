import re


def normalize(value):
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9+#.\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def find_skills(text, known_skills):
    text = normalize(text)
    matched = []

    for skill in known_skills:
        cleaned = normalize(skill)
        if cleaned and cleaned in text:
            matched.append(skill)

    return sorted(set(matched))
