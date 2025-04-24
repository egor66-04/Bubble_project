from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ElementCategory(models.Model):
    """Категория химического элемента (металл, неметалл и т.д.)"""
    name = models.CharField(_('Название'), max_length=100)
    description = models.TextField(_('Описание'), blank=True)
    color = models.CharField(_('Цвет (HEX)'), max_length=7, help_text="#RRGGBB", default="#FFFFFF")
    
    class Meta:
        verbose_name = _('Категория элемента')
        verbose_name_plural = _('Категории элементов')
    
    def __str__(self):
        return self.name

class Element(models.Model):
    """Химический элемент"""
    STATE_CHOICES = [
        ('solid', _('Твёрдое')),
        ('liquid', _('Жидкое')),
        ('gas', _('Газообразное')),
    ]
    
    name = models.CharField(_('Название'), max_length=100)
    symbol = models.CharField(_('Символ'), max_length=3)
    atomic_number = models.PositiveSmallIntegerField(_('Атомный номер'), unique=True)
    atomic_weight = models.FloatField(_('Атомная масса'))
    group = models.PositiveSmallIntegerField(_('Группа'), null=True, blank=True)
    period = models.PositiveSmallIntegerField(_('Период'))
    category = models.ForeignKey(ElementCategory, on_delete=models.CASCADE, 
                                 related_name='elements', verbose_name=_('Категория'))
    state = models.CharField(_('Агрегатное состояние'), max_length=10, choices=STATE_CHOICES, default='solid')
    image = models.ImageField(_('Изображение'), upload_to='elements/', blank=True, null=True)
    description = models.TextField(_('Описание'), blank=True)
    fun_facts = models.TextField(_('Интересные факты'), blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Химический элемент')
        verbose_name_plural = _('Химические элементы')
        ordering = ['atomic_number']
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"

class ChemicalReaction(models.Model):
    """Химическая реакция между элементами"""
    name = models.CharField(_('Название'), max_length=200)
    reactants = models.ManyToManyField(Element, related_name='reactions_as_reactant', 
                                        verbose_name=_('Реагенты'))
    products = models.ManyToManyField(Element, related_name='reactions_as_product', 
                                      verbose_name=_('Продукты'))
    reaction_formula = models.CharField(_('Формула реакции'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    video = models.FileField(_('Видео реакции'), upload_to='reaction_videos/', blank=True, null=True)
    image = models.ImageField(_('Изображение'), upload_to='reaction_images/', blank=True, null=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    
    class Meta:
        verbose_name = _('Химическая реакция')
        verbose_name_plural = _('Химические реакции')
    
    def __str__(self):
        return self.name

class ElementDetail(models.Model):
    """Дополнительные детали о химическом элементе"""
    element = models.OneToOneField(Element, on_delete=models.CASCADE, 
                                  related_name='details', verbose_name=_('Элемент'))
    melting_point = models.FloatField(_('Температура плавления (°C)'), null=True, blank=True)
    boiling_point = models.FloatField(_('Температура кипения (°C)'), null=True, blank=True)
    electron_configuration = models.CharField(_('Электронная конфигурация'), max_length=100, blank=True)
    electronegativity = models.FloatField(_('Электроотрицательность'), null=True, blank=True)
    discovery_year = models.PositiveSmallIntegerField(_('Год открытия'), null=True, blank=True)
    discovered_by = models.CharField(_('Кем открыт'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Детали элемента')
        verbose_name_plural = _('Детали элементов')
    
    def __str__(self):
        return f"Детали для {self.element}"
