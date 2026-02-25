import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from studentorg.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = "Create initial fake data for PSUSphere (college, program, org, students, memberships)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing studentorg data first, then create fresh fake data.",
        )

    def handle(self, *args, **options):
        should_reset = options["reset"]
        fake = Faker("en_PH")

        college_count = 5
        program_count = 12
        org_count = 10
        student_count = 50
        membership_count = 120

        if should_reset:
            self.stdout.write(self.style.WARNING("Reset mode enabled. Deleting existing data..."))
            OrgMember.objects.all().delete()
            Student.objects.all().delete()
            Organization.objects.all().delete()
            Program.objects.all().delete()
            College.objects.all().delete()
        else:
            existing_total = (
                College.objects.count()
                + Program.objects.count()
                + Organization.objects.count()
                + Student.objects.count()
                + OrgMember.objects.count()
            )
            if existing_total > 0:
                self.stdout.write(
                    self.style.WARNING(
                        "Existing data detected. Seed skipped to avoid duplicates. "
                        "Use `python manage.py create_initial_data --reset` to recreate clean data."
                    )
                )
                return

        self.stdout.write(self.style.WARNING("Creating initial data..."))

        colleges = self._create_colleges(fake, college_count)
        programs = self._create_programs(fake, program_count, colleges)
        orgs = self._create_organizations(fake, org_count, colleges)
        students = self._create_students(fake, student_count, programs)
        self._create_memberships(fake, membership_count, students, orgs)

        self.stdout.write(self.style.SUCCESS("Initial data created successfully!"))

    def _create_colleges(self, fake: Faker, count: int):
        colleges = []
        for _ in range(count):
            college = College.objects.create(college_name=f"{fake.word().title()} College")
            colleges.append(college)

        self.stdout.write(self.style.SUCCESS(f"Created {len(colleges)} colleges."))
        return colleges

    def _create_programs(self, fake: Faker, count: int, colleges):
        programs = []
        for _ in range(count):
            program = Program.objects.create(
                prog_name=f"{fake.word().title()} Program",
                college=random.choice(colleges),
            )
            programs.append(program)

        self.stdout.write(self.style.SUCCESS(f"Created {len(programs)} programs."))
        return programs

    def _create_organizations(self, fake: Faker, count: int, colleges):
        orgs = []
        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            name = " ".join(words).title()

            org = Organization.objects.create(
                name=name,
                college=random.choice(colleges),
                description=fake.sentence(),
            )
            orgs.append(org)

        self.stdout.write(self.style.SUCCESS(f"Created {len(orgs)} organizations."))
        return orgs

    def _create_students(self, fake: Faker, count: int, programs):
        students = []
        for _ in range(count):
            student_id = fake.unique.bothify(text="20##-#-####")

            student = Student.objects.create(
                student_id=student_id,
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=random.choice(programs),
            )
            students.append(student)

        self.stdout.write(self.style.SUCCESS(f"Created {len(students)} students."))
        return students

    def _create_memberships(self, fake: Faker, count: int, students, orgs):
        created = 0
        attempts = 0

        while created < count and attempts < count * 3:
            attempts += 1

            student = random.choice(students)
            org = random.choice(orgs)
            days_back = random.randint(1, 730)
            joined = date.today() - timedelta(days=days_back)

            OrgMember.objects.create(
                student=student,
                organization=org,
                date_joined=joined,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} organization memberships."))
