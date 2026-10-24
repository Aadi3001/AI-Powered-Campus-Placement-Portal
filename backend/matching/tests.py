from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from .utils import calculate_skill_match, check_eligibility


def make_job(**overrides):
    """A stand-in with only the attributes check_eligibility reads."""
    fields = {
        'min_cgpa': Decimal('7.0'),
        'eligible_branches': 'CSE, IT',
        'min_graduation_year': 2026,
        'max_graduation_year': 2027,
    }
    fields.update(overrides)
    return SimpleNamespace(**fields)


def make_student(**overrides):
    fields = {'cgpa': Decimal('8.0'), 'branch': 'IT', 'graduation_year': 2027}
    fields.update(overrides)
    return SimpleNamespace(**fields)


class SkillMatchTests(SimpleTestCase):
    def test_full_match(self):
        result = calculate_skill_match(['Python', 'Django'], ['python'])
        self.assertEqual(result['matched_skills'], ['python'])
        self.assertEqual(result['missing_skills'], [])
        self.assertEqual(result['skill_match_percentage'], 100.0)

    def test_partial_match(self):
        result = calculate_skill_match(['Python'], ['Python', 'Django', 'React'])
        self.assertEqual(result['matched_skills'], ['python'])
        self.assertEqual(result['missing_skills'], ['django', 'react'])
        self.assertEqual(result['skill_match_percentage'], 33.33)

    def test_no_match(self):
        result = calculate_skill_match([], ['Python'])
        self.assertEqual(result['skill_match_percentage'], 0.0)
        self.assertEqual(result['missing_skills'], ['python'])

    def test_job_without_requirements_counts_as_full_match(self):
        result = calculate_skill_match(['Python'], [])
        self.assertEqual(result['skill_match_percentage'], 100.0)

    def test_matching_ignores_case(self):
        result = calculate_skill_match(['PYTHON'], ['python'])
        self.assertEqual(result['matched_skills'], ['python'])


class EligibilityTests(SimpleTestCase):
    def test_fully_eligible(self):
        result = check_eligibility(make_student(), make_job())
        self.assertTrue(result['overall_eligible'])

    def test_cgpa_below_minimum(self):
        result = check_eligibility(make_student(cgpa=Decimal('6.5')), make_job())
        self.assertFalse(result['cgpa_eligible'])
        self.assertTrue(result['branch_eligible'])
        self.assertFalse(result['overall_eligible'])

    def test_cgpa_exactly_at_minimum(self):
        result = check_eligibility(make_student(cgpa=Decimal('7.0')), make_job())
        self.assertTrue(result['cgpa_eligible'])

    def test_branch_not_listed(self):
        result = check_eligibility(make_student(branch='MECH'), make_job())
        self.assertFalse(result['branch_eligible'])
        self.assertFalse(result['overall_eligible'])

    def test_graduation_year_too_late(self):
        result = check_eligibility(make_student(graduation_year=2028), make_job())
        self.assertFalse(result['graduation_year_eligible'])

    def test_graduation_year_too_early(self):
        result = check_eligibility(make_student(graduation_year=2025), make_job())
        self.assertFalse(result['graduation_year_eligible'])

    def test_no_constraints_means_eligible(self):
        job = make_job(
            min_cgpa=None, eligible_branches='',
            min_graduation_year=None, max_graduation_year=None,
        )
        result = check_eligibility(make_student(branch='MECH', graduation_year=2030), job)
        self.assertTrue(result['overall_eligible'])

    def test_missing_student_cgpa_skips_the_check(self):
        # Intentional: the CGPA rule is skipped when the student has no CGPA.
        # The prediction code handles that case separately.
        result = check_eligibility(make_student(cgpa=None), make_job())
        self.assertTrue(result['cgpa_eligible'])