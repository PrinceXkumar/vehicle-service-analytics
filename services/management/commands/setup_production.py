from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Profile
import os


class Command(BaseCommand):
    help = 'Set up production environment with superuser and sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser for admin access',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for superuser (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for superuser (default: admin@example.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for superuser (default: admin123)',
        )

    def handle(self, *args, **options):
        if options['create_superuser']:
            username = options['username']
            email = options['email']
            password = options['password']
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists')
                )
            else:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                # Create profile for superuser
                Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': Profile.ROLE_MANAGER,
                        'phone': '000-000-0000',
                        'address': 'Admin Address'
                    }
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser {username} created successfully')
                )

        self.stdout.write(
            self.style.SUCCESS('Production setup completed')
        )
