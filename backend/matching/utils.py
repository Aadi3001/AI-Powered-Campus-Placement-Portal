def calculate_skill_match(student_skill_names, job_required_skill_names):
    """
    Compares a student's skills against a job's required skills.
    Returns matched skills, missing skills, and a percentage score.
    """
    student_skills_set = set(s.lower() for s in student_skill_names)
    required_skills_set = set(s.lower() for s in job_required_skill_names)

    if not required_skills_set:
        # Job has no specific skill requirements — treat as a full match
        return {
            'matched_skills': [],
            'missing_skills': [],
            'skill_match_percentage': 100.0,
        }

    matched = student_skills_set & required_skills_set
    missing = required_skills_set - student_skills_set

    percentage = (len(matched) / len(required_skills_set)) * 100

    return {
        'matched_skills': sorted(matched),
        'missing_skills': sorted(missing),
        'skill_match_percentage': round(percentage, 2),
    }


def check_eligibility(student, job):
    """
    Checks whether a student meets a job's hard eligibility criteria:
    CGPA, branch, and graduation year range.
    Returns a dict of individual checks plus an overall eligible flag.
    """
    checks = {
        'cgpa_eligible': True,
        'branch_eligible': True,
        'graduation_year_eligible': True,
    }

    if job.min_cgpa is not None and student.cgpa is not None:
        checks['cgpa_eligible'] = student.cgpa >= job.min_cgpa

    if job.eligible_branches:
        eligible_branches_list = [
            b.strip().lower() for b in job.eligible_branches.split(',')
        ]
        checks['branch_eligible'] = student.branch.strip().lower() in eligible_branches_list

    if job.min_graduation_year is not None and student.graduation_year is not None:
        if student.graduation_year < job.min_graduation_year:
            checks['graduation_year_eligible'] = False

    if job.max_graduation_year is not None and student.graduation_year is not None:
        if student.graduation_year > job.max_graduation_year:
            checks['graduation_year_eligible'] = False

    checks['overall_eligible'] = all(checks.values())
    return checks