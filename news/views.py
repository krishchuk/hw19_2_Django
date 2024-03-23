from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from pytils.translit import slugify

from news.models import News


class NewsListView(ListView):
    model = News
    extra_context = {
        'title': "Новости"
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()

        item = News.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f"{item.title}"

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class NewsCreateView(CreateView):
    model = News
    fields = ('title', 'content', 'picture', 'is_published',)
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Добавить новость"
    }

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'content', 'picture', 'is_published',)
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Изменить новость"
    }

    def get_success_url(self):
        return reverse('news:news_detail', args=[self.kwargs.get('pk')])


class NewsDeleteView(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')
    extra_context = {
        'title': "Удалить новость"
    }
