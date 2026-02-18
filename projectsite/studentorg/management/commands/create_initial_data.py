from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import date, timedelta

from studentorg.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = "Create initial fake data for PSUSphere (college, program, org, students, memberships)"

    def handle(self, *args, **options):
        fake = Faker("en_PH")

        # You can adjust counts here
        college_count = 5
        program_count = 12
        org_count = 10
        student_count = 50
        membership_count = 120

        self.stdout.write(self.style.WARNING("Creating initial data..."))

        colleges = self._create_colleges(fake, college_count)
        programs = self._create_programs(fake, program_count, colleges)
        orgs = self._create_organizations(fake, org_count, colleges)
        students = self._create_students(fake, student_count, programs)
        self._create_memberships(fake, membership_count, students, orgs)

        self.stdout.write(self.style.SUCCESS("Initial data created successfully!"))

    # -------------------------
    # Create helper methods
    # -------------------------

    def _create_colleges(self, fake: Faker, count: int):
        colleges = []
        for _ in range(count):
            college = College.objects.create(
                college_name=f"{fake.word().title()} College"
            )
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
                college=random.choice(colleges),  # optional FK in your model; OK to set
                description=fake.sentence(),
            )
            orgs.append(org)

        self.stdout.write(self.style.SUCCESS(f"Created {len(orgs)} organizations."))
        return orgs

    def _create_students(self, fake: Faker, count: int, programs):
        students = []
        for _ in range(count):
            # student_id format: YYYY-X-NNNN (based on your PDF pattern)
            student_id = f"{random.randint(2020, 2025)}-{random.randint(1, 8)}-{random.randint(1000, 9999)}"

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

        # We try a bit more than count to avoid duplicate pairs if you later add uniqueness
        while created < count and attempts < count * 3:
            attempts += 1

            student = random.choice(students)
            org = random.choice(orgs)

            # random date within last 2 years
            days_back = random.randint(1, 730)
            joined = date.today() - timedelta(days=days_back)

            OrgMember.objects.create(
                student=student,
                organization=org,
                date_joined=joined,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} organization memberships."))
