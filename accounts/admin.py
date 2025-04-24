from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    User, UserFavoriteElement, UserAchievement, LearningProgress, 
    Achievement, Quiz, QuizQuestion, QuizAnswer, UserQuizResult
)

# Расширенная админка для модели пользователя
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Персональная информация'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio', 'birth_date')}),
        (_('Прогресс и уровень'), {'fields': ('xp_points', 'level')}),
        (_('Подписка'), {'fields': ('is_subscribed', 'subscription_end_date')}),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ['collapse'],
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('avatar_thumbnail', 'username', 'email', 'full_name', 'level_badge', 'subscription_status', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_subscribed', 'level', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    list_display_links = ('avatar_thumbnail', 'username')
    list_per_page = 20
    save_on_top = True
    readonly_fields = ('last_login', 'date_joined')
    
    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.avatar.url)
        return format_html('<div style="width: 40px; height: 40px; background-color: #007bff; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{}</div>', obj.username[0].upper())
    avatar_thumbnail.short_description = _("Аватар")
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else "-"
    full_name.short_description = _("Полное имя")
    
    def level_badge(self, obj):
        colors = {
            0: '#6c757d',  # Серый для новичков
            1: '#28a745',  # Зеленый для начинающих
            2: '#17a2b8',  # Голубой для опытных
            3: '#fd7e14',  # Оранжевый для продвинутых
            4: '#dc3545',  # Красный для экспертов
            5: '#6f42c1',  # Фиолетовый для мастеров
        }
        color = colors.get(min(obj.level // 5, 5), '#6c757d')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold;">{}</span>', color, obj.level)
    level_badge.short_description = _("Уровень")
    
    def subscription_status(self, obj):
        if obj.is_subscribed:
            if obj.subscription_end_date:
                return format_html('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> До {}</span>', obj.subscription_end_date.strftime('%d.%m.%Y'))
            return format_html('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Активна</span>')
        return format_html('<span style="color: #dc3545;"><i class="fas fa-times-circle"></i> Нет</span>')
    subscription_status.short_description = _("Подписка")
    
    class Media:
        css = {
            'all': ('css/admin/user_admin.css',)
        }
        js = ('js/admin/user_admin.js',)

# Админка для избранных элементов пользователя
@admin.register(UserFavoriteElement)
class UserFavoriteElementAdmin(admin.ModelAdmin):
    list_display = ('user', 'element_with_symbol', 'added_at')
    list_filter = ('added_at', 'element__category')
    search_fields = ('user__username', 'element__name', 'element__symbol')
    date_hierarchy = 'added_at'
    autocomplete_fields = ['user', 'element']
    list_select_related = ('user', 'element')
    
    def element_with_symbol(self, obj):
        return format_html('{} <span style="color: #6c757d; font-weight: bold;">({})</span>', obj.element.name, obj.element.symbol)
    element_with_symbol.short_description = _("Элемент")

# Админка для достижений
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'achievement_type_badge', 'xp_reward_display', 'required_level', 'icon_display', 'emoji')
    list_filter = ('required_level', 'achievement_type')
    search_fields = ('name', 'description')
    filter_horizontal = ('required_elements',)
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'description', 'achievement_type')
        }),
        (_('Награда и требования'), {
            'fields': ('xp_reward', 'required_level', 'required_elements')
        }),
        (_('Визуализация'), {
            'fields': ('icon', 'emoji')
        }),
    )
    
    def xp_reward_display(self, obj):
        return format_html('<span style="color: #28a745; font-weight: bold;">+{} XP</span>', obj.xp_reward)
    xp_reward_display.short_description = _("Награда XP")
    
    def achievement_type_badge(self, obj):
        colors = {
            'element': '#0d6efd',    # Синий для элементов
            'reaction': '#fd7e14',   # Оранжевый для реакций
            'quiz': '#20c997',       # Зеленоватый для викторин
            'progress': '#6f42c1',   # Фиолетовый для прогресса
            'social': '#e83e8c',     # Розовый для социальных
        }
        color = colors.get(obj.achievement_type, '#6c757d')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px;">{}</span>', 
                          color, dict(Achievement.ACHIEVEMENT_TYPES).get(obj.achievement_type, obj.achievement_type))
    achievement_type_badge.short_description = _("Тип")
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return "-"
    icon_display.short_description = _("Иконка")

# Админка для достижений пользователя
@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement_with_type', 'achieved_at')
    list_filter = ('achieved_at', 'achievement__achievement_type')
    search_fields = ('user__username', 'achievement__name')
    date_hierarchy = 'achieved_at'
    autocomplete_fields = ['user', 'achievement']
    list_select_related = ('user', 'achievement')
    
    def achievement_with_type(self, obj):
        colors = {
            'element': '#0d6efd',
            'reaction': '#fd7e14',
            'quiz': '#20c997',
            'progress': '#6f42c1',
            'social': '#e83e8c',
        }
        color = colors.get(obj.achievement.achievement_type, '#6c757d')
        return format_html('{} <span style="background-color: {}; color: white; padding: 2px 5px; border-radius: 5px; font-size: 0.8em;">{}</span>', 
                          obj.achievement.name, color, dict(Achievement.ACHIEVEMENT_TYPES).get(obj.achievement.achievement_type, obj.achievement.achievement_type))
    achievement_with_type.short_description = _("Достижение")

# Админка для прогресса обучения
@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'element', 'progress_bar', 'is_learned', 'last_interaction')
    list_filter = ('is_learned', 'last_interaction')
    search_fields = ('user__username', 'element__name')
    date_hierarchy = 'last_interaction'
    autocomplete_fields = ['user', 'element']
    list_select_related = ('user', 'element')
    
    def progress_bar(self, obj):
        color = '#dc3545' if obj.progress_percent < 30 else '#fd7e14' if obj.progress_percent < 70 else '#28a745'
        return format_html(
            '<div style="width: 100px; background-color: #f8f9fa; border-radius: 5px; height: 15px;">'
            '<div style="width: {}%; background-color: {}; border-radius: 5px; height: 15px;"></div>'
            '</div> <span style="font-size: 0.8em; color: #6c757d;">{:.0f}%</span>', 
            obj.progress_percent, color, obj.progress_percent
        )
    progress_bar.short_description = _("Прогресс")

# Админка для тестов
class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    autocomplete_fields = ['related_element']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'level_required', 'question_count', 'completion_count', 'is_active', 'created_at')
    list_filter = ('level', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuizQuestionInline]
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'description', 'level', 'is_active')
        }),
        (_('Метаданные'), {
            'fields': ('created_at',),
            'classes': ['collapse'],
        }),
    )
    readonly_fields = ('created_at',)
    
    def level_required(self, obj):
        return format_html('<span style="background-color: #6f42c1; color: white; padding: 3px 8px; border-radius: 10px;">Уровень {}</span>', obj.level)
    level_required.short_description = _("Требуемый уровень")
    
    def question_count(self, obj):
        count = obj.questions.count()
        return format_html('<span style="color: #0d6efd; font-weight: bold;">{}</span>', count)
    question_count.short_description = _("Вопросов")
    
    def completion_count(self, obj):
        count = UserQuizResult.objects.filter(quiz=obj).count()
        return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', count)
    completion_count.short_description = _("Прохождений")
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _question_count=Count('questions', distinct=True),
            _completion_count=Count('userquizresult', distinct=True)
        )
        return queryset

# Админка для вопросов тестов
class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 2
    fields = ('text', 'is_correct')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz_link', 'points', 'related_element')
    list_filter = ('quiz', 'points')
    search_fields = ('question_text',)
    inlines = [QuizAnswerInline]
    autocomplete_fields = ['related_element']
    
    def quiz_link(self, obj):
        link = reverse("admin:accounts_quiz_change", args=[obj.quiz.id])
        return format_html('<a href="{}">{}</a>', link, obj.quiz.title)
    quiz_link.short_description = _("Викторина")

# Админка для результатов тестов
@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score_display', 'percent_score', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
    date_hierarchy = 'completed_at'
    autocomplete_fields = ['user', 'quiz']
    list_select_related = ('user', 'quiz')
    
    def score_display(self, obj):
        return format_html('{} / {}', obj.score, obj.max_score)
    score_display.short_description = _("Баллы")
    
    def percent_score(self, obj):
        if obj.max_score > 0:
            percent = int((obj.score / obj.max_score) * 100)
            color = '#dc3545' if percent < 50 else '#fd7e14' if percent < 80 else '#28a745'
            return format_html(
                '<div style="width: 100px; background-color: #f8f9fa; border-radius: 5px; height: 15px;">'
                '<div style="width: {}%; background-color: {}; border-radius: 5px; height: 15px;"></div>'
                '</div> <span style="font-size: 0.8em; color: #6c757d;">{}%</span>', 
                percent, color, percent
            )
        return format_html('<span style="color: #dc3545;">0%</span>')
    percent_score.short_description = _("Процент")

# Регистрация моделей в админ-панели
admin.site.register(User, CustomUserAdmin)
