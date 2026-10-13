from django.test import SimpleTestCase

from .utils import extract_skills_from_text

SKILLS = ['C++', 'Java', 'JavaScript', 'Python', 'C#', '.NET', 'Node.js']


class ExtractSkillsTests(SimpleTestCase):
    """SimpleTestCase: these tests need no database."""

    def check(self, text, expected):
        self.assertCountEqual(extract_skills_from_text(text, SKILLS), expected)

    def test_skills_ending_in_symbols(self):
        self.check("Skills: C++, Java and Python", ['C++', 'Java', 'Python'])

    def test_dotted_and_symbol_skills(self):
        self.check("Experience in C#/.NET development", ['C#', '.NET'])

    def test_java_is_not_javascript(self):
        self.check("Built apps with JavaScript and Node.js", ['JavaScript', 'Node.js'])

    def test_no_partial_word_matches(self):
        self.check("I know Javascripting and Pythonic style", [])