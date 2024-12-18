import instaloader
from django.core.management.base import BaseCommand
from api.models import *
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch Instagram posts and save data to the database'

    def handle(self, *args, **kwargs):
        # Initialize Instaloader
        loader = instaloader.Instaloader()

        profile = instaloader.Profile.from_username(loader.context, "r_o_l_l_n_o_004")
        
        for post in profile.get_posts():
                obj, created = IGCommerce.objects.update_or_create(
                    shortcode = post.shortcode,
                    defaults = {
                        'media_id':post.mediaid,
                        'thumbnail':post.url,
                        'video':post.video_url if post.is_video else None,
                        'likes':post.likes,
                        'comments':post.comments
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {obj}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated: {obj}"))
        self.stdout.write(self.style.SUCCESS(f'Post fetching and saving completed at {datetime.now()} .'))
