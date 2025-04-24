"""
Скрипт для инициализации базовых данных
"""
import os
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bubble.settings")
django.setup()

from chemistry.models import Element, ElementCategory

def create_categories():
    """Создает базовые категории элементов"""
    categories = [
        {
            'name': 'Металлы',
            'description': 'Элементы с металлическими свойствами',
            'color': '#C0C0C0',
        },
        {
            'name': 'Неметаллы',
            'description': 'Элементы с неметаллическими свойствами',
            'color': '#A0FFA0',
        },
        {
            'name': 'Благородные газы',
            'description': 'Инертные газы с заполненными электронными оболочками',
            'color': '#A0A0FF',
        },
    ]
    
    created = {}
    for cat_data in categories:
        category, _ = ElementCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
            }
        )
        created[cat_data['name']] = category
        print(f"Категория: {category.name}")
    
    return created

def create_elements(categories):
    """Создает базовые химические элементы"""
    elements = [
        {
            'name': 'Водород',
            'symbol': 'H',
            'atomic_number': 1,
            'atomic_weight': 1.008,
            'group': 1,
            'period': 1,
            'category': categories['Неметаллы'],
            'state': 'gas',
            'description': 'Водород - самый легкий и распространенный элемент во вселенной.',
        },
        {
            'name': 'Гелий',
            'symbol': 'He',
            'atomic_number': 2,
            'atomic_weight': 4.0026,
            'group': 18,
            'period': 1,
            'category': categories['Благородные газы'],
            'state': 'gas',
            'description': 'Гелий - второй по распространенности элемент во вселенной после водорода.',
        },
        {
            'name': 'Углерод',
            'symbol': 'C',
            'atomic_number': 6,
            'atomic_weight': 12.011,
            'group': 14,
            'period': 2,
            'category': categories['Неметаллы'],
            'state': 'solid',
            'description': 'Углерод - основа всей органической химии и жизни на Земле.',
        },
        {
            'name': 'Кислород',
            'symbol': 'O',
            'atomic_number': 8,
            'atomic_weight': 15.999,
            'group': 16,
            'period': 2,
            'category': categories['Неметаллы'],
            'state': 'gas',
            'description': 'Кислород необходим для дыхания большинства живых организмов.',
        },
        {
            'name': 'Натрий',
            'symbol': 'Na',
            'atomic_number': 11,
            'atomic_weight': 22.9897,
            'group': 1,
            'period': 3,
            'category': categories['Металлы'],
            'state': 'solid',
            'description': 'Натрий - мягкий, серебристо-белый металл, который активно реагирует с водой.',
        },
        {
            'name': 'Железо',
            'symbol': 'Fe',
            'atomic_number': 26,
            'atomic_weight': 55.845,
            'group': 8,
            'period': 4,
            'category': categories['Металлы'],
            'state': 'solid',
            'description': 'Железо - один из самых распространенных элементов на Земле и важный материал для промышленности.',
        },
    ]
    
    for elem_data in elements:
        element, created = Element.objects.get_or_create(
            atomic_number=elem_data['atomic_number'],
            defaults={
                'name': elem_data['name'],
                'symbol': elem_data['symbol'],
                'atomic_weight': elem_data['atomic_weight'],
                'group': elem_data['group'],
                'period': elem_data['period'],
                'category': elem_data['category'],
                'state': elem_data['state'],
                'description': elem_data['description'],
            }
        )
        action = "Создан" if created else "Существует"
        print(f"{action} элемент: {element.name} ({element.symbol})")

if __name__ == "__main__":
    print("Инициализация базовых данных...")
    categories = create_categories()
    create_elements(categories)
    print("Готово!") 