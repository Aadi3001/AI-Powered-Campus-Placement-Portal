import random
from decimal import Decimal
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import StudentProfile, BRANCH_CHOICES
from students.models import Skill
from recruiters.models import SkillTag, Company, RecruiterProfile, Job
from applications.models import Application
from matching.utils import generate_match_report

fake = Faker()
User = get_user_model()

SKILL_POOL = [
    "Python", "Java", "Django", "React", "C++", "JavaScript", "SQL",
    "PostgreSQL", "HTML", "CSS", "Node.js", "Machine Learning", "Git",
    "Docker", "AWS", "Data Analysis", "Flask", "TensorFlow", "Spring Boot",
]

COMPANY_POOL = [
    ("Nimbus Systems", "Cloud Services"),
    ("Brightwave Technologies", "Software Products"),
    ("Orbit Analytics", "Data Analytics"),
    ("Cedar Labs", "AI Research"),
    ("Pinecrest Digital", "IT Consulting"),
]

JOB_TITLES = [
    "Software Developer Intern", "Backend Developer", "Data Analyst",
    "Full Stack Developer", "Machine Learning Engineer",
]


class Command(BaseCommand):
    help = "Seeds the database with realistic fake students, jobs, and applications."

    def handle(self, *args, **options):
        self.stdout.write("Seeding skill tags...")
        self.seed_skill_tags()
        self.stdout.write("Seeding students...")
        self.seed_students(count=300)
        self.stdout.write("Seeding student skills...")
        self.seed_student_skills()
        self.stdout.write("Seeding companies and recruiters...")
        self.seed_companies_and_recruiters()
        self.stdout.write("Seeding jobs...")
        self.seed_jobs()
        self.stdout.write("Seeding applications...")
        self.seed_applications()
        self.stdout.write(self.style.SUCCESS("Done seeding."))

    def seed_students(self, count):
        branch_codes = [code for code, _ in BRANCH_CHOICES]

        for i in range(count):
            username = f"seed_student_{i+1}"

            if User.objects.filter(username=username).exists():
                continue  # skip if already seeded, so re-running is safe

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="SeedPass123",
                role='STUDENT',
            )
            # signal already auto-created an empty StudentProfile; fetch and fill it
            profile = user.student_profile
            profile.full_name = fake.name()
            profile.branch = random.choice(branch_codes)
            profile.graduation_year = random.choice([2026, 2027, 2028])
            profile.cgpa = Decimal(str(round(random.uniform(5.5, 9.8), 2)))
            profile.save()

    def seed_skill_tags(self):
        for name in SKILL_POOL:
            SkillTag.objects.get_or_create(name=name)

    def seed_student_skills(self):
        proficiencies = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']
        seed_students = StudentProfile.objects.filter(
            user__username__startswith='seed_student'
        )

        for student in seed_students:
            if student.skills.exists():
                continue  # already has skills, so re-running stays safe

            chosen = random.sample(SKILL_POOL, k=random.randint(2, 6))
            for skill_name in chosen:
                Skill.objects.create(
                    student=student,
                    name=skill_name,
                    proficiency=random.choice(proficiencies),
                )

    def seed_companies_and_recruiters(self):
        for i, (company_name, industry) in enumerate(COMPANY_POOL, start=1):
            company, _ = Company.objects.get_or_create(
                name=company_name,
                defaults={
                    'industry': industry,
                    'description': f"{company_name} is a {industry.lower()} company.",
                },
            )

            username = f"seed_recruiter_{i}"
            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="SeedPass123",
                role='RECRUITER',
            )
            # the signal already created an empty RecruiterProfile; fill it in
            profile = user.recruiter_profile
            profile.company = company
            profile.full_name = fake.name()
            profile.designation = "HR Manager"
            profile.save()

    def seed_jobs(self):
        branch_codes = [code for code, _ in BRANCH_CHOICES]
        recruiters = RecruiterProfile.objects.filter(
            user__username__startswith='seed_recruiter'
        )

        for recruiter in recruiters:
            if recruiter.jobs.exists():
                continue  # already seeded, so re-running stays safe

            for title in random.sample(JOB_TITLES, k=2):
                skills = random.sample(SKILL_POOL, k=random.randint(2, 4))
                job = Job.objects.create(
                    recruiter=recruiter,
                    title=title,
                    description=(
                        f"{recruiter.company.name} is hiring a {title}. "
                        f"Experience with {', '.join(skills)} is expected."
                    ),
                    min_cgpa=Decimal(str(round(random.uniform(6.0, 8.0), 2))),
                    eligible_branches=", ".join(
                        random.sample(branch_codes, k=random.randint(2, 4))
                    ),
                    min_graduation_year=2026,
                    max_graduation_year=random.choice([2027, 2028]),
                    location=random.choice(["Mumbai", "Pune", "Bengaluru", "Hyderabad"]),
                )
                job.required_skills.set(SkillTag.objects.filter(name__in=skills))

    def seed_applications(self):
        seed_students = StudentProfile.objects.filter(
            user__username__startswith='seed_student'
        )
        all_jobs = list(Job.objects.all())

        for student in seed_students:
            if student.applications.exists():
                continue  # already has applications, so re-running stays safe

            for job in random.sample(all_jobs, k=random.randint(3, 6)):
                report = generate_match_report(student, job)
                Application.objects.create(
                    student=student,
                    job=job,
                    status=self.decide_outcome(student, report),
                )

    def decide_outcome(self, student, report):
        """
        SYNTHETIC outcome rule, NOT real hiring data.
        Any model trained on these outcomes learns this rule, so its accuracy
        must be reported as a pipeline demo on synthetic data.
        """
        roll = random.random()
        if roll < 0.10:
            return 'APPLIED'       # still unresolved
        if roll < 0.20:
            return 'SHORTLISTED'   # still unresolved

        if not report['overall_eligible']:
            return 'REJECTED'

        cgpa_part = (float(student.cgpa) - 5.5) / (9.8 - 5.5)   # roughly 0 to 1
        skill_part = report['skill_match_percentage'] / 100
        score = 0.5 * skill_part + 0.5 * cgpa_part

        probability = 0.15 + 0.6 * score
        return 'SELECTED' if random.random() < probability else 'REJECTED'