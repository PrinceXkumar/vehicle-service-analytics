"""
Management command to populate the database with sample data for testing analytics.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from services.models import Profile, Service, Vehicle

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for analytics testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of sample services to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(f'Creating {count} sample services...')
        
        # Create sample users if they don't exist
        self.create_sample_users()
        
        # Get existing users
        customers = User.objects.filter(profile__role=Profile.ROLE_CUSTOMER)
        mechanics = User.objects.filter(profile__role=Profile.ROLE_MECHANIC)
        
        if not customers.exists():
            self.stdout.write(self.style.ERROR('No customers found. Please create some users first.'))
            return
            
        if not mechanics.exists():
            self.stdout.write(self.style.ERROR('No mechanics found. Please create some users first.'))
            return
        
        # Create sample vehicles for customers
        self.create_sample_vehicles(customers)
        
        # Create sample services
        self.create_sample_services(customers, mechanics, count)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} sample services!')
        )

    def create_sample_users(self):
        """Create sample users if they don't exist."""
        # Create a manager
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                email='manager@example.com',
                password='password123',
                first_name='Alice',
                last_name='Manager'
            )
            Profile.objects.get_or_create(
                user=manager,
                defaults={
                    'role': Profile.ROLE_MANAGER,
                    'phone': '555-0101',
                    'address': '123 Manager St'
                }
            )
            self.stdout.write('Created manager user')

        # Create sample customers
        customer_data = [
            ('john_doe', 'john@example.com', 'John', 'Doe'),
            ('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
            ('bob_wilson', 'bob@example.com', 'Bob', 'Wilson'),
            ('alice_brown', 'alice@example.com', 'Alice', 'Brown'),
        ]
        
        for username, email, first_name, last_name in customer_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': Profile.ROLE_CUSTOMER,
                        'phone': f'555-{random.randint(1000, 9999)}',
                        'address': f'{random.randint(100, 999)} Customer St'
                    }
                )

        # Create sample mechanics
        mechanic_data = [
            ('mike_mechanic', 'mike@example.com', 'Mike', 'Johnson'),
            ('sarah_tech', 'sarah@example.com', 'Sarah', 'Davis'),
            ('tom_repair', 'tom@example.com', 'Tom', 'Wilson'),
        ]
        
        for username, email, first_name, last_name in mechanic_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': Profile.ROLE_MECHANIC,
                        'phone': f'555-{random.randint(1000, 9999)}',
                        'address': f'{random.randint(100, 999)} Mechanic St'
                    }
                )

    def create_sample_vehicles(self, customers):
        """Create sample vehicles for customers."""
        makes = ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Nissan', 'Hyundai']
        models = ['Camry', 'Civic', 'Focus', 'X3', 'C-Class', 'A4', 'Altima', 'Elantra']
        
        for customer in customers:
            if not customer.vehicles.exists():
                make = random.choice(makes)
                model = random.choice(models)
                year = random.randint(2015, 2023)
                
                Vehicle.objects.create(
                    owner=customer,
                    make=make,
                    model=model,
                    year=year,
                    vin=f'VIN{random.randint(100000, 999999)}',
                    registration_number=f'REG{random.randint(1000, 9999)}',
                    mileage=random.randint(10000, 100000)
                )

    def create_sample_services(self, customers, mechanics, count):
        """Create sample services with realistic data."""
        service_types = [
            Service.SERVICE_OIL_CHANGE,
            Service.SERVICE_TYRE_REPLACEMENT,
            Service.SERVICE_BRAKE_INSPECTION,
            Service.SERVICE_GENERAL_CHECKUP,
        ]
        
        statuses = [
            Service.STATUS_PENDING,
            Service.STATUS_IN_PROGRESS,
            Service.STATUS_COMPLETED,
        ]
        
        # Create services over the last 12 months
        now = timezone.now()
        start_date = now - timedelta(days=365)
        
        for i in range(count):
            # Random date within the last year
            days_ago = random.randint(0, 365)
            created_at = now - timedelta(days=days_ago)
            
            # Create service
            service = Service.objects.create(
                customer=random.choice(customers),
                service_type=random.choice(service_types),
                status=random.choice(statuses),
                created_at=created_at
            )
            
            # Assign mechanic for some services
            if random.random() > 0.3:  # 70% chance of being assigned
                service.assigned_mechanic = random.choice(mechanics)
                service.save()
