from django.urls import path

from . import views

""" Путь filter/ специально ставим перед url со slug, для того что бы он не
попадал под шаблон поиска фильма по слагу"""

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('filter/', views.FilterMoviesView.as_view(), name='filter-link'),
    path('search/', views.Search.as_view(), name='search-link'),
    path('add-rating/', views.AddStarRating.as_view(), name='add-rating'),
    # path('json-filter/', views.JsonFilterMoviesView.as_view(), name='json-filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add-review'),
    path('actor/<str:slug>/', views.ActorView.as_view(), name='actor-detail'),

]


