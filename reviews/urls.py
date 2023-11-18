# reviews/urls.py
from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView
from . import views

urlpatterns = [
    path('lista_reviews/', ReviewListView.as_view(), name='review-list'),
    path('add_review/', views.add_review, name='add_review'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
