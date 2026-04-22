def extract_skills(text):
    skills_list = [
        "Python", "Pandas", "NumPy", "TF-IDF", "Text Classification",
        "K-Means Clustering", "SQL", "CTEs", "Window Functions",
        "MySQL", "Data Cleaning", "ETL", "Power BI", "DAX",
        "Power Query", "Dashboard Design", "KPI",
        "Generative AI", "PyTorch", "Transformers"
    ]

    found_skills = []

    text_lower = text.lower()

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))