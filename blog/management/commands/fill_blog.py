from django.core.management import BaseCommand

from blog.models import Article
import json


class Command(BaseCommand):
    """Команда для наполнения блога статьями"""

    @staticmethod
    def json_read_articles():
        articles = []
        with open("blog.json", "r", encoding="utf-8") as file:
            for article in json.load(file):
                if article["model"] == "blog.article":
                    articles.append(article["fields"])
        return articles

    def handle(self, *args, **options):
        Article.objects.all().delete()
        Article.truncate_table_restart_id()
        articles_for_create = []

        for article in Command.json_read_articles():
            articles_for_create.append(Article(**article))

        Article.objects.bulk_create(articles_for_create)

        print("Articles successfully сreated!")
