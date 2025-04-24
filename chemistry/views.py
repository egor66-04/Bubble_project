from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Element, ElementCategory, ChemicalReaction, ElementDetail
from accounts.models import LearningProgress, UserQuizResult, Quiz, QuizQuestion, QuizAnswer, UserFavoriteElement
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
import json
from accounts.views import check_and_award_achievement

def element_list(request):
    """Список всех химических элементов"""
    elements = Element.objects.filter(is_active=True)
    
    # Поиск и фильтрация
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        elements = elements.filter(
            Q(name__icontains=search_query) |
            Q(symbol__icontains=search_query) |
            Q(atomic_number__icontains=search_query)
        )
    
    if category_id:
        elements = elements.filter(category_id=category_id)
    
    # Пагинация
    paginator = Paginator(elements, 20)  # 20 элементов на странице
    page = request.GET.get('page')
    elements = paginator.get_page(page)
    
    categories = ElementCategory.objects.all()
    
    context = {
        'elements': elements,
        'categories': categories,
        'search_query': search_query,
        'category_id': int(category_id) if category_id else None,
    }
    
    return render(request, 'chemistry/element_list.html', context)

def periodic_table(request):
    """Представление периодической таблицы"""
    elements = Element.objects.all()
    categories = ElementCategory.objects.all()
    
    # Добавляем информацию для расположения элементов в таблице
    for element in elements:
        if element.atomic_number <= 2:
            element.row = 1
        elif element.atomic_number <= 10:
            element.row = 2
        elif element.atomic_number <= 18:
            element.row = 3
        elif element.atomic_number <= 36:
            element.row = 4
        elif element.atomic_number <= 54:
            element.row = 5
        elif element.atomic_number <= 86:
            element.row = 6
        else:
            element.row = 7
            
        # Вычисление колонки (упрощенный алгоритм)
        if element.group:
            element.column = element.group
        else:
            # Для элементов без указанной группы используем приблизительное позиционирование
            if element.atomic_number in range(57, 72):  # Лантаноиды
                element.column = element.atomic_number - 57 + 3
                element.row = 9
            elif element.atomic_number in range(89, 104):  # Актиноиды
                element.column = element.atomic_number - 89 + 3
                element.row = 10
            else:
                element.column = (element.atomic_number % 18) or 18
    
    return render(request, 'chemistry/periodic_table.html', {
        'elements': elements,
        'categories': categories
    })

def element_detail(request, atomic_number):
    """Подробная информация о химическом элементе"""
    element = get_object_or_404(Element, atomic_number=atomic_number)
    
    # Проверка на избранное (только для авторизованных пользователей)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = request.user.favorite_elements.filter(id=element.id).exists()
        
    # Получение связанных реакций
    reactions = ChemicalReaction.objects.filter(
        Q(reactants=element) | Q(products=element)
    ).distinct()
    
    # Получение связанных элементов (элементы из той же категории, но не более 5)
    related_elements = Element.objects.filter(
        category=element.category
    ).exclude(id=element.id)[:5]
    
    # Если пользователь авторизован, отмечаем элемент как просмотренный
    if request.user.is_authenticated:
        learning_progress, created = LearningProgress.objects.get_or_create(
            user=request.user,
            element=element,
            defaults={'views_count': 1}
        )
        
        if not created:
            learning_progress.views_count += 1
            learning_progress.save()
        
        # Проверяем и выдаем достижение "Первый элемент"
        check_and_award_achievement(request.user, 'first_element')
    
    context = {
        'element': element,
        'is_favorite': is_favorite,
        'reactions': reactions,
        'related_elements': related_elements,
    }
    
    return render(request, 'chemistry/element_detail.html', context)

def category_list(request):
    """Список категорий элементов"""
    return render(request, 'chemistry/category_list.html', {'categories': ElementCategory.objects.all()})

def category_detail(request, pk):
    """Детальная информация о категории"""
    category = get_object_or_404(ElementCategory, pk=pk)
    return render(request, 'chemistry/category_detail.html', {'category': category})

def state_list(request):
    """Список агрегатных состояний"""
    return render(request, 'chemistry/state_list.html', {'states': Element.STATE_CHOICES})

def state_detail(request, pk):
    """Элементы в конкретном агрегатном состоянии"""
    return render(request, 'chemistry/state_detail.html', {'state': pk})

def reaction_list(request):
    """Список химических реакций"""
    reactions = ChemicalReaction.objects.all()
    elements = Element.objects.all()[:10]  # Ограничиваем для демонстрации
    
    return render(request, 'chemistry/reaction_list.html', {
        'reactions': reactions,
        'elements': elements
    })

def reaction_detail(request, pk):
    """Детальная информация о реакции"""
    reaction = get_object_or_404(ChemicalReaction, pk=pk)
    return render(request, 'chemistry/reaction_detail.html', {'reaction': reaction})

def use_list(request):
    """Список применений элементов"""
    return render(request, 'chemistry/use_list.html')

def use_detail(request, pk):
    """Детальная информация о применении"""
    return render(request, 'chemistry/use_detail.html', {'use_id': pk})

def fact_list(request):
    """Список интересных фактов"""
    return render(request, 'chemistry/fact_list.html')

def fact_detail(request, pk):
    """Детальная информация о факте"""
    return render(request, 'chemistry/fact_detail.html', {'fact_id': pk})

def search(request):
    """Поиск по элементам"""
    query = request.GET.get('q', '')
    
    results = []
    if query:
        results = Element.objects.filter(
            Q(name__icontains=query) |
            Q(symbol__icontains=query) |
            Q(atomic_number__icontains=query),
            is_active=True
        ).order_by('atomic_number')
        
        # Проверяем и выдаем достижение "Первый поиск"
        if request.user.is_authenticated:
            check_and_award_achievement(request.user, 'first_search')
    
    context = {
        'query': query,
        'results': results
    }
    
    return render(request, 'chemistry/search.html', context)

@login_required
def quiz_list(request):
    """Список доступных тестов"""
    # Получаем все активные викторины без фильтрации по уровню
    quizzes = Quiz.objects.filter(is_active=True)
    
    # Получаем историю прохождения тестов данным пользователем
    completed_quizzes = UserQuizResult.objects.filter(user=request.user).values_list('quiz_id', flat=True)
    
    # Получаем уровень пользователя для отображения информации о доступности
    user_level = request.user.level
    
    context = {
        'quizzes': quizzes,
        'completed_quizzes': completed_quizzes,
        'user_level': user_level,
    }
    
    return render(request, 'chemistry/quiz_list.html', context)

@login_required
def quiz_detail(request, pk):
    """Информация о тесте перед его прохождением"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    
    # Проверяем, доступен ли тест для уровня пользователя
    if quiz.level > request.user.level:
        messages.error(request, f"Этот тест доступен только с {quiz.level} уровня!")
        return redirect('chemistry:quiz_list')
    
    # Проверяем, проходил ли пользователь тест ранее
    previous_results = UserQuizResult.objects.filter(user=request.user, quiz=quiz).order_by('-completed_at')
    
    context = {
        'quiz': quiz,
        'previous_results': previous_results,
    }
    
    return render(request, 'chemistry/quiz_detail.html', context)

@login_required
def take_quiz(request, pk):
    """Прохождение теста"""
    quiz = get_object_or_404(Quiz, id=pk)
    
    # Проверяем, может ли пользователь проходить этот тест (по уровню)
    if request.user.level < quiz.level:
        return redirect('chemistry:quiz_list')
    
    # Получаем все вопросы для теста
    questions = QuizQuestion.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        score = 0
        max_score = 0
        correct_answers_count = 0
        
        # Обрабатываем ответы пользователя
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = get_object_or_404(QuizAnswer, id=answer_id)
                max_score += question.points
                
                if selected_answer.is_correct:
                    score += question.points
                    correct_answers_count += 1
                else:
                    correct_answers_count = 0  # Сбрасываем счетчик правильных ответов при ошибке
            else:
                max_score += question.points
        
        # Сохраняем результат
        UserQuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            max_score=max_score
        )
        
        # Начисляем опыт пользователю
        xp_earned = int(score / max_score * 10)  # Предполагаем, что max_xp = 10 
        request.user.xp_points += xp_earned
        
        # Проверяем повышение уровня
        new_level = request.user.level
        while request.user.xp_points >= new_level * 100:
            new_level += 1
        
        # Если уровень изменился, обновляем его
        if new_level > request.user.level:
            request.user.level = new_level
        
        request.user.save()
        
        # Проверяем достижения
        check_and_award_achievement(request.user, 'first_quiz')
        
        # Проверяем достижение "Три правильных ответа подряд"
        if correct_answers_count >= 3:
            check_and_award_achievement(request.user, 'three_correct_answers')
        
        # Редирект на страницу результатов
        return redirect('chemistry:quiz_detail', pk=quiz.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    
    return render(request, 'chemistry/take_quiz.html', context)

# API для получения данных о химических элементах
def api_element_list(request):
    """API для получения списка всех элементов"""
    elements = Element.objects.filter(is_active=True)
    
    data = [{
        'id': element.id,
        'name': element.name,
        'symbol': element.symbol,
        'atomic_number': element.atomic_number,
        'category': element.category.name,
        'category_color': element.category.color,
        'period': element.period,
        'group': element.group,
    } for element in elements]
    
    return JsonResponse({'elements': data})

def api_element_detail(request, atomic_number):
    """API для получения детальной информации об элементе"""
    try:
        element = Element.objects.get(atomic_number=atomic_number, is_active=True)
        
        # Базовая информация об элементе
        data = {
            'id': element.id,
            'name': element.name,
            'symbol': element.symbol,
            'atomic_number': element.atomic_number,
            'atomic_weight': element.atomic_weight,
            'category': element.category.name,
            'period': element.period,
            'group': element.group,
            'description': element.description,
            'fun_facts': element.fun_facts,
        }
        
        # Дополнительная информация, если есть
        try:
            details = element.details
            data.update({
                'melting_point': details.melting_point,
                'boiling_point': details.boiling_point,
                'electron_configuration': details.electron_configuration,
                'electronegativity': details.electronegativity,
                'discovery_year': details.discovery_year,
                'discovered_by': details.discovered_by,
            })
        except ElementDetail.DoesNotExist:
            pass
        
        return JsonResponse(data)
    except Element.DoesNotExist:
        return JsonResponse({'error': 'Элемент не найден'}, status=404)

def api_check_reaction(request, element1_id, element2_id):
    """API для проверки реакций между элементами"""
    try:
        element1 = Element.objects.get(id=element1_id)
        element2 = Element.objects.get(id=element2_id)
    except Element.DoesNotExist:
        return JsonResponse({'error': 'Элемент не найден'}, status=404)
    
    return JsonResponse({
        'success': True,
        'element1': element1.symbol,
        'element2': element2.symbol,
        'message': f'Реакция между {element1.name} и {element2.name} возможна'
    })

class ElementListView(ListView):
    model = Element
    template_name = 'chemistry/element_list.html'
    context_object_name = 'elements'
    paginate_by = 20

    def get_queryset(self):
        queryset = Element.objects.filter(is_active=True)
        
        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтр по состоянию
        state = self.request.GET.get('state')
        if state:
            queryset = queryset.filter(state=state)
        
        # Поиск
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(symbol__icontains=query) |
                Q(atomic_number__icontains=query)
            )
        
        return queryset.order_by('atomic_number')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ElementCategory.objects.all()
        context['states'] = Element.STATE_CHOICES
        
        # Сохраняем параметры фильтрации для поддержки пагинации
        context['current_category'] = self.request.GET.get('category', '')
        context['current_state'] = self.request.GET.get('state', '')
        context['current_query'] = self.request.GET.get('q', '')
        
        # Если пользователь аутентифицирован, получаем список избранных элементов
        if self.request.user.is_authenticated:
            favorite_ids = UserFavoriteElement.objects.filter(
                user=self.request.user
            ).values_list('element_id', flat=True)
            context['favorite_element_ids'] = list(favorite_ids)
        
        return context

class ElementDetailView(DetailView):
    model = Element
    template_name = 'chemistry/element_detail.html'
    context_object_name = 'element'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element = self.get_object()
        
        # Получаем связанные реакции
        related_reactions = ChemicalReaction.objects.filter(
            Q(reactants=element) | Q(products=element)
        ).filter(is_active=True).distinct()
        
        context['related_reactions'] = related_reactions
        
        # Проверяем, является ли элемент избранным для пользователя
        if self.request.user.is_authenticated:
            context['is_favorite'] = UserFavoriteElement.objects.filter(
                user=self.request.user,
                element=element
            ).exists()
            
            # Получаем прогресс пользователя по этому элементу
            try:
                element_progress = LearningProgress.objects.get(
                    user=self.request.user,
                    element=element
                )
                context['element_progress'] = element_progress
            except LearningProgress.DoesNotExist:
                pass
        
        return context

@require_POST
@login_required
def toggle_favorite_element(request, element_id=None):
    """Добавляет или удаляет элемент из избранного пользователя"""
    try:
        # Проверяем, есть ли данные JSON в запросе
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            element_id = data.get('element_id')
            
        # Если element_id не был получен ни из URL, ни из JSON, возвращаем ошибку
        if not element_id:
            return JsonResponse({'error': 'Идентификатор элемента не указан'}, status=400)
            
        element = Element.objects.get(id=element_id)
        
        # Проверяем текущее состояние (из JSON данных или из БД)
        is_favorite_param = None
        if request.content_type == 'application/json':
            is_favorite_param = data.get('is_favorite')
            
        # Если состояние было указано в JSON
        if is_favorite_param is not None:
            # Если элемент в избранном, но запрос на удаление
            if is_favorite_param and UserFavoriteElement.objects.filter(user=request.user, element=element).exists():
                UserFavoriteElement.objects.filter(user=request.user, element=element).delete()
                is_favorite = False
            # Если элемент не в избранном, но запрос на добавление
            elif not is_favorite_param and not UserFavoriteElement.objects.filter(user=request.user, element=element).exists():
                UserFavoriteElement.objects.create(user=request.user, element=element)
                is_favorite = True
            else:
                # Состояние уже соответствует запросу
                is_favorite = is_favorite_param
        else:
            # Стандартный подход - переключаем состояние
            favorite, created = UserFavoriteElement.objects.get_or_create(
                user=request.user,
                element=element
            )
            
            if not created:
                # Если запись уже существовала, удаляем её (убираем из избранного)
                favorite.delete()
                is_favorite = False
            else:
                is_favorite = True
        
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'element_id': element_id
        })
    except Element.DoesNotExist:
        return JsonResponse({'error': 'Элемент не найден'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат JSON'}, status=400)

def ElementListAPIView(request):
    """API представление для списка элементов"""
    elements = Element.objects.all()
    data = [{'id': e.id, 'name': e.name, 'symbol': e.symbol} for e in elements]
    return JsonResponse(data, safe=False)

def ElementDetailAPIView(request, pk):
    """API представление для деталей элемента"""
    element = get_object_or_404(Element, pk=pk)
    data = {
        'id': element.id,
        'name': element.name,
        'symbol': element.symbol,
        'atomic_number': element.atomic_number
    }
    return JsonResponse(data)
