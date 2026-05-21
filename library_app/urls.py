from django.urls import path
from . import views

urlpatterns = [
    path('reader_list/', views.reader_list, name='reader_list'),  # Главная - читатели
    path('book_list/', views.book_list, name='book_list'),  # Страница книг
]