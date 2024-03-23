from django.urls import path

from news.apps import NewsConfig
from news.views import NewsListView, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView

app_name = NewsConfig.name

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('detail/<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('update/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
]
