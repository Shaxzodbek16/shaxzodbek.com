from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from .models import (
    Match,
    Connection,
    Author,
    Category,
    ProgrammingLanguage,
    Video,
)
from datetime import date, timedelta


class MatchModelTest(TestCase):
    def setUp(self):
        self.match = Match.objects.create(who_is_it="Test Match")

    def test_match_creation(self):
        self.assertTrue(isinstance(self.match, Match))
        self.assertEqual(self.match.__str__(), "Test Match")

    def test_auto_now_add(self):
        self.assertIsNotNone(self.match.created)

    def test_auto_now(self):
        old_updated = self.match.updated
        self.match.who_is_it = "Updated Match"
        self.match.save()
        self.assertGreater(self.match.updated, old_updated)

    def test_ordering(self):
        Match.objects.create(who_is_it="New Match")
        matches = Match.objects.all()
        self.assertEqual(matches[0].who_is_it, "New Match")
        self.assertEqual(matches[1].who_is_it, "Test Match")


class ConnectionModelTest(TestCase):
    def setUp(self):
        self.match = Match.objects.create(who_is_it="Test Match")
        self.connection = Connection.objects.create(
            first_name="John",
            last_name="Doe",
            picture=SimpleUploadedFile(
                "test_image.jpg", b"file_content", content_type="image/jpeg"
            ),
            birth_date=date(1990, 1, 1),
            job_title="Developer",
            met_address="123 Test St",
            met_at=timezone.now(),
        )
        self.connection.who_for_me.add(self.match)

    def test_connection_creation(self):
        self.assertTrue(isinstance(self.connection, Connection))
        self.assertIn("John Doe Developer 1990-01-01", self.connection.__str__())

    def test_many_to_many_relationship(self):
        self.assertEqual(self.connection.who_for_me.count(), 1)
        self.assertEqual(self.connection.who_for_me.first(), self.match)

    def test_optional_fields(self):
        connection = Connection.objects.create(
            first_name="Jane",
            last_name="Doe",
            picture=SimpleUploadedFile(
                "test_image.jpg", b"file_content", content_type="image/jpeg"
            ),
            birth_date=date(1995, 1, 1),
            met_address="456 Test Ave",
            met_at=timezone.now(),
        )
        self.assertIsNone(connection.job_title)
        self.assertIsNone(connection.home_address)

    def test_ordering(self):
        Connection.objects.create(
            first_name="Younger",
            last_name="Person",
            picture=SimpleUploadedFile(
                "test_image.jpg", b"file_content", content_type="image/jpeg"
            ),
            birth_date=date(2000, 1, 1),
            met_address="789 Test Blvd",
            met_at=timezone.now(),
        )
        connections = Connection.objects.all()
        self.assertEqual(connections[0].first_name, "Younger")
        self.assertEqual(connections[0].last_name, "Person")


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Jane", last_name="Austen")

    def test_author_creation(self):
        self.assertTrue(isinstance(self.author, Author))
        self.assertEqual(self.author.__str__(), "Jane Austen")

    def test_ordering(self):
        Author.objects.create(first_name="William", last_name="Shakespeare")
        authors = Author.objects.all()
        self.assertEqual(authors[0].first_name, "William")
        self.assertEqual(authors[1].first_name, "Jane")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction")

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), "Fiction")

    def test_ordering(self):
        Category.objects.create(name="Non-fiction")
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "Non-fiction")
        self.assertEqual(categories[1].name, "Fiction")


class ProgrammingLanguageModelTest(TestCase):
    def setUp(self):
        self.language = ProgrammingLanguage.objects.create(name="Python")

    def test_programming_language_creation(self):
        self.assertTrue(isinstance(self.language, ProgrammingLanguage))
        self.assertEqual(self.language.__str__(), "Python")

    def test_ordering(self):
        ProgrammingLanguage.objects.create(name="JavaScript")
        languages = ProgrammingLanguage.objects.all()
        self.assertEqual(languages[0].name, "Python")
        self.assertEqual(languages[1].name, "JavaScript")


class VideoModelTest(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            url="https://example.com/video",
            created_at=timezone.now(),
            thumbnail=SimpleUploadedFile(
                "thumbnail.jpg", b"file_content", content_type="image/jpeg"
            ),
        )

    def test_video_creation(self):
        self.assertTrue(isinstance(self.video, Video))
        self.assertIn("Test Video at", self.video.__str__())

    def test_ordering(self):
        Video.objects.create(
            title="New Video",
            url="https://example.com/new-video",
            created_at=timezone.now() + timedelta(hours=1),
            thumbnail=SimpleUploadedFile(
                "new_thumbnail.jpg", b"file_content", content_type="image/jpeg"
            ),
        )
        videos = Video.objects.all()
        self.assertEqual(videos[0].title, "New Video")
        self.assertEqual(videos[1].title, "Test Video")
