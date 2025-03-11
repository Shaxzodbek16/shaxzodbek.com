from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from datetime import datetime
from .models import (
    Article,
    ProgrammingLanguage,
    Education,
    Certification,
    Type,
    Project,
)


class TestBlogModels(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content1="Content 1",
            content2="Content 2",
            visible=True,
        )
        self.pl = ProgrammingLanguage.objects.create(
            name="Python", knowing_percentage=85.5
        )
        self.education = Education.objects.create(
            name="Test University",
            description="Test Description",
            field="Computer Science",
        )
        self.cert = Certification.objects.create(name="Test Cert", description="Desc")
        self.type_obj = Type.objects.create(name="Web Development")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Desc",
            started_from=datetime.now(),
            ended_at=datetime.now(),
        )

    def test_article_model(self):
        self.assertEqual(str(self.article), "Test Article")
        self.assertEqual(self.article.slug, slugify("Test Article"))
        self.assertTrue(self.article.visible)
        self.assertIsInstance(self.article.created, datetime)

    def test_programming_language_model(self):
        self.assertEqual(str(self.pl), "Python")
        self.assertEqual(self.pl.slug, slugify("Python"))
        self.assertEqual(self.pl.knowing_percentage, 85.5)
        self.assertIsInstance(self.pl.started_from, datetime)

    def test_education_model(self):
        self.assertEqual(str(self.education), "Test University")
        self.assertEqual(self.education.slug, slugify("Test University"))
        self.assertEqual(self.education.field, "Computer Science")

    def test_certification_model(self):
        cert2 = Certification.objects.create(name="Cert 2", description="Desc 2")
        self.assertEqual(str(self.cert), "Test Cert")
        self.assertEqual(self.cert.slug, slugify("Test Cert"))
        self.assertEqual(self.cert.next, cert2)
        self.assertEqual(cert2.previous, self.cert)

    def test_type_model(self):
        self.assertEqual(str(self.type_obj), "Web Development")
        self.assertEqual(self.type_obj.slug, slugify("Web Development"))

    def test_project_model(self):
        self.project.programming_languages.add(self.pl)
        self.project.type.add(self.type_obj)
        self.assertEqual(str(self.project), "Test Project")
        self.assertEqual(self.project.slug, slugify("Test Project"))
        self.assertIn(self.pl, self.project.programming_languages.all())
        self.assertIn(self.type_obj, self.project.type.all())


class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.article = Article.objects.create(
            title="Test Article",
            content1="Content 1",
            content2="Content 2",
            visible=True,
        )
        self.pl = ProgrammingLanguage.objects.create(name="Python")
        self.education = Education.objects.create(name="Test Uni", description="Desc")
        self.cert = Certification.objects.create(name="Test Cert", description="Desc")
        self.project = Project.objects.create(
            name="Test Project",
            description="Desc",
            started_from=datetime.now(),
            ended_at=datetime.now(),
        )

    def test_home_view(self):
        url = reverse("blog:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("programming_languages", response.context)
        self.assertIn("educations", response.context)
        self.assertIn("articles", response.context)
        self.assertIn("projects", response.context)
        self.assertTemplateUsed(response, "home.html")

    def test_aboutme_view(self):
        url = reverse("blog:aboutme")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aboutme.html")

    def test_articles_view(self):
        url = reverse("blog:articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)
        self.assertIn(self.article, response.context["page_obj"])
        self.assertTemplateUsed(response, "blog/articles.html")

    def test_article_detail_view(self):
        url = reverse("blog:article_detail", kwargs={"slug": self.article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["article"], self.article)
        self.assertTemplateUsed(response, "blog/article_detail.html")

    def test_certifications_view(self):
        url = reverse("blog:certifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)
        self.assertIn(self.cert, response.context["page_obj"])
        self.assertTemplateUsed(response, "blog/certifications.html")

    def test_certification_detail_view(self):
        url = reverse("blog:certification_detail", kwargs={"slug": self.cert.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["certification"], self.cert)
        self.assertTemplateUsed(response, "blog/certification_detail.html")

    def test_projects_view(self):
        url = reverse("blog:projects")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)
        self.assertIn(self.project, response.context["page_obj"])
        self.assertTemplateUsed(response, "blog/projects.html")

    def test_project_detail_view(self):
        url = reverse("blog:project_detail", kwargs={"slug": self.project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["project"], self.project)
        self.assertTemplateUsed(response, "blog/project_detail.html")

    def test_404_on_invalid_slug(self):
        url = reverse("blog:article_detail", kwargs={"slug": "non-existent"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
