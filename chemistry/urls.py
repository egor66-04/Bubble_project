from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'chemistry'

urlpatterns = [
    path('', lambda request: redirect('chemistry:element_list'), name='chemistry_index'),
    path('elements/', views.ElementListView.as_view(), name='element_list'),
    path('periodic-table/', views.periodic_table, name='periodic_table'),
    path('elements/<int:pk>/', views.ElementDetailView.as_view(), name='element_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('states/', views.state_list, name='state_list'),
    path('states/<int:pk>/', views.state_detail, name='state_detail'),
    path('reactions/', views.reaction_list, name='reaction_list'),
    path('reactions/<int:pk>/', views.reaction_detail, name='reaction_detail'),
    path('uses/', views.use_list, name='use_list'),
    path('uses/<int:pk>/', views.use_detail, name='use_detail'),
    path('facts/', views.fact_list, name='fact_list'),
    path('facts/<int:pk>/', views.fact_detail, name='fact_detail'),
    path('search/', views.search, name='chemistry_search'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:pk>/take/', views.take_quiz, name='take_quiz'),
    path('api/elements/', views.ElementListAPIView, name='api_element_list'),
    path('api/elements/<int:pk>/', views.ElementDetailAPIView, name='api_element_detail'),
    path('api/elements/toggle-favorite/<int:pk>/', views.toggle_favorite_element, name='toggle_favorite_element'),
    path('api/toggle-favorite-element/', views.toggle_favorite_element, name='toggle_favorite_element_api'),
    path('api/reactions/check/<int:element1_id>/<int:element2_id>/', views.api_check_reaction, name='api_check_reaction'),
] 