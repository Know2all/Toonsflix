import instaloader
from django.core.management.base import BaseCommand
from models import *
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch Instagram posts and save data to the database'

    def handle(self, *args, **kwargs):
        # Initialize Instaloader
        loader = instaloader.Instaloader()

        profile = instaloader.Profile.from_username(loader.context, "r_o_l_l_n_o_004")
        
        for post in profile.get_posts():
            if not IGCommerce.objects.filter(id=post.media_id).exists():
                IGCommerce.objects.create(
                    id=post.media_id,
                    thumbnail=post.url,  # This is just an example, adjust as needed
                    video=post.video_url if post.is_video else None,
                    likes=post.likes,
                    comments=post.comments
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully saved post {post.media_id}'))

        self.stdout.write(self.style.SUCCESS('Data fetching and saving completed.'))
