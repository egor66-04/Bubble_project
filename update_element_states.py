"""
Скрипт для обновления агрегатного состояния химических элементов
"""
import os
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bubble.settings")
django.setup()

from chemistry.models import Element

def update_element_states():
    """
    Обновляет агрегатные состояния элементов
    """
    # Словарь с элементами и их состояниями
    element_states = {
        'H': 'gas',     # Водород
        'He': 'gas',    # Гелий
        'Li': 'solid',  # Литий
        'O': 'gas',     # Кислород
        'C': 'solid',   # Углерод
        'Na': 'solid',  # Натрий
        'Cl': 'gas',    # Хлор
        'Fe': 'solid',  # Железо
        'Au': 'solid',  # Золото
        'Ag': 'solid',  # Серебро
    }
    
    # Обновляем состояния элементов
    for symbol, state in element_states.items():
        try:
            element = Element.objects.get(symbol=symbol)
            element.state = state
            element.save()
            print(f"Обновлено состояние для {element.name} ({element.symbol}): {state}")
        except Element.DoesNotExist:
            print(f"Элемент с символом {symbol} не найден")

if __name__ == "__main__":
    print("Обновление агрегатного состояния элементов...")
    update_element_states()
    print("Готово!") 