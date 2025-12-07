"""
Расширенный скрипт для заполнения базы данных химическими элементами, реакциями и викторинами
"""
import os
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bubble.settings")
django.setup()

from chemistry.models import Element, ElementCategory, ElementDetail, ChemicalReaction
from accounts.models import Achievement, Quiz, QuizQuestion, QuizAnswer

def create_extended_elements(categories):
    """
    Создание расширенного списка химических элементов (первые 30 элементов)
    """
    elements_data = [
        # Период 1
        {
            'name': 'Водород', 'symbol': 'H', 'atomic_number': 1, 'atomic_weight': 1.008,
            'group': 1, 'period': 1, 'category': categories['Неметаллы'], 'state': 'gas',
            'description': 'Водород — самый легкий и распространенный элемент во Вселенной.',
            'fun_facts': 'Водород составляет 75% массы всей видимой материи во Вселенной.',
            'details': {'melting_point': -259.16, 'boiling_point': -252.87, 'electron_configuration': '1s¹',
                       'electronegativity': 2.2, 'discovery_year': 1766, 'discovered_by': 'Генри Кавендиш'}
        },
        {
            'name': 'Гелий', 'symbol': 'He', 'atomic_number': 2, 'atomic_weight': 4.0026,
            'group': 18, 'period': 1, 'category': categories['Благородные газы'], 'state': 'gas',
            'description': 'Гелий — второй по распространенности элемент во Вселенной.',
            'fun_facts': 'Гелий был обнаружен на Солнце раньше, чем на Земле.',
            'details': {'melting_point': -272.2, 'boiling_point': -268.9, 'electron_configuration': '1s²',
                       'electronegativity': None, 'discovery_year': 1868, 'discovered_by': 'Пьер Жансен'}
        },
        
        # Период 2
        {
            'name': 'Литий', 'symbol': 'Li', 'atomic_number': 3, 'atomic_weight': 6.94,
            'group': 1, 'period': 2, 'category': categories['Щелочные металлы'], 'state': 'solid',
            'description': 'Литий — самый легкий металл.',
            'fun_facts': 'Используется в современных аккумуляторах для телефонов и электромобилей.',
            'details': {'melting_point': 180.5, 'boiling_point': 1342, 'electron_configuration': '1s² 2s¹',
                       'electronegativity': 0.98, 'discovery_year': 1817, 'discovered_by': 'Йохан Арфведсон'}
        },
        {
            'name': 'Бериллий', 'symbol': 'Be', 'atomic_number': 4, 'atomic_weight': 9.0122,
            'group': 2, 'period': 2, 'category': categories['Щелочноземельные металлы'], 'state': 'solid',
            'description': 'Бериллий — легкий, прочный металл.',
            'fun_facts': 'Используется в аэрокосмической промышленности из-за высокой прочности.',
            'details': {'melting_point': 1287, 'boiling_point': 2469, 'electron_configuration': '1s² 2s²',
                       'electronegativity': 1.57, 'discovery_year': 1798, 'discovered_by': 'Луи Воклен'}
        },
        {
            'name': 'Бор', 'symbol': 'B', 'atomic_number': 5, 'atomic_weight': 10.81,
            'group': 13, 'period': 2, 'category': categories['Неметаллы'], 'state': 'solid',
            'description': 'Бор — полуметалл, необходимый для роста растений.',
            'fun_facts': 'Бор используется в производстве боросиликатного стекла (термостойкого).',
            'details': {'melting_point': 2075, 'boiling_point': 4000, 'electron_configuration': '1s² 2s² 2p¹',
                       'electronegativity': 2.04, 'discovery_year': 1808, 'discovered_by': 'Жозеф Гей-Люссак'}
        },
        {
            'name': 'Углерод', 'symbol': 'C', 'atomic_number': 6, 'atomic_weight': 12.011,
            'group': 14, 'period': 2, 'category': categories['Неметаллы'], 'state': 'solid',
            'description': 'Углерод — основа всей органической химии и жизни.',
            'fun_facts': 'Алмаз и графит — две формы углерода с совершенно разными свойствами.',
            'details': {'melting_point': 3550, 'boiling_point': 4027, 'electron_configuration': '1s² 2s² 2p²',
                       'electronegativity': 2.55, 'discovery_year': None, 'discovered_by': 'Известен с древности'}
        },
        {
            'name': 'Азот', 'symbol': 'N', 'atomic_number': 7, 'atomic_weight': 14.007,
            'group': 15, 'period': 2, 'category': categories['Неметаллы'], 'state': 'gas',
            'description': 'Азот составляет 78% атмосферы Земли.',
            'fun_facts': 'Жидкий азот используется для быстрой заморозки и хранения биологических образцов.',
            'details': {'melting_point': -210, 'boiling_point': -195.8, 'electron_configuration': '1s² 2s² 2p³',
                       'electronegativity': 3.04, 'discovery_year': 1772, 'discovered_by': 'Даниель Резерфорд'}
        },
        {
            'name': 'Кислород', 'symbol': 'O', 'atomic_number': 8, 'atomic_weight': 15.999,
            'group': 16, 'period': 2, 'category': categories['Неметаллы'], 'state': 'gas',
            'description': 'Кислород необходим для дыхания большинства живых организмов.',
            'fun_facts': 'Без кислорода человек может прожить всего несколько минут.',
            'details': {'melting_point': -218.79, 'boiling_point': -182.95, 'electron_configuration': '1s² 2s² 2p⁴',
                       'electronegativity': 3.44, 'discovery_year': 1774, 'discovered_by': 'Джозеф Пристли'}
        },
        {
            'name': 'Фтор', 'symbol': 'F', 'atomic_number': 9, 'atomic_weight': 18.998,
            'group': 17, 'period': 2, 'category': categories['Галогены'], 'state': 'gas',
            'description': 'Фтор — самый активный неметалл.',
            'fun_facts': 'Фтор добавляют в зубную пасту для защиты от кариеса.',
            'details': {'melting_point': -219.67, 'boiling_point': -188.11, 'electron_configuration': '1s² 2s² 2p⁵',
                       'electronegativity': 3.98, 'discovery_year': 1886, 'discovered_by': 'Анри Муассан'}
        },
        {
            'name': 'Неон', 'symbol': 'Ne', 'atomic_number': 10, 'atomic_weight': 20.180,
            'group': 18, 'period': 2, 'category': categories['Благородные газы'], 'state': 'gas',
            'description': 'Неон — инертный газ, используемый в неоновых лампах.',
            'fun_facts': 'Неоновые вывески светятся красно-оранжевым светом.',
            'details': {'melting_point': -248.59, 'boiling_point': -246.05, 'electron_configuration': '1s² 2s² 2p⁶',
                       'electronegativity': None, 'discovery_year': 1898, 'discovered_by': 'Уильям Рамзай'}
        },
        
        # Период 3
        {
            'name': 'Натрий', 'symbol': 'Na', 'atomic_number': 11, 'atomic_weight': 22.990,
            'group': 1, 'period': 3, 'category': categories['Щелочные металлы'], 'state': 'solid',
            'description': 'Натрий — мягкий металл, активно реагирующий с водой.',
            'fun_facts': 'Хлорид натрия (NaCl) — это обычная поваренная соль.',
            'details': {'melting_point': 97.72, 'boiling_point': 883, 'electron_configuration': '[Ne] 3s¹',
                       'electronegativity': 0.93, 'discovery_year': 1807, 'discovered_by': 'Гемфри Дэви'}
        },
        {
            'name': 'Магний', 'symbol': 'Mg', 'atomic_number': 12, 'atomic_weight': 24.305,
            'group': 2, 'period': 3, 'category': categories['Щелочноземельные металлы'], 'state': 'solid',
            'description': 'Магний — легкий серебристый металл.',
            'fun_facts': 'Магний горит ярким белым пламенем и используется в фейерверках.',
            'details': {'melting_point': 650, 'boiling_point': 1090, 'electron_configuration': '[Ne] 3s²',
                       'electronegativity': 1.31, 'discovery_year': 1755, 'discovered_by': 'Джозеф Блэк'}
        },
        {
            'name': 'Алюминий', 'symbol': 'Al', 'atomic_number': 13, 'atomic_weight': 26.982,
            'group': 13, 'period': 3, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Алюминий — легкий, прочный металл.',
            'fun_facts': 'Самый распространенный металл в земной коре.',
            'details': {'melting_point': 660.32, 'boiling_point': 2519, 'electron_configuration': '[Ne] 3s² 3p¹',
                       'electronegativity': 1.61, 'discovery_year': 1825, 'discovered_by': 'Ганс Эрстед'}
        },
        {
            'name': 'Кремний', 'symbol': 'Si', 'atomic_number': 14, 'atomic_weight': 28.085,
            'group': 14, 'period': 3, 'category': categories['Неметаллы'], 'state': 'solid',
            'description': 'Кремний — основа компьютерных чипов.',
            'fun_facts': 'Второй по распространенности элемент в земной коре после кислорода.',
            'details': {'melting_point': 1414, 'boiling_point': 3265, 'electron_configuration': '[Ne] 3s² 3p²',
                       'electronegativity': 1.90, 'discovery_year': 1824, 'discovered_by': 'Йёнс Берцелиус'}
        },
        {
            'name': 'Фосфор', 'symbol': 'P', 'atomic_number': 15, 'atomic_weight': 30.974,
            'group': 15, 'period': 3, 'category': categories['Неметаллы'], 'state': 'solid',
            'description': 'Фосфор — необходим для всех живых организмов.',
            'fun_facts': 'Белый фосфор светится в темноте и самовоспламеняется на воздухе.',
            'details': {'melting_point': 44.15, 'boiling_point': 280.5, 'electron_configuration': '[Ne] 3s² 3p³',
                       'electronegativity': 2.19, 'discovery_year': 1669, 'discovered_by': 'Хенниг Бранд'}
        },
        {
            'name': 'Сера', 'symbol': 'S', 'atomic_number': 16, 'atomic_weight': 32.06,
            'group': 16, 'period': 3, 'category': categories['Неметаллы'], 'state': 'solid',
            'description': 'Сера — желтый неметалл с характерным запахом.',
            'fun_facts': 'Сера используется в производстве спичек и серной кислоты.',
            'details': {'melting_point': 115.21, 'boiling_point': 444.6, 'electron_configuration': '[Ne] 3s² 3p⁴',
                       'electronegativity': 2.58, 'discovery_year': None, 'discovered_by': 'Известна с древности'}
        },
        {
            'name': 'Хлор', 'symbol': 'Cl', 'atomic_number': 17, 'atomic_weight': 35.45,
            'group': 17, 'period': 3, 'category': categories['Галогены'], 'state': 'gas',
            'description': 'Хлор — ядовитый газ желто-зеленого цвета.',
            'fun_facts': 'Используется для дезинфекции воды в бассейнах и водопроводе.',
            'details': {'melting_point': -101.5, 'boiling_point': -34.04, 'electron_configuration': '[Ne] 3s² 3p⁵',
                       'electronegativity': 3.16, 'discovery_year': 1774, 'discovered_by': 'Карл Шееле'}
        },
        {
            'name': 'Аргон', 'symbol': 'Ar', 'atomic_number': 18, 'atomic_weight': 39.948,
            'group': 18, 'period': 3, 'category': categories['Благородные газы'], 'state': 'gas',
            'description': 'Аргон — инертный газ, третий по распространенности в атмосфере.',
            'fun_facts': 'Используется в лампах накаливания для предотвращения окисления нити.',
            'details': {'melting_point': -189.34, 'boiling_point': -185.85, 'electron_configuration': '[Ne] 3s² 3p⁶',
                       'electronegativity': None, 'discovery_year': 1894, 'discovered_by': 'Лорд Рэлей'}
        },
        
        # Период 4 (первые 12 элементов)
        {
            'name': 'Калий', 'symbol': 'K', 'atomic_number': 19, 'atomic_weight': 39.098,
            'group': 1, 'period': 4, 'category': categories['Щелочные металлы'], 'state': 'solid',
            'description': 'Калий — мягкий металл, необходимый для работы нервной системы.',
            'fun_facts': 'Калий настолько мягкий, что его можно резать ножом.',
            'details': {'melting_point': 63.5, 'boiling_point': 759, 'electron_configuration': '[Ar] 4s¹',
                       'electronegativity': 0.82, 'discovery_year': 1807, 'discovered_by': 'Гемфри Дэви'}
        },
        {
            'name': 'Кальций', 'symbol': 'Ca', 'atomic_number': 20, 'atomic_weight': 40.078,
            'group': 2, 'period': 4, 'category': categories['Щелочноземельные металлы'], 'state': 'solid',
            'description': 'Кальций — важнейший элемент для костей и зубов.',
            'fun_facts': '99% кальция в организме находится в костях и зубах.',
            'details': {'melting_point': 842, 'boiling_point': 1484, 'electron_configuration': '[Ar] 4s²',
                       'electronegativity': 1.00, 'discovery_year': 1808, 'discovered_by': 'Гемфри Дэви'}
        },
        {
            'name': 'Скандий', 'symbol': 'Sc', 'atomic_number': 21, 'atomic_weight': 44.956,
            'group': 3, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Скандий — редкий легкий металл.',
            'fun_facts': 'Используется в высокотехнологичных сплавах для аэрокосмической промышленности.',
            'details': {'melting_point': 1541, 'boiling_point': 2836, 'electron_configuration': '[Ar] 3d¹ 4s²',
                       'electronegativity': 1.36, 'discovery_year': 1879, 'discovered_by': 'Ларс Нильсон'}
        },
        {
            'name': 'Титан', 'symbol': 'Ti', 'atomic_number': 22, 'atomic_weight': 47.867,
            'group': 4, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Титан — прочный, легкий и устойчивый к коррозии металл.',
            'fun_facts': 'Используется в имплантатах благодаря биосовместимости.',
            'details': {'melting_point': 1668, 'boiling_point': 3287, 'electron_configuration': '[Ar] 3d² 4s²',
                       'electronegativity': 1.54, 'discovery_year': 1791, 'discovered_by': 'Уильям Грегор'}
        },
        {
            'name': 'Ванадий', 'symbol': 'V', 'atomic_number': 23, 'atomic_weight': 50.942,
            'group': 5, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Ванадий — твердый металл, используемый в сплавах.',
            'fun_facts': 'Добавка ванадия делает сталь более прочной и упругой.',
            'details': {'melting_point': 1910, 'boiling_point': 3407, 'electron_configuration': '[Ar] 3d³ 4s²',
                       'electronegativity': 1.63, 'discovery_year': 1801, 'discovered_by': 'Андрес дель Рио'}
        },
        {
            'name': 'Хром', 'symbol': 'Cr', 'atomic_number': 24, 'atomic_weight': 51.996,
            'group': 6, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Хром — твердый блестящий металл.',
            'fun_facts': 'Хромирование придает металлам блестящую защитную поверхность.',
            'details': {'melting_point': 1907, 'boiling_point': 2671, 'electron_configuration': '[Ar] 3d⁵ 4s¹',
                       'electronegativity': 1.66, 'discovery_year': 1797, 'discovered_by': 'Луи Воклен'}
        },
        {
            'name': 'Марганец', 'symbol': 'Mn', 'atomic_number': 25, 'atomic_weight': 54.938,
            'group': 7, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Марганец — важный элемент для производства стали.',
            'fun_facts': 'Марганец необходим для фотосинтеза в растениях.',
            'details': {'melting_point': 1246, 'boiling_point': 2061, 'electron_configuration': '[Ar] 3d⁵ 4s²',
                       'electronegativity': 1.55, 'discovery_year': 1774, 'discovered_by': 'Йохан Ган'}
        },
        {
            'name': 'Железо', 'symbol': 'Fe', 'atomic_number': 26, 'atomic_weight': 55.845,
            'group': 8, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Железо — основной компонент стали.',
            'fun_facts': 'Железо составляет основу земного ядра.',
            'details': {'melting_point': 1538, 'boiling_point': 2862, 'electron_configuration': '[Ar] 3d⁶ 4s²',
                       'electronegativity': 1.83, 'discovery_year': None, 'discovered_by': 'Известно с древности'}
        },
        {
            'name': 'Кобальт', 'symbol': 'Co', 'atomic_number': 27, 'atomic_weight': 58.933,
            'group': 9, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Кобальт — твердый магнитный металл.',
            'fun_facts': 'Используется в производстве аккумуляторов для электромобилей.',
            'details': {'melting_point': 1495, 'boiling_point': 2927, 'electron_configuration': '[Ar] 3d⁷ 4s²',
                       'electronegativity': 1.88, 'discovery_year': 1735, 'discovered_by': 'Георг Брандт'}
        },
        {
            'name': 'Никель', 'symbol': 'Ni', 'atomic_number': 28, 'atomic_weight': 58.693,
            'group': 10, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Никель — устойчивый к коррозии металл.',
            'fun_facts': 'Используется в монетах и нержавеющей стали.',
            'details': {'melting_point': 1455, 'boiling_point': 2913, 'electron_configuration': '[Ar] 3d⁸ 4s²',
                       'electronegativity': 1.91, 'discovery_year': 1751, 'discovered_by': 'Аксель Кронстедт'}
        },
        {
            'name': 'Медь', 'symbol': 'Cu', 'atomic_number': 29, 'atomic_weight': 63.546,
            'group': 11, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Медь — отличный проводник электричества.',
            'fun_facts': 'Медь была одним из первых металлов, освоенных человечеством.',
            'details': {'melting_point': 1084.62, 'boiling_point': 2562, 'electron_configuration': '[Ar] 3d¹⁰ 4s¹',
                       'electronegativity': 1.90, 'discovery_year': None, 'discovered_by': 'Известна с древности'}
        },
        {
            'name': 'Цинк', 'symbol': 'Zn', 'atomic_number': 30, 'atomic_weight': 65.38,
            'group': 12, 'period': 4, 'category': categories['Переходные металлы'], 'state': 'solid',
            'description': 'Цинк — важный элемент для иммунной системы.',
            'fun_facts': 'Цинк используется для оцинковки стали, защищая ее от ржавчины.',
            'details': {'melting_point': 419.53, 'boiling_point': 907, 'electron_configuration': '[Ar] 3d¹⁰ 4s²',
                       'electronegativity': 1.65, 'discovery_year': 1746, 'discovered_by': 'Андреас Маргграф'}
        },
    ]
    
    for elem_data in elements_data:
        element, created = Element.objects.get_or_create(
            atomic_number=elem_data['atomic_number'],
            defaults={
                'name': elem_data['name'],
                'symbol': elem_data['symbol'],
                'atomic_weight': elem_data['atomic_weight'],
                'group': elem_data['group'],
                'period': elem_data['period'],
                'category': elem_data['category'],
                'state': elem_data.get('state', 'solid'),
                'description': elem_data['description'],
                'fun_facts': elem_data.get('fun_facts', '')
            }
        )
        
        if created:
            print(f"✓ Создан элемент: {element.name} ({element.symbol})")
        else:
            print(f"  Элемент уже существует: {element.name} ({element.symbol})")
        
        # Добавляем детали
        if 'details' in elem_data:
            detail, detail_created = ElementDetail.objects.get_or_create(
                element=element,
                defaults=elem_data['details']
            )
            if detail_created:
                print(f"  + Добавлены детали для {element.name}")

def create_reactions():
    """Создание химических реакций"""
    reactions_data = [
        {
            'name': 'Образование воды',
            'formula': '2H₂ + O₂ → 2H₂O',
            'description': 'Водород соединяется с кислородом, образуя воду. Это одна из самых важных реакций для жизни на Земле.',
            'reactants': ['H', 'O'],
            'products': ['H', 'O']
        },
        {
            'name': 'Образование поваренной соли',
            'formula': '2Na + Cl₂ → 2NaCl',
            'description': 'Натрий активно реагирует с хлором, образуя хлорид натрия (поваренную соль).',
            'reactants': ['Na', 'Cl'],
            'products': ['Na', 'Cl']
        },
        {
            'name': 'Горение углерода',
            'formula': 'C + O₂ → CO₂',
            'description': 'Углерод сгорает в кислороде, образуя углекислый газ.',
            'reactants': ['C', 'O'],
            'products': ['C', 'O']
        },
        {
            'name': 'Горение магния',
            'formula': '2Mg + O₂ → 2MgO',
            'description': 'Магний горит ярким белым светом, образуя оксид магния.',
            'reactants': ['Mg', 'O'],
            'products': ['Mg', 'O']
        },
        {
            'name': 'Реакция алюминия с кислородом',
            'formula': '4Al + 3O₂ → 2Al₂O₃',
            'description': 'Алюминий окисляется на воздухе, образуя защитную пленку оксида алюминия.',
            'reactants': ['Al', 'O'],
            'products': ['Al', 'O']
        },
    ]
    
    for reaction_data in reactions_data:
        reaction, created = ChemicalReaction.objects.get_or_create(
            name=reaction_data['name'],
            defaults={
                'reaction_formula': reaction_data['formula'],
                'description': reaction_data['description']
            }
        )
        
        if created:
            print(f"✓ Создана реакция: {reaction.name}")
            # Добавляем реагенты и продукты
            for symbol in reaction_data['reactants']:
                try:
                    element = Element.objects.get(symbol=symbol)
                    reaction.reactants.add(element)
                except Element.DoesNotExist:
                    print(f"  ! Элемент {symbol} не найден")
            
            for symbol in reaction_data['products']:
                try:
                    element = Element.objects.get(symbol=symbol)
                    reaction.products.add(element)
                except Element.DoesNotExist:
                    print(f"  ! Элемент {symbol} не найден")
        else:
            print(f"  Реакция уже существует: {reaction.name}")

def create_achievements():
    """Создание достижений"""
    achievements_data = [
        {
            'name': 'Первые шаги',
            'description': 'Посетите свою первую страницу на сайте',
            'achievement_type': 'first_action',
            'xp_reward': 10,
            'icon': 'fas fa-shoe-prints',
            'emoji': '👣'
        },
        {
            'name': 'Исследователь',
            'description': 'Просмотрите информацию о первом химическом элементе',
            'achievement_type': 'first_element',
            'xp_reward': 25,
            'icon': 'fas fa-atom',
            'emoji': '⚛️'
        },
        {
            'name': 'Искатель знаний',
            'description': 'Воспользуйтесь поиском в первый раз',
            'achievement_type': 'first_search',
            'xp_reward': 15,
            'icon': 'fas fa-search',
            'emoji': '🔍'
        },
        {
            'name': 'Ученик химии',
            'description': 'Пройдите свой первый тест',
            'achievement_type': 'first_quiz',
            'xp_reward': 50,
            'icon': 'fas fa-graduation-cap',
            'emoji': '🎓'
        },
        {
            'name': 'Мастер викторин',
            'description': 'Ответьте правильно на три вопроса подряд',
            'achievement_type': 'three_correct_answers',
            'xp_reward': 100,
            'icon': 'fas fa-trophy',
            'emoji': '🏆'
        },
    ]
    
    for ach_data in achievements_data:
        achievement, created = Achievement.objects.get_or_create(
            achievement_type=ach_data['achievement_type'],
            defaults=ach_data
        )
        if created:
            print(f"✓ Создано достижение: {achievement.name}")
        else:
            print(f"  Достижение уже существует: {achievement.name}")

def create_quizzes():
    """Создание викторин"""
    # Викторина 1: Базовые знания
    quiz1, created = Quiz.objects.get_or_create(
        title='Основы химии',
        defaults={
            'description': 'Проверьте свои базовые знания химии',
            'level': 1,
            'max_points': 50,
            'time_limit': 10
        }
    )
    
    if created:
        print(f"✓ Создана викторина: {quiz1.title}")
        
        # Вопросы для викторины 1
        questions_data = [
            {
                'text': 'Какой элемент является самым легким в периодической таблице?',
                'answers': [
                    ('Водород', True),
                    ('Гелий', False),
                    ('Литий', False),
                    ('Углерод', False)
                ],
                'element': 'H'
            },
            {
                'text': 'Какой газ составляет большую часть атмосферы Земли?',
                'answers': [
                    ('Кислород', False),
                    ('Азот', True),
                    ('Углекислый газ', False),
                    ('Водород', False)
                ],
                'element': 'N'
            },
            {
                'text': 'Какой элемент необходим для дыхания?',
                'answers': [
                    ('Водород', False),
                    ('Азот', False),
                    ('Кислород', True),
                    ('Гелий', False)
                ],
                'element': 'O'
            },
            {
                'text': 'Из какого элемента состоят алмазы?',
                'answers': [
                    ('Кремний', False),
                    ('Углерод', True),
                    ('Кислород', False),
                    ('Железо', False)
                ],
                'element': 'C'
            },
            {
                'text': 'Какой металл используется в электрических проводах?',
                'answers': [
                    ('Железо', False),
                    ('Алюминий', False),
                    ('Медь', True),
                    ('Золото', False)
                ],
                'element': 'Cu'
            },
        ]
        
        for q_data in questions_data:
            try:
                element = Element.objects.get(symbol=q_data['element'])
            except Element.DoesNotExist:
                element = None
            
            question = QuizQuestion.objects.create(
                quiz=quiz1,
                question_text=q_data['text'],
                related_element=element,
                points=10
            )
            
            for answer_text, is_correct in q_data['answers']:
                QuizAnswer.objects.create(
                    question=question,
                    answer_text=answer_text,
                    is_correct=is_correct
                )
        
        print(f"  + Добавлено {len(questions_data)} вопросов")
    
    # Викторина 2: Металлы
    quiz2, created = Quiz.objects.get_or_create(
        title='Мир металлов',
        defaults={
            'description': 'Проверьте свои знания о металлах',
            'level': 2,
            'max_points': 60,
            'time_limit': 15
        }
    )
    
    if created:
        print(f"✓ Создана викторина: {quiz2.title}")
        
        questions_data = [
            {
                'text': 'Какой металл самый распространенный в земной коре?',
                'answers': [
                    ('Железо', False),
                    ('Алюминий', True),
                    ('Медь', False),
                    ('Золото', False)
                ],
                'element': 'Al'
            },
            {
                'text': 'Какой металл используется в батарейках для смартфонов?',
                'answers': [
                    ('Натрий', False),
                    ('Литий', True),
                    ('Калий', False),
                    ('Магний', False)
                ],
                'element': 'Li'
            },
            {
                'text': 'Какой металл является основой стали?',
                'answers': [
                    ('Медь', False),
                    ('Алюминий', False),
                    ('Железо', True),
                    ('Цинк', False)
                ],
                'element': 'Fe'
            },
        ]
        
        for q_data in questions_data:
            try:
                element = Element.objects.get(symbol=q_data['element'])
            except Element.DoesNotExist:
                element = None
            
            question = QuizQuestion.objects.create(
                quiz=quiz2,
                question_text=q_data['text'],
                related_element=element,
                points=20
            )
            
            for answer_text, is_correct in q_data['answers']:
                QuizAnswer.objects.create(
                    question=question,
                    answer_text=answer_text,
                    is_correct=is_correct
                )
        
        print(f"  + Добавлено {len(questions_data)} вопросов")

if __name__ == "__main__":
    print("=" * 60)
    print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ КОНТЕНТОМ")
    print("=" * 60)
    
    from chemistry.models import ElementCategory
    
    print("\n1. Создание категорий элементов...")
    categories_dict = {}
    categories = [
        ('Щелочные металлы', 'Мягкие, активные металлы группы 1', '#FF6B6B'),
        ('Щелочноземельные металлы', 'Реактивные металлы группы 2', '#FFA07A'),
        ('Переходные металлы', 'Твердые металлы с высокой температурой плавления', '#C70039'),
        ('Неметаллы', 'Элементы с неметаллическими свойствами', '#4ECDC4'),
        ('Галогены', 'Высокореактивные неметаллы', '#95E1D3'),
        ('Благородные газы', 'Инертные газы', '#9B59B6'),
    ]
    
    for name, desc, color in categories:
        cat, created = ElementCategory.objects.get_or_create(
            name=name,
            defaults={'description': desc, 'color': color}
        )
        categories_dict[name] = cat
        if created:
            print(f"✓ Создана категория: {name}")
        else:
            print(f"  Категория уже существует: {name}")
    
    print("\n2. Создание химических элементов (30 элементов)...")
    create_extended_elements(categories_dict)
    
    print("\n3. Создание химических реакций...")
    create_reactions()
    
    print("\n4. Создание достижений...")
    create_achievements()
    
    print("\n5. Создание викторин...")
    create_quizzes()
    
    print("\n" + "=" * 60)
    print("✓ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 60)