from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Problem, Category, Algorithm, Example
from django.core.files.uploadedfile import SimpleUploadedFile


class ProblemViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin = User.objects.create_superuser(username='admin', password='12345', email='admin@test.com')

        self.category = Category.objects.create(name='Test Category')
        self.algorithm = Algorithm.objects.create(name='Test Algorithm')
        self.example = Example.objects.create(
            input_data='Test Input',
            output_data='Test Output'
        )

        self.test_problem = Problem.objects.create(
            title='Test Problem',
            description='Test Description',
            theme=self.category,
            algorithm=self.algorithm,
            difficulty='easy',
            solution='Test Solution'
        )
        self.test_problem.examples.add(self.example)

    def test_problem_list_view(self):
        response = self.client.get(reverse('problems:problem_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_list.html')
        self.assertTrue('problems' in response.context)

    def test_problem_detail_view(self):
        response = self.client.get(
            reverse('problems:problem_detail', kwargs={'slug': self.test_problem.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_detail.html')

    def test_problem_create_view_as_admin(self):
        self.client.login(username='admin', password='12345')
        response = self.client.get(reverse('problems:problem_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_form.html')

    def test_problem_create_view_as_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('problems:problem_create'))
        self.assertEqual(response.status_code, 403)

    def test_problem_update_view_as_admin(self):
        self.client.login(username='admin', password='12345')
        response = self.client.get(
            reverse('problems:problem_update', kwargs={'slug': self.test_problem.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_form.html')

    def test_problem_delete_as_admin(self):
        self.client.login(username='admin', password='12345')
        response = self.client.post(
            reverse('problems:problem_delete', kwargs={'slug': self.test_problem.slug})
        )
        self.assertRedirects(response, reverse('problems:problem_list'))
        self.assertFalse(Problem.objects.filter(slug=self.test_problem.slug).exists())