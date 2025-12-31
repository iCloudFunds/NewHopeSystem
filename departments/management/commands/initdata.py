from django.core.management.base import BaseCommand
from departments.models import Department, Stream, Floor

class Command(BaseCommand):
    help = 'Initialize department, stream, and floor data'

    def handle(self, *args, **options):
        # Create departments
        departments_data = [
            {'name': 'General Department', 'code': 'GEN'},
            {'name': 'Industrial Department', 'code': 'IND'},
            {'name': 'Commercial Department', 'code': 'COM'},
        ]
        
        created_departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'code': dept_data['code']}
            )
            if created:
                created_departments.append(dept.name)
                
                # Create streams for each department
                Stream.objects.get_or_create(
                    name='first_cycle',
                    department=dept,
                    defaults={'name': 'first_cycle'}
                )
                Stream.objects.get_or_create(
                    name='second_cycle',
                    department=dept,
                    defaults={'name': 'second_cycle'}
                )
        
        # Create floors
        floors_data = [
            {'name': 'down', 'description': 'Down Floor'},
            {'name': 'middle', 'description': 'Middle Floor'},
            {'name': 'top', 'description': 'Top Floor'},
        ]
        
        created_floors = []
        for floor_data in floors_data:
            floor, created = Floor.objects.get_or_create(
                name=floor_data['name'],
                defaults={'description': floor_data['description']}
            )
            if created:
                created_floors.append(floor.description)
        
        if created_departments:
            self.stdout.write(self.style.SUCCESS(f'Successfully created departments: {", ".join(created_departments)}'))
        else:
            self.stdout.write(self.style.WARNING('All departments already exist.'))
        
        if created_floors:
            self.stdout.write(self.style.SUCCESS(f'Successfully created floors: {", ".join(created_floors)}'))
        else:
            self.stdout.write(self.style.WARNING('All floors already exist.'))