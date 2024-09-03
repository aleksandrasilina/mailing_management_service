from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article
from blog.services import get_article_list_from_cache


class ArticleListView(ListView):
    model = Article
    paginate_by = 3
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self):
        return get_article_list_from_cache()


class ArticleDetailView(LoginRequiredMixin,  DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['article'].title
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:articles_list')
    extra_context = {
        'title': 'Создание статьи'
    }


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:articles_list')

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование статьи: {context['article']}'
        return context


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:articles_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {context['article']}'
        return context
