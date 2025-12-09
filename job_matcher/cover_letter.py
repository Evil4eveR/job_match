from textwrap import shorten


def generate_cover_letter(
    candidate_name: str,
    resume_text: str,
    job_title: str,
    company_name: str,
    city: str,
    platform: str,
) -> str:
    """
    Very simple template-based cover letter.
    You can improve the text later as you like.
    """

    # Take a small snippet from resume to mention skills
    snippet = shorten(resume_text.replace("\n", " "), width=200, placeholder="...")

    greeting_name = company_name if company_name else "Hiring Team"
    location_part = f" in {city}" if city else ""
    platform_part = f" on {platform}" if platform != "Other" else ""

    letter = f"""Dear {greeting_name},

I am writing to express my interest in the {job_title} position{location_part} that I found{platform_part}.
Based on the requirements, I believe my background and skills are a strong match.

In my experience I have worked with technologies and responsibilities such as: {snippet}
I am particularly interested in this role at {company_name} because it aligns with my goals to grow as a {job_title}
and contribute to a team that values quality, collaboration and continuous improvement.

I would welcome the opportunity to discuss how my experience and skills can contribute to your company.
Thank you for considering my application.

Best regards,
{candidate_name}
"""
    return letter
