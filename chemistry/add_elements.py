"""
Скрипт для добавления базовых химических элементов в таблицу Менделеева
"""
import os
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bubble.settings")
django.setup()

from chemistry.models import Element, ElementCategory, ElementDetail, ChemicalReaction

def create_element_categories():
    """
    Создание категорий химических элементов
    """
    categories = [
        {
            'name': 'Щелочные металлы',
            'description': 'Мягкие, легкие металлы, которые очень активны химически.',
            'color': '#FF5733'
        },
        {
            'name': 'Щелочноземельные металлы',
            'description': 'Твердые металлы, менее реактивные, чем щелочные металлы.',
            'color': '#FFC300'
        },
        {
            'name': 'Переходные металлы',
            'description': 'Твердые, блестящие металлы с высокой температурой плавления.',
            'color': '#C70039'
        },
        {
            'name': 'Неметаллы',
            'description': 'Элементы с низкой теплопроводностью и плохой электрической проводимостью.',
            'color': '#33FF57'
        },
        {
            'name': 'Галогены',
            'description': 'Высоко реактивные неметаллы.',
            'color': '#00BFFF'
        },
        {
            'name': 'Благородные газы',
            'description': 'Химически инертные элементы с очень низкой реактивностью.',
            'color': '#9370DB'
        }
    ]

    created_categories = {}
    
    for category_data in categories:
        category, created = ElementCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data['description'],
                'color': category_data['color']
            }
        )
        created_categories[category_data['name']] = category
        if created:
            print(f"Создана категория: {category.name}")
        else:
            print(f"Категория уже существует: {category.name}")
    
    return created_categories

def create_elements(categories):
    """
    Создание химических элементов
    """
    elements = [
        # Водород
        {
            'name': 'Водород',
            'symbol': 'H',
            'atomic_number': 1,
            'atomic_weight': 1.008,
            'group': 1,
            'period': 1,
            'category': categories['Неметаллы'],
            'description': 'Водород — самый легкий и распространенный элемент во Вселенной. При нормальных условиях представляет собой бесцветный газ без запаха и вкуса.',
            'fun_facts': '- Водород — самый легкий элемент во Вселенной.\n- Составляет 75% массы Солнца и звезд.\n- Может использоваться как чистое топливо, при сгорании образует только воду.',
            'details': {
                'melting_point': -259.16,
                'boiling_point': -252.87,
                'electron_configuration': '1s¹',
                'electronegativity': 2.2,
                'discovery_year': 1766,
                'discovered_by': 'Генри Кавендиш'
            }
        },
        # Гелий
        {
            'name': 'Гелий',
            'symbol': 'He',
            'atomic_number': 2,
            'atomic_weight': 4.0026,
            'group': 18,
            'period': 1,
            'category': categories['Благородные газы'],
            'description': 'Гелий — второй по распространенности элемент во Вселенной после водорода. Это инертный газ без цвета, запаха и вкуса.',
            'fun_facts': '- Гелий был обнаружен на Солнце раньше, чем на Земле.\n- Единственный элемент, который не может быть затвердевшим при атмосферном давлении.\n- Используется для наполнения воздушных шаров и дирижаблей.',
            'details': {
                'melting_point': -272.2,
                'boiling_point': -268.9,
                'electron_configuration': '1s²',
                'electronegativity': None,
                'discovery_year': 1868,
                'discovered_by': 'Пьер Жансен и Джозеф Норман Локьер'
            }
        },
        # Литий
        {
            'name': 'Литий',
            'symbol': 'Li',
            'atomic_number': 3,
            'atomic_weight': 6.94,
            'group': 1,
            'period': 2,
            'category': categories['Щелочные металлы'],
            'description': 'Литий — самый легкий металл. Он мягкий, серебристо-белого цвета, легко окисляется на воздухе.',
            'fun_facts': '- Литий — самый легкий металл и самый легкий твердый элемент.\n- Используется в литий-ионных аккумуляторах.\n- Применяется в медицине для лечения биполярного расстройства.',
            'details': {
                'melting_point': 180.5,
                'boiling_point': 1342,
                'electron_configuration': '1s² 2s¹',
                'electronegativity': 0.98,
                'discovery_year': 1817,
                'discovered_by': 'Йохан Август Арфведсон'
            }
        },
        # Кислород
        {
            'name': 'Кислород',
            'symbol': 'O',
            'atomic_number': 8,
            'atomic_weight': 15.999,
            'group': 16,
            'period': 2,
            'category': categories['Неметаллы'],
            'description': 'Кислород — активный неметалл, необходимый для дыхания большинства живых организмов на Земле.',
            'fun_facts': '- Кислород составляет около 21% атмосферы Земли.\n- Свободный кислород впервые появился в атмосфере Земли около 2.5 миллиардов лет назад.\n- Без кислорода большинство живых организмов не могут существовать дольше нескольких минут.',
            'details': {
                'melting_point': -218.79,
                'boiling_point': -182.95,
                'electron_configuration': '1s² 2s² 2p⁴',
                'electronegativity': 3.44,
                'discovery_year': 1774,
                'discovered_by': 'Джозеф Пристли и Карл Вильгельм Шееле'
            }
        },
        # Углерод
        {
            'name': 'Углерод',
            'symbol': 'C',
            'atomic_number': 6,
            'atomic_weight': 12.011,
            'group': 14,
            'period': 2,
            'category': categories['Неметаллы'],
            'description': 'Углерод — основа всей органической химии и жизни на Земле. Существует в различных формах, включая алмаз и графит.',
            'fun_facts': '- Углерод содержится во всех живых организмах.\n- Может образовывать около 10 миллионов различных соединений.\n- Алмаз и графит — две аллотропные формы углерода с совершенно разными свойствами.',
            'details': {
                'melting_point': 3550,
                'boiling_point': 4027,
                'electron_configuration': '1s² 2s² 2p²',
                'electronegativity': 2.55,
                'discovery_year': None,  # Известен с древних времен
                'discovered_by': 'Известен с древности'
            }
        },
        # Натрий
        {
            'name': 'Натрий',
            'symbol': 'Na',
            'atomic_number': 11,
            'atomic_weight': 22.9897,
            'group': 1,
            'period': 3,
            'category': categories['Щелочные металлы'],
            'description': 'Натрий — мягкий, серебристо-белый металл, который быстро окисляется на воздухе и бурно реагирует с водой.',
            'fun_facts': '- Натрий должен храниться под маслом, так как быстро реагирует с воздухом.\n- Образует яркое желтое пламя при горении.\n- Натрий является важным элементом для нервной системы человека.',
            'details': {
                'melting_point': 97.72,
                'boiling_point': 883,
                'electron_configuration': '1s² 2s² 2p⁶ 3s¹',
                'electronegativity': 0.93,
                'discovery_year': 1807,
                'discovered_by': 'Гемфри Дэви'
            }
        },
        # Хлор
        {
            'name': 'Хлор',
            'symbol': 'Cl',
            'atomic_number': 17,
            'atomic_weight': 35.453,
            'group': 17,
            'period': 3,
            'category': categories['Галогены'],
            'description': 'Хлор — ядовитый желто-зеленый газ с резким запахом. Сильный окислитель.',
            'fun_facts': '- Хлор использовался как химическое оружие в Первой мировой войне.\n- Является одним из наиболее распространенных элементов в земной коре.\n- Необходим для дезинфекции питьевой воды и бассейнов.',
            'details': {
                'melting_point': -101.5,
                'boiling_point': -34.04,
                'electron_configuration': '1s² 2s² 2p⁶ 3s² 3p⁵',
                'electronegativity': 3.16,
                'discovery_year': 1774,
                'discovered_by': 'Карл Вильгельм Шееле'
            }
        },
        # Железо
        {
            'name': 'Железо',
            'symbol': 'Fe',
            'atomic_number': 26,
            'atomic_weight': 55.845,
            'group': 8,
            'period': 4,
            'category': categories['Переходные металлы'],
            'description': 'Железо — наиболее распространенный металл на Земле и четвертый по распространенности элемент в земной коре.',
            'fun_facts': '- Железо является основным компонентом ядра Земли.\n- Ржавчина — это оксид железа, образующийся при контакте с кислородом и водой.\n- Железо необходимо для образования гемоглобина в крови.',
            'details': {
                'melting_point': 1538,
                'boiling_point': 2862,
                'electron_configuration': '1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶',
                'electronegativity': 1.83,
                'discovery_year': None,  # Известен с древних времен
                'discovered_by': 'Известен с древности'
            }
        },
        # Золото
        {
            'name': 'Золото',
            'symbol': 'Au',
            'atomic_number': 79,
            'atomic_weight': 196.967,
            'group': 11,
            'period': 6,
            'category': categories['Переходные металлы'],
            'description': 'Золото — благородный металл желтого цвета. Устойчив к коррозии и большинству кислот.',
            'fun_facts': '- Золото настолько ковкое, что из 1 грамма можно вытянуть проволоку длиной 2 километра.\n- Все золото, когда-либо добытое, может поместиться в куб со стороной около 21 метра.\n- Используется не только в ювелирном деле, но и в электронике и медицине.',
            'details': {
                'melting_point': 1064.18,
                'boiling_point': 2856,
                'electron_configuration': '1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s² 4d¹⁰ 5p⁶ 6s¹ 4f¹⁴ 5d¹⁰',
                'electronegativity': 2.54,
                'discovery_year': None,  # Известен с древних времен
                'discovered_by': 'Известен с древности'
            }
        },
        # Серебро
        {
            'name': 'Серебро',
            'symbol': 'Ag',
            'atomic_number': 47,
            'atomic_weight': 107.868,
            'group': 11,
            'period': 5,
            'category': categories['Переходные металлы'],
            'description': 'Серебро — блестящий, мягкий, ковкий металл с наивысшей электропроводностью среди всех элементов.',
            'fun_facts': '- Серебро обладает самой высокой электропроводностью из всех металлов.\n- Имеет антибактериальные свойства и использовалось для хранения воды еще в древности.\n- Сплав серебра 925 пробы (стерлинговое серебро) наиболее часто используется в ювелирном деле.',
            'details': {
                'melting_point': 961.78,
                'boiling_point': 2162,
                'electron_configuration': '1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s¹ 4d¹⁰',
                'electronegativity': 1.93,
                'discovery_year': None,  # Известен с древних времен
                'discovered_by': 'Известен с древности'
            }
        }
    ]

    for element_data in elements:
        # Проверяем, существует ли элемент
        element, created = Element.objects.get_or_create(
            atomic_number=element_data['atomic_number'],
            defaults={
                'name': element_data['name'],
                'symbol': element_data['symbol'],
                'atomic_weight': element_data['atomic_weight'],
                'group': element_data['group'],
                'period': element_data['period'],
                'category': element_data['category'],
                'description': element_data['description'],
                'fun_facts': element_data['fun_facts']
            }
        )
        
        if created:
            print(f"Создан элемент: {element.name} ({element.symbol})")
        else:
            print(f"Элемент уже существует: {element.name} ({element.symbol})")
        
        # Добавляем детали для элемента, если они есть
        details_data = element_data.get('details')
        if details_data:
            element_detail, detail_created = ElementDetail.objects.get_or_create(
                element=element,
                defaults=details_data
            )
            
            if detail_created:
                print(f"Добавлены детали для элемента: {element.name}")
            else:
                print(f"Детали для элемента {element.name} уже существуют")

def create_reactions():
    """
    Создание химических реакций между элементами
    """
    # Получаем элементы из базы данных
    try:
        hydrogen = Element.objects.get(symbol='H')
        oxygen = Element.objects.get(symbol='O')
        sodium = Element.objects.get(symbol='Na')
        chlorine = Element.objects.get(symbol='Cl')
        carbon = Element.objects.get(symbol='C')
    except Element.DoesNotExist:
        print("Не найдены все необходимые элементы для создания реакций")
        return

    # Реакции
    reactions = [
        {
            'name': 'Образование воды',
            'reaction_formula': '2H₂ + O₂ → 2H₂O',
            'description': 'При соединении водорода и кислорода образуется вода. Эта реакция экзотермическая и выделяет большое количество тепла.',
            'reactants': [hydrogen, oxygen],
            'products': [hydrogen, oxygen]  # Вода (H2O) не является элементом, но для демонстрации используем H и O
        },
        {
            'name': 'Образование поваренной соли',
            'reaction_formula': '2Na + Cl₂ → 2NaCl',
            'description': 'При взаимодействии натрия и хлора образуется хлорид натрия (поваренная соль). Реакция протекает очень бурно.',
            'reactants': [sodium, chlorine],
            'products': [sodium, chlorine]
        },
        {
            'name': 'Горение углерода',
            'reaction_formula': 'C + O₂ → CO₂',
            'description': 'При сгорании углерода в кислороде образуется углекислый газ. Эта реакция лежит в основе многих процессов горения.',
            'reactants': [carbon, oxygen],
            'products': [carbon, oxygen]
        }
    ]

    for reaction_data in reactions:
        # Создаем реакцию
        reaction, created = ChemicalReaction.objects.get_or_create(
            name=reaction_data['name'],
            defaults={
                'reaction_formula': reaction_data['reaction_formula'],
                'description': reaction_data['description']
            }
        )
        
        if created:
            print(f"Создана реакция: {reaction.name}")
        else:
            print(f"Реакция уже существует: {reaction.name}")
            continue  # Пропускаем дальнейшие действия, если реакция уже существует
        
        # Добавляем реагенты и продукты
        for reactant in reaction_data['reactants']:
            reaction.reactants.add(reactant)
        
        for product in reaction_data['products']:
            reaction.products.add(product)
        
        print(f"Добавлены реагенты и продукты для реакции: {reaction.name}")

if __name__ == "__main__":
    print("Добавление химических элементов в базу данных...")
    categories = create_element_categories()
    create_elements(categories)
    create_reactions()
    print("Готово!") 