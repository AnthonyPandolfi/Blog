import json
import argparse
import sys
import os

def load_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_resume_txt(profile):
    lines = []

    # Personal Info
    pi = profile.get('personal_info', {})
    lines.append(pi.get('name', 'Name').upper())
    lines.append(f"Email: {pi.get('email', '')} | Phone: {pi.get('phone', '')}")
    lines.append(f"Location: {pi.get('address', '')}")
    links = []
    if pi.get('linkedin'): links.append(f"LinkedIn: {pi.get('linkedin')}")
    if pi.get('github'): links.append(f"GitHub: {pi.get('github')}")
    if links:
        lines.append(" | ".join(links))
    lines.append("")

    # Summary
    if 'summary' in profile:
        lines.append("SUMMARY")
        lines.append("-" * 20)
        lines.append(profile['summary'])
        lines.append("")

    # Skills
    if 'skills' in profile:
        lines.append("SKILLS")
        lines.append("-" * 20)
        lines.append(", ".join(profile['skills']))
        lines.append("")

    # Experience
    if 'experience' in profile:
        lines.append("EXPERIENCE")
        lines.append("-" * 20)
        for exp in profile['experience']:
            lines.append(f"{exp.get('role', '')} at {exp.get('company', '')}")
            lines.append(f"{exp.get('start_date', '')} to {exp.get('end_date', '')}")
            for resp in exp.get('responsibilities', []):
                lines.append(f"- {resp}")
            lines.append("")

    # Education
    if 'education' in profile:
        lines.append("EDUCATION")
        lines.append("-" * 20)
        for edu in profile['education']:
            lines.append(f"{edu.get('degree', '')}")
            lines.append(f"{edu.get('institution', '')}")
            lines.append(f"{edu.get('start_date', '')} to {edu.get('end_date', '')}")
            lines.append("")

    return "\n".join(lines)

def generate_resume_html(profile):
    # build semantic html
    html = ["<!DOCTYPE html>", "<html lang=\"en\">", "<head>", "<meta charset=\"UTF-8\">", "<title>Resume</title>", "</head>", "<body>"]

    pi = profile.get('personal_info', {})
    html.append(f"<h1>{pi.get('name', '')}</h1>")
    html.append(f"<p>Email: {pi.get('email', '')} | Phone: {pi.get('phone', '')}<br>")
    html.append(f"Location: {pi.get('address', '')}<br>")

    links = []
    if pi.get('linkedin'): links.append(f"<a href=\"https://{pi.get('linkedin')}\">LinkedIn</a>")
    if pi.get('github'): links.append(f"<a href=\"https://{pi.get('github')}\">GitHub</a>")
    if links:
        html.append(" | ".join(links))
    html.append("</p>")

    if 'summary' in profile:
        html.append("<h2>Summary</h2>")
        html.append(f"<p>{profile['summary']}</p>")

    if 'skills' in profile:
        html.append("<h2>Skills</h2>")
        html.append(f"<p>{', '.join(profile['skills'])}</p>")

    if 'experience' in profile:
        html.append("<h2>Experience</h2>")
        for exp in profile['experience']:
            html.append(f"<h3>{exp.get('role', '')} - {exp.get('company', '')}</h3>")
            html.append(f"<p><em>{exp.get('start_date', '')} to {exp.get('end_date', '')}</em></p>")
            html.append("<ul>")
            for resp in exp.get('responsibilities', []):
                html.append(f"<li>{resp}</li>")
            html.append("</ul>")

    if 'education' in profile:
        html.append("<h2>Education</h2>")
        for edu in profile['education']:
            html.append(f"<h3>{edu.get('degree', '')}</h3>")
            html.append(f"<p>{edu.get('institution', '')}<br>")
            html.append(f"<em>{edu.get('start_date', '')} to {edu.get('end_date', '')}</em></p>")

    html.append("</body>")
    html.append("</html>")
    return "\n".join(html)

def generate_cover_letter(profile, job_title, company_name):
    pi = profile.get('personal_info', {})
    name = pi.get('name', 'Applicant')

    text = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position at {company_name}.

With my background in software engineering and my commitment to building high-quality, accessible products, I am confident in my ability to make an immediate impact on your team.

Please find my resume attached for your review. I would welcome the opportunity to discuss how my skills and experiences align with the needs of {company_name}.

Thank you for your time and consideration.

Sincerely,

{name}
{pi.get('email', '')}
{pi.get('phone', '')}
"""
    return text

def main():
    parser = argparse.ArgumentParser(description="Generate ATS-friendly resume and cover letter.")
    parser.add_argument('--profile', type=str, default='profile.json', help='Path to profile JSON file')
    parser.add_argument('--job-title', type=str, help='Target Job Title for cover letter')
    parser.add_argument('--company', type=str, help='Target Company Name for cover letter')

    args = parser.parse_args()

    if not os.path.exists(args.profile):
        print(f"Error: {args.profile} not found.")
        sys.exit(1)

    profile = load_profile(args.profile)

    # Generate Resume
    txt_resume = generate_resume_txt(profile)
    html_resume = generate_resume_html(profile)

    with open('resume.txt', 'w', encoding='utf-8') as f:
        f.write(txt_resume)
    with open('resume.html', 'w', encoding='utf-8') as f:
        f.write(html_resume)

    print("Generated resume.txt and resume.html")

    # Generate Cover Letter if args provided
    if args.job_title and args.company:
        cl_text = generate_cover_letter(profile, args.job_title, args.company)
        with open('cover_letter.txt', 'w', encoding='utf-8') as f:
            f.write(cl_text)
        print(f"Generated cover_letter.txt for {args.job_title} at {args.company}")

if __name__ == "__main__":
    main()
