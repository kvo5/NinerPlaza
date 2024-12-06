from django.core.management.base import BaseCommand
from base.models import Team

class Command(BaseCommand):
    help = 'Creates the initial four teams/factions'

    def handle(self, *args, **kwargs):
        teams_data = [
            {
                'name': 'EcoTech Solutions',
                'description': 'Pioneering sustainable technology solutions for a greener future. Join us in creating eco-friendly innovations that make a difference.',
                'image': 'team1.jpg'
            },
            {
                'name': 'HealthHub',
                'description': "Revolutionizing healthcare through digital innovation. We're building the future of accessible, efficient healthcare solutions.",
                'image': 'team2.jpg'
            },
            {
                'name': 'FinTech Pioneers',
                'description': 'Transforming financial services through cutting-edge technology. Join us in creating the next generation of financial solutions.',
                'image': 'team3.jpg'
            },
            {
                'name': 'AI Innovators',
                'description': 'Pushing the boundaries of artificial intelligence and machine learning. We are building intelligent solutions for tomorrow\'s challenges.',
                'image': 'team4.jpg'
            }
        ]

        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={
                    'description': team_data['description'],
                    'image': team_data['image']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created team: {team.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Team already exists: {team.name}'))
            
        self.stdout.write(self.style.SUCCESS('Successfully created teams')) 