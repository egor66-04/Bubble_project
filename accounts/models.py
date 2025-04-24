from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from chemistry.models import Element, ChemicalReaction

class User(AbstractUser):
    """Расширенная модель пользователя"""
    email = models.EmailField(_('Email адрес'), unique=True)
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('О себе'), blank=True)
    birth_date = models.DateField(_('Дата рождения'), blank=True, null=True)
    xp_points = models.PositiveIntegerField(_('Очки опыта'), default=0)
    level = models.PositiveSmallIntegerField(_('Уровень'), default=1)
    is_subscribed = models.BooleanField(_('Подписка'), default=False)
    subscription_end_date = models.DateTimeField(_('Дата окончания подписки'), blank=True, null=True)
    favorite_elements = models.ManyToManyField(
        Element,
        through='UserFavoriteElement',
        related_name='favorited_by',
        verbose_name=_('Избранные элементы')
    )
    favorite_reactions = models.ManyToManyField(
        ChemicalReaction,
        through='UserFavoriteReaction',
        related_name='favorited_by',
        verbose_name=_('Избранные реакции')
    )
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
    
    def __str__(self):
        return self.username

class UserFavoriteElement(models.Model):
    """Связь между пользователем и избранными элементами"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    element = models.ForeignKey(Element, on_delete=models.CASCADE, verbose_name=_('Элемент'))
    added_at = models.DateTimeField(_('Дата добавления'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Избранный элемент')
        verbose_name_plural = _('Избранные элементы')
        unique_together = ('user', 'element')
    
    def __str__(self):
        return f"{self.user.username} - {self.element.symbol}"

class UserFavoriteReaction(models.Model):
    """Связь между пользователем и избранными реакциями"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    reaction = models.ForeignKey(ChemicalReaction, on_delete=models.CASCADE, verbose_name=_('Реакция'))
    added_at = models.DateTimeField(_('Дата добавления'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Избранная реакция')
        verbose_name_plural = _('Избранные реакции')
        unique_together = ('user', 'reaction')
    
    def __str__(self):
        return f"{self.user.username} - {self.reaction.name}"

class Achievement(models.Model):
    """Модель достижений"""
    ACHIEVEMENT_TYPES = (
        ('first_action', _('Первое действие')),
        ('first_element', _('Первый элемент')),
        ('first_quiz', _('Первая викторина')),
        ('three_correct_answers', _('Три правильных ответа подряд')),
        ('first_search', _('Первый поиск')),
        ('custom', _('Другое достижение')),
    )
    
    name = models.CharField(_('Название'), max_length=100)
    description = models.TextField(_('Описание'))
    image = models.ImageField(_('Значок'), upload_to='achievements/', blank=True, null=True)
    xp_reward = models.PositiveIntegerField(_('Награда XP'), default=0)
    required_elements = models.ManyToManyField(
        Element,
        related_name='achievements',
        verbose_name=_('Необходимые элементы'),
        blank=True
    )
    required_level = models.PositiveSmallIntegerField(_('Необходимый уровень'), default=1)
    achievement_type = models.CharField(
        _('Тип достижения'), 
        max_length=50, 
        choices=ACHIEVEMENT_TYPES,
        default='custom'
    )
    icon = models.CharField(_('Иконка'), max_length=50, default='fas fa-award')
    emoji = models.CharField(_('Эмодзи'), max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Достижение')
        verbose_name_plural = _('Достижения')
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """Связь между пользователем и полученными достижениями"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements', 
                             verbose_name=_('Пользователь'))
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, 
                                   verbose_name=_('Достижение'))
    achieved_at = models.DateTimeField(_('Дата получения'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Достижение пользователя')
        verbose_name_plural = _('Достижения пользователей')
        unique_together = ('user', 'achievement')
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class LearningProgress(models.Model):
    """Прогресс обучения пользователя по элементам"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress',
                             verbose_name=_('Пользователь'))
    element = models.ForeignKey(Element, on_delete=models.CASCADE, 
                               verbose_name=_('Элемент'))
    is_learned = models.BooleanField(_('Изучен'), default=False)
    progress_percent = models.PositiveSmallIntegerField(_('Процент изучения'), default=0)
    last_interaction = models.DateTimeField(_('Последнее взаимодействие'), auto_now=True)
    
    class Meta:
        verbose_name = _('Прогресс обучения')
        verbose_name_plural = _('Прогресс обучения')
        unique_together = ('user', 'element')
    
    def __str__(self):
        return f"{self.user.username} - {self.element.symbol} ({self.progress_percent}%)"

class Quiz(models.Model):
    """Тест по химическим элементам"""
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'), blank=True)
    level = models.PositiveSmallIntegerField(_('Уровень сложности'), default=1)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    max_points = models.PositiveIntegerField(_('Максимальное количество очков'), default=10)
    time_limit = models.PositiveIntegerField(_('Ограничение по времени (мин)'), default=10)
    
    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')
    
    def __str__(self):
        return f"{self.title} (Уровень {self.level})"

class QuizQuestion(models.Model):
    """Вопрос в тесте"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions',
                            verbose_name=_('Тест'))
    question_text = models.TextField(_('Текст вопроса'))
    related_element = models.ForeignKey(Element, on_delete=models.SET_NULL, 
                                       null=True, blank=True, verbose_name=_('Связанный элемент'))
    points = models.PositiveSmallIntegerField(_('Очки за правильный ответ'), default=1)
    
    class Meta:
        verbose_name = _('Вопрос теста')
        verbose_name_plural = _('Вопросы тестов')
    
    def __str__(self):
        return f"Вопрос {self.id} - {self.quiz.title}"

class QuizAnswer(models.Model):
    """Вариант ответа на вопрос теста"""
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, 
                                related_name='answers', verbose_name=_('Вопрос'))
    answer_text = models.CharField(_('Текст ответа'), max_length=255)
    is_correct = models.BooleanField(_('Правильный ответ'), default=False)
    
    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответов')
    
    def __str__(self):
        return f"Ответ на вопрос {self.question.id} - {'Правильный' if self.is_correct else 'Неправильный'}"

class UserQuizResult(models.Model):
    """Результаты прохождения теста пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results',
                             verbose_name=_('Пользователь'))
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_('Тест'))
    score = models.PositiveIntegerField(_('Набранные очки'), default=0)
    max_score = models.PositiveIntegerField(_('Максимально возможные очки'), default=0)
    completed_at = models.DateTimeField(_('Дата прохождения'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Результат теста')
        verbose_name_plural = _('Результаты тестов')
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.max_score})"
