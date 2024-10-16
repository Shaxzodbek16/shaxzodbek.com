from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from .models import Technology, CVImages, CV, AboutMe
from django.db.utils import IntegrityError


class TechnologyModelTest(TestCase):
    def setUp(self):
        self.technology = Technology.objects.create(
            name="Python",
            description="A high-level programming language"
        )

    def test_technology_creation(self):
        self.assertTrue(isinstance(self.technology, Technology))
        self.assertEqual(self.technology.__str__(), self.technology.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Technology._meta.verbose_name_plural), "Technologies")

    def test_ordering(self):
        Technology.objects.create(name="Java")
        Technology.objects.create(name="C++")
        technologies = Technology.objects.all()
        self.assertEqual(technologies[0].name, "C++")
        self.assertEqual(technologies[1].name, "Java")
        self.assertEqual(technologies[2].name, "Python")


class CVImagesModelTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.cv_image = CVImages.objects.create(
            name="Test Image",
            image=self.image
        )

    def test_cv_images_creation(self):
        self.assertTrue(isinstance(self.cv_image, CVImages))
        self.assertEqual(self.cv_image.__str__(), self.cv_image.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(CVImages._meta.verbose_name_plural), "CV Images")

    def test_image_upload(self):
        self.assertTrue(self.cv_image.image.name.startswith('cv/cvImages/'))


class CVModelTest(TestCase):
    def setUp(self):
        self.technology = Technology.objects.create(name="Python")
        self.cv_image = CVImages.objects.create(name="Test Image",
                                                image=SimpleUploadedFile("test_image.jpg", b"file_content",
                                                                         content_type="image/jpeg"))
        self.cv = CV.objects.create(
            title="My CV",
            description="A great CV",
            file=SimpleUploadedFile("test_cv.pdf", b"file_content", content_type="application/pdf"),
            path="https://example.com/cv",
            created_at=timezone.now(),
            is_working=True
        )
        self.cv.technologies.add(self.technology)
        self.cv.picture.add(self.cv_image)

    def test_cv_creation(self):
        self.assertTrue(isinstance(self.cv, CV))
        self.assertEqual(self.cv.__str__(), "My CV")

    def test_slug_generation(self):
        self.assertEqual(self.cv.slug, "my-cv")

    def test_unique_slug(self):
        with self.assertRaises(IntegrityError):
            CV.objects.create(
                title="My CV",
                description="Another CV",
                created_at=timezone.now()
            )

    def test_updating_title_updates_slug(self):
        self.cv.title = "Updated CV Title"
        self.cv.save()
        self.assertEqual(self.cv.slug, "updated-cv-title")

    def test_many_to_many_relationships(self):
        self.assertEqual(self.cv.technologies.count(), 1)
        self.assertEqual(self.cv.picture.count(), 1)

    def test_verbose_name_plural(self):
        self.assertEqual(str(CV._meta.verbose_name_plural), "CVs")

    def test_ordering(self):
        CV.objects.create(title="Older CV", description="Old", created_at=timezone.now() - timezone.timedelta(days=1))
        cvs = CV.objects.all()
        self.assertEqual(cvs[0].title, "My CV")
        self.assertEqual(cvs[1].title, "Older CV")


class AboutMeModelTest(TestCase):
    def setUp(self):
        self.about_me = AboutMe.objects.create(
            title="About John Doe",
            description="A passionate developer",
            image=SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg"),
            extra_data="Some extra info",
            location="New York, USA",
            created_at=timezone.now()
        )

    def test_about_me_creation(self):
        self.assertTrue(isinstance(self.about_me, AboutMe))
        self.assertEqual(self.about_me.__str__(), self.about_me.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(AboutMe._meta.verbose_name_plural), "About Me")

    def test_image_upload(self):
        self.assertTrue(self.about_me.image.name.startswith('cv/aboutMe/'))

    def test_optional_fields(self):
        optional_about_me = AboutMe.objects.create(
            title="Minimal About Me",
            created_at=timezone.now()
        )
        self.assertIsNone(optional_about_me.extra_data)
        self.assertIsNone(optional_about_me.location)

    def test_ordering(self):
        AboutMe.objects.create(title="Older Entry", created_at=timezone.now() - timezone.timedelta(days=1))
        entries = AboutMe.objects.all()
        self.assertEqual(entries[0].title, "About John Doe")
        self.assertEqual(entries[1].title, "Older Entry")
