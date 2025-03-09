from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker
from blog.models import (
    Article,
    ProgrammingLanguage,
    Education,
    Certification,
    Type,
    Project,
)

# Initialize Faker
fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data using Faker and random images"

    def handle(self, *args, **options):
        self.stdout.write("Populating database...")

        self.create_programming_languages(20)
        self.create_types(20)
        self.create_articles(100)
        self.create_education(100)
        self.create_certifications(100)
        self.create_projects(100)

        self.stdout.write(self.style.SUCCESS("Database successfully populated!"))

    def get_random_image(self, width=600, height=400):
        """Fetches a random image from Lorem Picsum"""
        return f"https://picsum.photos/{width}/{height}"

    def create_programming_languages(self, count):
        languages = [
            "Python",
            "JavaScript",
            "Java",
            "C#",
            "PHP",
            "Ruby",
            "Swift",
            "Go",
            "Rust",
            "TypeScript",
            "Kotlin",
            "Scala",
            "R",
            "Perl",
            "Dart",
            "Haskell",
            "Elixir",
            "Clojure",
            "F#",
        ]

        ProgrammingLanguage.objects.all().delete()

        for i in languages[: min(count, len(languages))]:
            ProgrammingLanguage.objects.create(
                name=i,
                started_from=fake.date_time_between(
                    start_date="-5y",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                image=self.get_random_image(),
            )
        self.stdout.write(f"Created {min(count, len(languages))} programming languages")

    def create_types(self, count):
        types = [
            "Mobile App",
            "API",
            "Desktop App",
            "Game",
            "Data Analysis",
            "Machine Learning",
            "DevOps",
            "Library",
            "Framework",
            "Script",
            "Tool",
            "Plugin",
            "Extension",
            "Microservice",
            "Bot",
            "CLI",
            "Database",
            "Testing",
            "Security",
        ]

        Type.objects.all().delete()

        for i in types:
            Type.objects.create(name=i)
        self.stdout.write(f"Created {min(count, len(types))} project types")

    def create_articles(self, count):
        Article.objects.all().delete()

        for i in range(count):
            Article.objects.create(
                title=f"{fake.catch_phrase()} {i}",
                content1="\n\n".join(fake.paragraphs(5)),
                content2="\n\n".join(fake.paragraphs(3)),
                created=fake.date_time_between(
                    start_date="-2y",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                visible=random.choice([True, True, True, False]),  # 75% visible
                image=self.get_random_image(),
            )
        self.stdout.write(f"Created {count} articles")

    def create_education(self, count):
        Education.objects.all().delete()

        for i in range(count):
            start_date = fake.date_time_between(
                start_date="-10y",
                end_date="-2y",
                tzinfo=timezone.get_current_timezone(),
            )
            end_date = start_date + timedelta(days=random.randint(365, 1460))
            Education.objects.create(
                name=f"{fake.random_element(['BS', 'MS', 'PhD', 'Certificate'])} in {fake.job()} {i}",
                description=fake.text(max_nb_chars=500),
                field=fake.job(),
                started_from=start_date,
                ended_at=end_date,
                image=self.get_random_image(),
            )
        self.stdout.write(f"Created {count} education entries")

    def create_certifications(self, count):
        Certification.objects.all().delete()

        for i in range(count):
            Certification.objects.create(
                name=f"{fake.company()} {fake.random_element(['Professional', 'Associate', 'Expert', 'Master'])} Certification {i}",
                description=fake.text(max_nb_chars=400),
                took_at=fake.date_time_between(
                    start_date="-3y",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                image=self.get_random_image(),
            )
        self.stdout.write(f"Created {count} certifications")

    def create_projects(self, count):
        Project.objects.all().delete()

        programming_languages = list(ProgrammingLanguage.objects.all())
        project_types = list(Type.objects.all())

        for i in range(count):
            end_date = fake.date_time_between(
                start_date="-2y", end_date="now", tzinfo=timezone.get_current_timezone()
            )
            start_date = end_date - timedelta(days=random.randint(30, 365))
            project = Project.objects.create(
                name=f"{fake.random_element(['Build', 'Create', 'Develop'])} {fake.catch_phrase()} {i}",
                description=fake.text(max_nb_chars=600),
                link_to_project=fake.url() if random.random() > 0.3 else None,
                github_link=(
                    f"https://github.com/{fake.user_name()}/{fake.slug()}"
                    if random.random() > 0.2
                    else None
                ),
                started_from=start_date,
                ended_at=end_date,
                image=self.get_random_image(),
            )

            if programming_languages:
                for lang in random.sample(
                    programming_languages,
                    random.randint(1, min(4, len(programming_languages))),
                ):
                    project.programming_languages.add(lang)

            if project_types:
                for proj_type in random.sample(
                    project_types, random.randint(1, min(2, len(project_types)))
                ):
                    project.type.add(proj_type)

        self.stdout.write(f"Created {count} projects")
