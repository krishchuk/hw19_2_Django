from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from news.models import News


class NewsListView(ListView):
    model = News
    extra_context = {
        'title': "Новости"
    }


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()

        item = News.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f"{item.title}"

        return context_data


class NewsCreateView(CreateView):
    model = News
    fields = ('title', 'content', 'picture', 'slug', 'is_published',)
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Добавить новость"
    }


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'content', 'picture', 'slug', 'is_published',)
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Изменить новость"
    }


class NewsDeleteView(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Удалить новость"
    }
