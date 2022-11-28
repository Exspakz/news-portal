from django.core.management import BaseCommand

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Removes all posts from the selected category'
    missing_args_message = 'Not enough arguments'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Delete all posts from the category "{options["category"]}" (y/n)? ')

        if answer == 'y':
            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category "{category.name}"'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category "{options["category"]}"'))
        else:
            self.stdout.write(self.style.ERROR('Canceled by the user'))
