from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.core.cache import cache

from .models import (
    User, UserFavoriteElement, UserAchievement, LearningProgress,
    UserQuizResult, Quiz, QuizQuestion, QuizAnswer, Achievement
)
from chemistry.models import Element, ChemicalReaction
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm

def logout_view(request):
    """Выход из системы"""
    auth_logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти в систему.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """Профиль пользователя"""
    from django.db.models import Count, Q
    
    # Оптимизация: один запрос вместо нескольких
    progress_stats = LearningProgress.objects.filter(user=request.user).aggregate(
        learned=Count('id', filter=Q(is_learned=True)),
        total=Count('id')
    )
    
    learned_elements_count = progress_stats['learned']
    
    # Общее количество элементов в системе
    total_elements_count = Element.objects.filter(is_active=True).count()
    
    # Процент изученных элементов
    if total_elements_count > 0:
        learning_progress_percent = int((learned_elements_count / total_elements_count) * 100)
    else:
        learning_progress_percent = 0
    
    # Последние 5 изученных элементов с оптимизацией
    recent_elements = LearningProgress.objects.filter(
        user=request.user
    ).select_related('element').order_by('-last_interaction')[:5]
    
    # Последние достижения с оптимизацией
    recent_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-achieved_at')[:5]
    
    # Статистика по тестам одним запросом
    quiz_stats = UserQuizResult.objects.filter(user=request.user).aggregate(
        count=Count('id'),
        total_score=Sum('score'),
        total_max=Sum('max_score')
    )
    
    quiz_completed_count = quiz_stats['count'] or 0
    
    if quiz_stats['total_max'] and quiz_stats['total_max'] > 0:
        avg_quiz_score_percent = int((quiz_stats['total_score'] / quiz_stats['total_max']) * 100)
    else:
        avg_quiz_score_percent = 0
    
    # XP до следующего уровня
    current_level = request.user.level
    next_level = current_level + 1
    xp_for_next_level = next_level * 100
    xp_needed = xp_for_next_level - request.user.xp_points
    
    # Расчет прогресса к следующему уровню (в процентах)
    level_progress_percent = int((request.user.xp_points - (current_level - 1) * 100) / 100 * 100)
    
    context = {
        'user': request.user,
        'learned_elements_count': learned_elements_count,
        'total_elements_count': total_elements_count,
        'learning_progress_percent': learning_progress_percent,
        'recent_elements': recent_elements,
        'recent_achievements': recent_achievements,
        'quiz_completed_count': quiz_completed_count,
        'avg_quiz_score_percent': avg_quiz_score_percent,
        'xp_needed': xp_needed,
        'level_progress_percent': level_progress_percent,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    """Изменение пароля пользователя"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессию, чтобы пользователь не вышел из системы
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успешно изменен!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/change_password.html', context)

def check_and_award_achievement(user, achievement_type):
    """
    Проверяет и выдает достижение пользователю, если оно еще не получено
    
    Args:
        user: Пользователь, который может получить достижение
        achievement_type: Тип достижения, которое нужно проверить
        
    Returns:
        UserAchievement или None: Возвращает объект достижения, если оно было выдано, или None
    """
    from django.db import transaction
    
    # Если пользователь не аутентифицирован, не выдаем достижение
    if not user.is_authenticated:
        return None
    
    # Проверяем, существует ли достижение данного типа
    achievements = Achievement.objects.filter(achievement_type=achievement_type)
    if not achievements.exists():
        return None
    
    # Берем первое достижение с данным типом
    achievement = achievements.first()
    
    # Проверяем, не получил ли пользователь уже это достижение
    if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
        return None
    
    # Проверим, соответствует ли пользователь требованиям достижения
    if user.level < achievement.required_level:
        return None
    
    # Используем транзакцию для атомарности
    with transaction.atomic():
        # Выдаем достижение
        user_achievement = UserAchievement.objects.create(
            user=user,
            achievement=achievement
        )
        
        # Начисляем опыт пользователю
        if achievement.xp_reward > 0:
            # Блокируем пользователя для обновления
            locked_user = User.objects.select_for_update().get(pk=user.pk)
            locked_user.xp_points += achievement.xp_reward
            
            # Проверяем повышение уровня
            new_level = locked_user.level
            while locked_user.xp_points >= new_level * 100:
                new_level += 1
            
            # Если уровень изменился, обновляем его
            if new_level > locked_user.level:
                locked_user.level = new_level
            
            locked_user.save()
            
            # Обновляем данные в памяти
            user.refresh_from_db()
    
    return user_achievement

@login_required
def achievements(request):
    """Страница достижений пользователя"""
    # Полученные достижения
    user_achievements = UserAchievement.objects.filter(user=request.user).order_by('-achieved_at')
    
    # Получаем все возможные достижения для отображения
    all_achievements = Achievement.objects.all()
    
    # Создаем словарь для отслеживания полученных и неполученных достижений
    achievements_dict = {achievement.id: {'achievement': achievement, 'is_earned': False} 
                          for achievement in all_achievements}
    
    # Отмечаем полученные достижения
    for ua in user_achievements:
        if ua.achievement.id in achievements_dict:
            achievements_dict[ua.achievement.id]['is_earned'] = True
            achievements_dict[ua.achievement.id]['user_achievement'] = ua
    
    # Преобразуем словарь в список для шаблона
    achievements_list = list(achievements_dict.values())
    
    context = {
        'user_achievements': user_achievements,
        'all_achievements': achievements_list,
    }
    
    # Проверяем и выдаем достижение "Первое действие" при посещении страницы достижений
    check_and_award_achievement(request.user, 'first_action')
    
    return render(request, 'accounts/achievements.html', context)

@login_required
def learning_progress(request):
    """Страница прогресса обучения пользователя"""
    # Прогресс изучения элементов с оптимизацией
    element_progress = LearningProgress.objects.filter(
        user=request.user
    ).select_related('element', 'element__category').order_by('-progress_percent')
    
    # Статистика по прогрессу
    total_elements = Element.objects.filter(is_active=True).count()
    learned_elements = element_progress.filter(is_learned=True).count()
    in_progress_elements = element_progress.filter(is_learned=False, progress_percent__gt=0).count()
    not_started_elements = total_elements - learned_elements - in_progress_elements
    
    # Процент общего прогресса
    if total_elements > 0:
        total_progress_percent = int(learned_elements / total_elements * 100)
    else:
        total_progress_percent = 0
    
    context = {
        'element_progress': element_progress,
        'total_elements': total_elements,
        'learned_elements': learned_elements,
        'in_progress_elements': in_progress_elements,
        'not_started_elements': not_started_elements,
        'total_progress_percent': total_progress_percent,
    }
    
    return render(request, 'accounts/learning_progress.html', context)

@login_required
def favorite_elements(request):
    """Показать избранные элементы пользователя"""
    # Оптимизация: select_related для категории
    favorite_elements = request.user.favorite_elements.select_related('category').all()
    return render(request, 'accounts/favorite_elements.html', {
        'favorite_elements': favorite_elements
    })

@login_required
def favorite_reactions(request):
    """Отображает список избранных реакций пользователя."""
    user = request.user
    # Оптимизация: prefetch_related для M2M полей
    favorite_reactions = user.favorite_reactions.prefetch_related('reactants', 'products').all().order_by('-id')
    
    return render(request, 'accounts/favorite_reactions.html', {
        'favorite_reactions': favorite_reactions,
    })

@login_required
@require_POST
def toggle_favorite_reaction(request):
    """Добавляет или удаляет реакцию из избранного."""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
        reaction_id = request.POST.get('reaction_id')
        if not reaction_id:
            return JsonResponse({'success': False, 'error': 'Не указан ID реакции'})
        
        try:
            reaction = ChemicalReaction.objects.get(id=reaction_id)
        except ChemicalReaction.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Реакция не найдена'})
        
        user = request.user
        is_favorite = user.favorite_reactions.filter(id=reaction.id).exists()
        
        if is_favorite:
            user.favorite_reactions.remove(reaction)
            is_now_favorite = False
        else:
            user.favorite_reactions.add(reaction)
            is_now_favorite = True
        
        return JsonResponse({
            'success': True, 
            'is_favorite': is_now_favorite,
            'count': user.favorite_reactions.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Некорректный запрос'})

@login_required
def add_to_favorites(request, element_id):
    """Добавление элемента в избранное"""
    element = get_object_or_404(Element, id=element_id, is_active=True)
    
    # Проверяем, не добавлен ли элемент уже в избранное
    if not UserFavoriteElement.objects.filter(user=request.user, element=element).exists():
        UserFavoriteElement.objects.create(user=request.user, element=element)
        messages.success(request, f'Элемент {element.name} добавлен в избранное.')
    else:
        messages.info(request, f'Элемент {element.name} уже в избранном.')
    
    # Возвращаемся на страницу элемента
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    else:
        return redirect('chemistry:element_detail', atomic_number=element.atomic_number)

@login_required
def remove_from_favorites(request, element_id):
    """Удаление элемента из избранного"""
    element = get_object_or_404(Element, id=element_id)
    favorite = get_object_or_404(UserFavoriteElement, user=request.user, element=element)
    favorite.delete()
    
    messages.success(request, f'Элемент {element.name} удален из избранного.')
    
    # Возвращаемся на страницу избранного или на страницу элемента
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    elif request.META.get('HTTP_REFERER') and 'favorites' in request.META.get('HTTP_REFERER'):
        return redirect('accounts:favorite_elements')
    else:
        return redirect('chemistry:element_detail', atomic_number=element.atomic_number)

@login_required
def quiz_history(request):
    """История пройденных тестов пользователя"""
    # Оптимизация: select_related для викторины
    quiz_results = UserQuizResult.objects.filter(
        user=request.user
    ).select_related('quiz').order_by('-completed_at')
    
    context = {
        'quiz_results': quiz_results,
    }
    
    return render(request, 'accounts/quiz_history.html', context)

@login_required
def add_reaction_to_favorites(request, reaction_id):
    """Добавление реакции в избранное"""
    reaction = get_object_or_404(ChemicalReaction, id=reaction_id)
    
    # Проверяем, не добавлена ли реакция уже в избранное
    if not request.user.favorite_reactions.filter(id=reaction_id).exists():
        request.user.favorite_reactions.add(reaction)
        messages.success(request, 'Реакция добавлена в избранное!')
    
    # Возвращаемся на страницу реакции
    return redirect('chemistry:reaction_detail', pk=reaction_id)

@login_required
def remove_reaction_from_favorites(request, reaction_id):
    """Удаление реакции из избранного"""
    reaction = get_object_or_404(ChemicalReaction, id=reaction_id)
    
    # Проверяем, есть ли реакция в избранном
    if request.user.favorite_reactions.filter(id=reaction_id).exists():
        request.user.favorite_reactions.remove(reaction)
        messages.success(request, 'Реакция удалена из избранного!')
    
    # Возвращаемся на страницу реакции
    return redirect('chemistry:reaction_detail', pk=reaction_id)

@login_required
def subscription(request):
    """Страница информации о подписке"""
    # Проверяем статус подписки пользователя
    is_subscribed = request.user.is_subscribed
    subscription_end_date = request.user.subscription_end_date
    
    # Проверяем, не истек ли срок подписки
    if is_subscribed and subscription_end_date and subscription_end_date < timezone.now():
        request.user.is_subscribed = False
        request.user.subscription_end_date = None
        request.user.save()
        is_subscribed = False
        subscription_end_date = None
    
    context = {
        'is_subscribed': is_subscribed,
        'subscription_end_date': subscription_end_date,
    }
    
    return render(request, 'accounts/subscription.html', context)

@login_required
def subscription_checkout(request):
    """Страница оформления подписки"""
    # Здесь будет интеграция с платежной системой
    # В данной версии просто отображаем страницу с информацией
    return render(request, 'accounts/subscription_checkout.html')

@login_required
def subscription_success(request):
    """Успешное оформление подписки"""
    # Имитация успешной оплаты - активация подписки на 30 дней
    # В реальном проекте это будет делать платежная система через API
    
    # Устанавливаем статус подписки
    request.user.is_subscribed = True
    
    # Устанавливаем срок подписки на 30 дней от текущей даты
    request.user.subscription_end_date = timezone.now() + timezone.timedelta(days=30)
    request.user.save()
    
    messages.success(request, 'Поздравляем! Ваша подписка успешно активирована.')
    
    return redirect('accounts:subscription')

@login_required
def check_new_achievements_api(request):
    """API для проверки новых достижений пользователя"""
    # Получаем все достижения пользователя с оптимизацией
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-achieved_at')
    
    # Создаем ключ для кэша
    cache_key = f"user_{request.user.id}_shown_achievements"
    
    # Получаем ID последнего показанного достижения
    shown_achievement_ids = cache.get(cache_key, [])
    
    # Находим новые достижения
    new_achievements = []
    for user_achievement in user_achievements:
        if user_achievement.id not in shown_achievement_ids:
            achievement = user_achievement.achievement
            new_achievements.append({
                'id': achievement.id,
                'name': achievement.name,
                'description': achievement.description,
                'xp_reward': achievement.xp_reward,
                'icon': achievement.icon,
                'emoji': achievement.emoji or '🏆'
            })
            # Добавляем в список показанных
            shown_achievement_ids.append(user_achievement.id)
    
    # Обновляем кэш
    cache.set(cache_key, shown_achievement_ids, 86400)  # Храним 24 часа
    
    return JsonResponse({
        'success': True,
        'new_achievements': new_achievements
    })
