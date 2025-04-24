from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Регистрация
    path('register/', views.register, name='register'),
    
    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/achievements/', views.achievements, name='achievements'),
    path('profile/learning-progress/', views.learning_progress, name='learning_progress'),
    path('profile/favorite-elements/', views.favorite_elements, name='favorite_elements'),
    path('profile/favorite-reactions/', views.favorite_reactions, name='favorite_reactions'),
    path('toggle-favorite-reaction/', views.toggle_favorite_reaction, name='toggle_favorite_reaction'),
    
    # API для достижений
    path('api/check-new-achievements/', views.check_new_achievements_api, name='check_new_achievements_api'),
    
    # Восстановление пароля
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Достижения и прогресс
    path('achievements/', views.achievements, name='achievements'),
    path('progress/', views.learning_progress, name='learning_progress'),
    
    # Избранные элементы
    path('favorite-elements/', views.favorite_elements, name='favorite_elements'),
    path('add-to-favorites/<int:element_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:element_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    
    # Избранные реакции
    path('add-reaction-to-favorites/<int:reaction_id>/', views.add_reaction_to_favorites, name='add_reaction_to_favorites'),
    path('remove-reaction-from-favorites/<int:reaction_id>/', views.remove_reaction_from_favorites, name='remove_reaction_from_favorites'),
    
    # История тестов
    path('quiz-history/', views.quiz_history, name='quiz_history'),
    
    # Подписка
    path('subscription/', views.subscription, name='subscription'),
    path('subscription/checkout/', views.subscription_checkout, name='subscription_checkout'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
] 