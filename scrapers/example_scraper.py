from typing import List, Dict


def get_example_jobs() -> List[Dict]:
    """
    Fake jobs for testing. Each job includes:
      - title, description, link, company_name, company_desc, city
      - apply_mode: "easy", "external", or "refuse"
    """
    return [
        {
            "title": "Junior Python Developer",
            "description": (
                "We are looking for an entry-level software engineer with "
                "Python, SQL, Linux and web APIs experience."
            ),
            "link": "https://www.indeed.com/viewjob?jk=123",
            "company_name": "Example Tech",
            "company_desc": "A fake tech company used for testing.",
            "city": "Remote",
            "apply_mode": "easy",      # easy apply -> Applied
        },
        {
            "title": "Entry Level Data Analyst",
            "description": (
                "Analyse datasets, write SQL queries, build dashboards and "
                "support the data team."
            ),
            "link": "https://www.linkedin.com/jobs/view/456",
            "company_name": "Data Corp",
            "company_desc": "Data-focused company for test purposes.",
            "city": "Toronto",
            "apply_mode": "external",  # needs external site -> To-Do
        },
        {
            "title": "Junior Software Engineer",
            "description": (
                "Work with Python and Linux to maintain backend services "
                "and help develop new features."
            ),
            "link": "https://www.ziprecruiter.com/jobs/789",
            "company_name": "DevStudio",
            "company_desc": "Another fake company for testing.",
            "city": "Berlin",
            "apply_mode": "refuse",    # not suitable -> Refused
        },
    ]
