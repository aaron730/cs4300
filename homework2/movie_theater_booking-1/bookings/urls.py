from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('cancel/', views.cancel_booking, name='cancel_booking'),
]