from django.test import TestCase
from django.utils import timezone
from .models import (
    Post,
    ProgrammingLanguage,
    Education,
    Certification,
    Project,
    Type,
    CV,
    AboutMe,
)
from django.urls import reverse


class PostModelTest(TestCase):
    def setUp(self):
        # Create test posts
        self.post1 = Post.objects.create(
            title="Test Post 1",
            content1="Test content 1",
            content2="Test content 2",
            created=timezone.now(),
            visible=True,
        )

        self.post2 = Post.objects.create(
            title="Test Post 2",
            content1="Test content 1",
            content2="Test content 2",
            created=timezone.now() - timezone.timedelta(days=1),
            visible=True,
        )

        self.post3 = Post.objects.create(
            title="Test Post 3",
            content1="Test content 1",
            content2="Test content 2",
            created=timezone.now() + timezone.timedelta(days=1),
            visible=True,
        )

        self.hidden_post = Post.objects.create(
            title="Hidden Post",
            content1="Hidden content 1",
            content2="Hidden content 2",
            created=timezone.now(),
            visible=False,
        )

    def test_post_creation(self):
        """Test that a post can be created with the correct attributes"""
        self.assertEqual(self.post1.title, "Test Post 1")
        self.assertEqual(self.post1.content1, "Test content 1")
        self.assertEqual(self.post1.content2, "Test content 2")
        self.assertTrue(self.post1.visible)
        self.assertEqual(self.post1.slug, "test-post-1")

    def test_post_str_representation(self):
        """Test the string representation of a post"""
        self.assertEqual(str(self.post1), "Test Post 1")

    def test_slug_generation(self):
        """Test that slugs are generated correctly"""
        post = Post.objects.create(
            title="This is a Test Post!",
            content1="Test content",
            content2="More test content",
            created=timezone.now(),
        )
        self.assertEqual(post.slug, "this-is-a-test-post")

    def test_next_previous_properties(self):
        """Test the next and previous properties"""
        # post2 is older than post1, so post2 should be the next post for post1
        self.assertEqual(self.post1.next, self.post2)

        # post3 is newer than post1, so post3 should be the previous post for post1
        self.assertEqual(self.post1.previous, self.post3)

        # post3 is the newest, so it should have no previous post
        self.assertIsNone(self.post3.previous)

        # post2 is the oldest, so it should have no next post
        self.assertIsNone(self.post2.next)

    def test_visibility_filter(self):
        """Test that hidden posts are not included in next/previous calculations"""
        # Hidden posts should not be considered for next/previous
        visible_posts = Post.objects.filter(visible=True)
        self.assertEqual(visible_posts.count(), 3)
        self.assertNotIn(self.hidden_post, visible_posts)


class ProgrammingLanguageModelTest(TestCase):
    def setUp(self):
        self.language = ProgrammingLanguage.objects.create(
            name="Python",
            knowing_percentage=90.0,
            started_from=timezone.now() - timezone.timedelta(days=365),
        )

    def test_language_creation(self):
        """Test that a programming language can be created with the correct attributes"""
        self.assertEqual(self.language.name, "Python")
        self.assertEqual(self.language.knowing_percentage, 90.0)
        self.assertEqual(self.language.slug, "python")

    def test_language_str_representation(self):
        """Test the string representation of a programming language"""
        self.assertEqual(str(self.language), "Python")


class ViewsTest(TestCase):
    def setUp(self):
        # Create test data
        self.post = Post.objects.create(
            title="Test Post",
            content1="Test content 1",
            content2="Test content 2",
            created=timezone.now(),
            visible=True,
        )

        self.language = ProgrammingLanguage.objects.create(
            name="Python",
            knowing_percentage=90.0,
            started_from=timezone.now() - timezone.timedelta(days=365),
        )

        self.education = Education.objects.create(
            name="Test University",
            description="Test description",
            started_from=timezone.now() - timezone.timedelta(days=1000),
            ended_at=timezone.now() - timezone.timedelta(days=500),
            field="Computer Science",
        )

        self.certification = Certification.objects.create(
            name="Test Certification",
            description="Test certification description",
            took_at=timezone.now() - timezone.timedelta(days=100),
        )

        self.project_type = Type.objects.create(name="Web Development")

        self.project = Project.objects.create(
            name="Test Project",
            description="Test project description",
            started_from=timezone.now() - timezone.timedelta(days=200),
            ended_at=timezone.now() - timezone.timedelta(days=100),
        )
        self.project.programming_languages.add(self.language)
        self.project.type.add(self.project_type)

        self.about_me = AboutMe.objects.create(
            content="Test about me content", image_description="Test image description"
        )

    def test_home_view(self):
        """Test the home view"""
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIn("programming_languages", response.context)
        self.assertIn("educations", response.context)
        self.assertIn("posts", response.context)
        self.assertIn("projects", response.context)

    def test_aboutme_view(self):
        """Test the about me view"""
        response = self.client.get(reverse("blog:aboutme"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aboutme.html")
        self.assertIn("items", response.context)
        self.assertEqual(list(response.context["items"]), [self.about_me])

    def test_post_list_view(self):
        """Test the post list view"""
        response = self.client.get(reverse("blog:post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post.html")
        self.assertIn("page_obj", response.context)
        self.assertEqual(list(response.context["page_obj"]), [self.post])

    def test_post_detail_view(self):
        """Test the post detail view"""
        response = self.client.get(reverse("blog:post_detail", args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertEqual(response.context["post"], self.post)

    def test_certifications_view(self):
        """Test the certifications view"""
        response = self.client.get(reverse("blog:certifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/certifications.html")
        self.assertIn("page_obj", response.context)
        self.assertEqual(list(response.context["page_obj"]), [self.certification])

    def test_certification_detail_view(self):
        """Test the certification detail view"""
        response = self.client.get(
            reverse("blog:certification_detail", args=[self.certification.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/certification_detail.html")
        self.assertEqual(response.context["certification"], self.certification)

    def test_projects_view(self):
        """Test the projects view"""
        response = self.client.get(reverse("blog:projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/projects.html")
        self.assertIn("page_obj", response.context)
        self.assertEqual(list(response.context["page_obj"]), [self.project])

    def test_project_detail_view(self):
        """Test the project detail view"""
        response = self.client.get(
            reverse("blog:project_detail", args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/project_detail.html")
        self.assertEqual(response.context["project"], self.project)
