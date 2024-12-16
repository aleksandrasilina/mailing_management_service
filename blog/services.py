from django.core.cache import cache

from blog.models import Article
from config.settings import CACHE_ENABLED


def get_article_list_from_cache():
    """Получает данные по статьям блога из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Article.objects.all()
    key = 'article_list'
    articles = cache.get(key)
    if articles is not None:
        return articles
    articles = Article.objects.all()
    cache.get(key, articles)
    return articles
