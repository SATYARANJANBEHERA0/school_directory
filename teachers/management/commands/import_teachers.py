
import csv
from django.core.management.base import BaseCommand
from teachers.models import Teacher

class Command(BaseCommand):
    help = 'Import teachers from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Teacher.objects.create(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email Address'],
                    profile_picture=row['Profile Picture'],
                    phone_number=row['Phone Number'],
                    room_number=row['Room Number'],
                )
