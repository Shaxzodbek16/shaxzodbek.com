from django.test import TestCase
from .models import Questions

class QuestionsModelTest(TestCase):
    def setUp(self):
        self.question = Questions.objects.create(
            question="What is 2+2?",
            answer="4",
            option1="3",
            option2="4", 
            option3="5",
            taken_book="Math Book",
            theme="Addition",
            subject="Math"
        )

    def test_question_creation(self):
        self.assertEqual(self.question.question, "What is 2+2?")
        self.assertEqual(self.question.answer, "4")
        self.assertEqual(self.question.option1, "3")
        self.assertEqual(self.question.option2, "4")
        self.assertEqual(self.question.option3, "5")
        self.assertEqual(self.question.taken_book, "Math Book")
        self.assertEqual(self.question.theme, "Addition")
        self.assertEqual(self.question.subject, "Math")

    def test_question_str(self):
        expected = "What is 2+ --- answer is 4"
        self.assertEqual(str(self.question), expected)

    def test_question_repr(self):
        expected = "Questions What is 2+ --- answer is 4"
        self.assertEqual(repr(self.question), expected)

    def test_question_equality(self):
        question2 = Questions.objects.create(
            question="What is 2+2?",
            answer="4",
            option1="3",
            option2="4",
            option3="5"
        )
        self.assertEqual(self.question, question2)

    def test_slug_generation(self):
        self.assertEqual(self.question.slug, "what-is-22")

    def test_unique_slug_generation(self):
        question2 = Questions.objects.create(
            question="What is 2+2?",
            answer="4",
            option1="6",
            option2="7",
            option3="8"
        )
        self.assertEqual(question2.slug, "what-is-22-1")

    def test_meta_options(self):
        self.assertEqual(Questions._meta.db_table, "Math")
        self.assertEqual(Questions._meta.verbose_name, "Math")
        self.assertEqual(Questions._meta.verbose_name_plural, "Maths")

