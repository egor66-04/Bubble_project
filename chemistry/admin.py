from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import ElementCategory, Element, ChemicalReaction, ElementDetail

class ElementDetailInline(admin.StackedInline):
    model = ElementDetail
    can_delete = False
    verbose_name = _("Детали элемента")
    verbose_name_plural = _("Детали элемента")
    classes = ['collapse']
    extra = 0
    fieldsets = (
        (_('Физические свойства'), {
            'fields': ('melting_point', 'boiling_point', 'density', 'thermal_conductivity', 'electronegativity'),
            'classes': ['collapse', 'wide'],
        }),
        (_('Электронная конфигурация'), {
            'fields': ('electron_configuration', 'electron_shell_image'),
            'classes': ['collapse', 'wide'],
        }),
        (_('История и описание'), {
            'fields': ('description', 'discovery_year', 'discovered_by', 'discovery_info'),
            'classes': ['collapse', 'wide'],
        }),
        (_('Применение'), {
            'fields': ('applications', 'fun_facts'),
            'classes': ['collapse', 'wide'],
        }),
    )

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('element_image', 'symbol', 'name', 'atomic_number', 'category', 'state_display', 'is_active')
    list_filter = ('category', 'is_active', 'period', 'group', 'state')
    search_fields = ('name', 'symbol', 'atomic_number')
    ordering = ('atomic_number',)
    list_display_links = ('element_image', 'symbol', 'name')
    list_per_page = 20
    actions = ['mark_as_active', 'mark_as_inactive']
    save_on_top = True
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (('name', 'symbol', 'atomic_number'), ('atomic_weight', 'category', 'is_active'))
        }),
        (_('Положение в таблице'), {
            'fields': (('period', 'group'), 'state'),
            'classes': ['collapse', 'wide'],
        }),
        (_('Медиа'), {
            'fields': ('image',),
            'classes': ['wide'],
        }),
        (_('Описание'), {
            'fields': ('description',),
            'classes': ['collapse', 'wide'],
        }),
    )
    inlines = [ElementDetailInline]
    
    def element_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; border: 2px solid {};" />', 
                              obj.image.url, obj.category.color if obj.category else '#ccc')
        return format_html('<div style="width: 50px; height: 50px; background-color: {}; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><span style="color: white; font-weight: bold;">{}</span></div>', 
                          obj.category.color if obj.category else '#ccc', obj.symbol)
    element_image.short_description = _("Изображение")
    
    def state_display(self, obj):
        states = {
            'solid': _('Твёрдое'),
            'liquid': _('Жидкое'),
            'gas': _('Газообразное')
        }
        colors = {
            'solid': '#6c757d',
            'liquid': '#0d6efd',
            'gas': '#20c997'
        }
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px;">{}</span>', 
                          colors.get(obj.state, '#6c757d'), states.get(obj.state, _('Неизвестно')))
    state_display.short_description = _("Агрегатное состояние")
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = _("Отметить как активные")
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = _("Отметить как неактивные")
    
    class Media:
        css = {
            'all': ('css/admin/element_admin.css',)
        }
        js = ('js/admin/element_admin.js',)

@admin.register(ElementCategory)
class ElementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_display', 'color')
    search_fields = ('name',)
    
    def color_display(self, obj):
        return format_html('<div style="background-color: {}; width: 100px; height: 20px; border-radius: 3px;"></div>', obj.color)
    color_display.short_description = _("Цвет")

class ChemicalReactionElementsInline(admin.TabularInline):
    model = ChemicalReaction.reactants.through
    verbose_name = _("Реагент")
    verbose_name_plural = _("Реагенты")
    extra = 1
    autocomplete_fields = ['element']

class ChemicalReactionProductsInline(admin.TabularInline):
    model = ChemicalReaction.products.through
    verbose_name = _("Продукт")
    verbose_name_plural = _("Продукты")
    extra = 1
    autocomplete_fields = ['element']

@admin.register(ChemicalReaction)
class ChemicalReactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'reaction_formula', 'get_reactants', 'get_products', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'reaction_formula')
    filter_horizontal = ('reactants', 'products')
    exclude = ('reactants', 'products')
    inlines = [ChemicalReactionElementsInline, ChemicalReactionProductsInline]
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'reaction_formula', 'is_active')
        }),
        (_('Описание'), {
            'fields': ('description',),
            'classes': ['collapse', 'wide'],
        }),
        (_('Медиа'), {
            'fields': ('video', 'image'),
            'classes': ['wide'],
        }),
    )
    
    def get_reactants(self, obj):
        return ", ".join([element.symbol for element in obj.reactants.all()])
    get_reactants.short_description = _("Реагенты")
    
    def get_products(self, obj):
        return ", ".join([element.symbol for element in obj.products.all()])
    get_products.short_description = _("Продукты")
    
    class Media:
        css = {
            'all': ('css/admin/reaction_admin.css',)
        }
        js = ('js/admin/reaction_admin.js',)
