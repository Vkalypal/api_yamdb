import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment


class Command(BaseCommand):
    help = 'Imports data from CSV files'

    def handle(self, *args, **options):
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_genre_titles()
        # self.import_reviews()
        # self.import_comments()
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))

    def import_categories(self):
        Category.objects.all().delete()
        with open('static/data/category.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category(id=row['id'], name=row['name'], slug=row['slug'])
                category.save()

    def import_genres(self):
        Genre.objects.all().delete()
        with open('static/data/genre.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
                genre.save()

    def import_titles(self):
        Title.objects.all().delete()
        with open('static/data/titles.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_id = row['category']
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    continue

                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
                title.save()

    def import_genre_titles(self):
        GenreTitle.objects.all().delete()
        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title_id = row['title_id']
                genre_id = row['genre_id']
                try:
                    title = Title.objects.get(id=title_id)
                    genre = Genre.objects.get(id=genre_id)
                except (Title.DoesNotExist, Genre.DoesNotExist):
                    continue

                genre_title = GenreTitle(
                    title=title,
                    genre=genre
                )
                genre_title.save()

    # def import_reviews(self):
    #     Review.objects.all().delete()
    #     with open('static/data/review.csv', 'r', encoding='utf-8') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             title_id = row['title_id']
    #             try:
    #                 title = Title.objects.get(id=title_id)
    #             except Title.DoesNotExist:
    #                 continue

    #             review = Review(
    #                 title=title,
    #                 text=row['text'],
    #                 author_id=row['author_id'],
    #                 score=row['score']
    #             )
    #             review.save()

    # def import_comments(self):
    #     Comment.objects.all().delete()
    #     with open('static/data/comments.csv', 'r', encoding='utf-8') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             review_id = row['review_id']
    #             try:
    #                 review = Review.objects.get(id=review_id)
    #             except Review.DoesNotExist:
    #                 continue

    #             comment = Comment(
    #                 review=review,
    #                 text=row['text'],
    #                 author_id=row['author_id']
    #             )
    #             comment.save()