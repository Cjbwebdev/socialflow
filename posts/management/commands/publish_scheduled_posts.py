from django.core.management.base import BaseCommand
from posts.publish import publish_due_posts_for_user


class Command(BaseCommand):
    help = 'Publish scheduled posts to connected social accounts.'

    def handle(self, *args, **options):
        results = publish_due_posts_for_user(None)
        if not results:
            self.stdout.write('No scheduled posts ready to publish.')
            return

        for post, success, message in results:
            if success:
                self.stdout.write(self.style.SUCCESS(f'Post {post.pk} published.'))
            else:
                self.stdout.write(self.style.ERROR(f'Post {post.pk} failed: {message}'))
