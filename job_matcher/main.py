from datetime import date
from .cover_letter import generate_cover_letter

from .config import load_config
from .sheets_client import append_rows
from .resume_parser import load_resume_text
from .scorer import score_job_rule_based
from scrapers.example_scraper import get_example_jobs


def main():
    # 1) Load config + resume
    config = load_config()
    print("Config loaded.")
    candidate_name = "Yassin Marmoud"  # change if needed

    resume_path = config.resume["path"]
    resume_text = load_resume_text(resume_path)
    print("Resume loaded. Length:", len(resume_text))

    sheet_id = config.google_sheets["spreadsheet_id"]
    sheet_range = config.google_sheets["range"]  # e.g. "Sheet1!A2"

    # Rating threshold (1–10)
    min_rating = int(config.scoring.get("min_score_to_apply", 5))
    print("Minimum rating to keep a job:", min_rating)

    # 2) Get fake jobs
    jobs = get_example_jobs()
    print(f"Got {len(jobs)} jobs to score.")

    rows = []

    # known platforms mapping
    platforms = {
        "indeed.com": "Indeed",
        "linkedin.com": "LinkedIn",
        "ziprecruiter.com": "ZipRecruiter",
        "google.com": "Google",
        "upwork.com": "Upwork",
        "glassdoor.com": "Glassdoor",
        "monster.com": "Monster",
        "careerbuilder.com": "CareerBuilder",
        "simplyhired.com": "SimplyHired",
        "remoteok.com": "RemoteOK",
    }

    for job in jobs:
        job_title = job["title"]
        job_description = job["description"]
        link = job["link"]
        company_name = job["company_name"]
        company_desc = job["company_desc"]
        city = job["city"]
        apply_mode = job.get("apply_mode", "external")

        # --- detect platform from link ---
        platform = "Other"
        for key, name in platforms.items():
            if key in link:
                platform = name
                break

        # --- decide status from apply mode ---
        if apply_mode == "easy":
            status = "Applied"
        elif apply_mode == "external":
            status = "To-Do"
        else:
            status = "Rejected"

        # --- build data for scoring function ---
        scoring_job = {
            "title": job_title,
            "description": job_description,
            "city": city,
            "salary_text": job.get("salary_text", ""),
            "benefits_text": job.get("benefits_text", ""),
            # default to full-time if not specified
            "job_type": job.get("job_type", "Full-time"),
        }

        # --- score 0–10 with your rules ---
        rating = score_job_rule_based(resume_text, scoring_job)

        if rating == 0:
            print(f"SKIP (German or no match): {job_title}")
            continue

        if rating < min_rating:
            print(f"SKIP (rating {rating} < {min_rating}): {job_title}")
            continue

        print(f"KEEP: {job_title} | rating={rating} | status={status}")

        # --- remote detection (for checkbox) ---
        text_all = (job_title + " " + job_description + " " + city).lower()
        is_remote = "remote" in text_all

        # --- generate cover letter text ---
        cover_letter_text = generate_cover_letter(
            candidate_name=candidate_name,
            resume_text=resume_text,
            job_title=job_title,
            company_name=company_name,
            city=city,
            platform=platform,
        )

        # --- build row (14 columns) ---
        # Title, Job Description, Platform, Link, Date, Rating,
        # Company Name, Job Description.1, Cover Letter, Salary,
        # City, Expired, Remote, Status
        row = [
            job_title,
            job_description,
            platform,
            link,
            str(date.today()),
            rating,
            company_name,
            job_description,
            cover_letter_text,  # auto-generated cover letter
            "",
            city,
            False,
            is_remote,
            status,
        ]

        rows.append(row)

    # 3) Write all rows
    if rows:
        print(f"Sending {len(rows)} rows to Google Sheets...")
        append_rows(sheet_id, sheet_range, rows)
        print("Done. Check your sheet.")
    else:
        print("No jobs passed the rules (German or rating below minimum).")


if __name__ == "__main__":
    main()
