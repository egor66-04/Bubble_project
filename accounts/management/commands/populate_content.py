"""
Django management команда для заполнения базы данных контентом
"""
from django.core.management.base import BaseCommand
from chemistry.models import Element, ElementCategory, ElementDetail, ChemicalReaction
from accounts.models import Achievement, Quiz, QuizQuestion, QuizAnswer


class Command(BaseCommand):
    help = 'Заполняет базу данных химическими элементами, реакциями и викторинами'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ КОНТЕНТОМ")
        self.stdout.write("=" * 60)
        
        # Создаем категории
        categories_dict = self.create_categories()
        
        # Создаем элементы
        self.create_elements(categories_dict)
        
        # Создаем реакции
        self.create_reactions()
        
        # Создаем достижения
        self.create_achievements()
        
        # Создаем викторины
        self.create_quizzes()
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("[OK] БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!"))
        self.stdout.write("=" * 60)
    
    def create_categories(self):
        self.stdout.write("\n1. Создание категорий элементов...")
        categories_dict = {}
        categories = [
            ('Щелочные металлы', 'Мягкие, активные металлы группы 1', '#FF6B9D'),
            ('Щелочноземельные металлы', 'Реактивные металлы группы 2', '#FFB347'),
            ('Переходные металлы', 'Твердые металлы с высокой температурой плавления', '#4FACFE'),
            ('Постпереходные металлы', 'Металлы после переходных элементов', '#43E97B'),
            ('Металлоиды', 'Полуметаллы с промежуточными свойствами', '#FA709A'),
            ('Неметаллы', 'Элементы с неметаллическими свойствами', '#667EEA'),
            ('Галогены', 'Высокореактивные неметаллы', '#FEE140'),
            ('Благородные газы', 'Инертные газы', '#C471F5'),
            ('Лантаноиды', 'Редкоземельные элементы', '#38F9D7'),
            ('Актиноиды', 'Радиоактивные элементы', '#F093FB'),
        ]
        
        for name, desc, color in categories:
            cat, created = ElementCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'color': color}
            )
            categories_dict[name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Создана категория: {name}"))
            else:
                self.stdout.write(f"  Категория уже существует: {name}")
        
        return categories_dict
    
    def create_elements(self, categories):
        self.stdout.write("\n2. Создание химических элементов (118 элементов)...")
        
        elements_data = [
            # Период 1
            {'name': 'Водород', 'symbol': 'H', 'atomic_number': 1, 'atomic_weight': 1.008, 'group': 1, 'period': 1, 
             'category': 'Неметаллы', 'state': 'gas', 
             'description': 'Водород - самый легкий и распространенный элемент во Вселенной.',
             'fun_facts': 'Водород составляет 75% массы всей видимой материи во Вселенной.'},
            
            {'name': 'Гелий', 'symbol': 'He', 'atomic_number': 2, 'atomic_weight': 4.0026, 'group': 18, 'period': 1,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Гелий - второй по распространенности элемент во Вселенной.',
             'fun_facts': 'Гелий был обнаружен на Солнце раньше, чем на Земле.'},
            
            # Период 2
            {'name': 'Литий', 'symbol': 'Li', 'atomic_number': 3, 'atomic_weight': 6.94, 'group': 1, 'period': 2,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Литий - самый легкий металл.',
             'fun_facts': 'Используется в современных аккумуляторах для телефонов и электромобилей.'},
            
            {'name': 'Бериллий', 'symbol': 'Be', 'atomic_number': 4, 'atomic_weight': 9.0122, 'group': 2, 'period': 2,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Бериллий - легкий, прочный металл.',
             'fun_facts': 'Используется в аэрокосмической промышленности из-за высокой прочности.'},
            
            {'name': 'Бор', 'symbol': 'B', 'atomic_number': 5, 'atomic_weight': 10.81, 'group': 13, 'period': 2,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Бор - полуметалл, необходимый для роста растений.',
             'fun_facts': 'Бор используется в производстве боросиликатного стекла.'},
            
            {'name': 'Углерод', 'symbol': 'C', 'atomic_number': 6, 'atomic_weight': 12.011, 'group': 14, 'period': 2,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Углерод - основа всей органической химии и жизни.',
             'fun_facts': 'Алмаз и графит - две формы углерода с совершенно разными свойствами.'},
            
            {'name': 'Азот', 'symbol': 'N', 'atomic_number': 7, 'atomic_weight': 14.007, 'group': 15, 'period': 2,
             'category': 'Неметаллы', 'state': 'gas',
             'description': 'Азот составляет 78% атмосферы Земли.',
             'fun_facts': 'Жидкий азот используется для быстрой заморозки.'},
            
            {'name': 'Кислород', 'symbol': 'O', 'atomic_number': 8, 'atomic_weight': 15.999, 'group': 16, 'period': 2,
             'category': 'Неметаллы', 'state': 'gas',
             'description': 'Кислород необходим для дыхания большинства живых организмов.',
             'fun_facts': 'Без кислорода человек может прожить всего несколько минут.'},
            
            {'name': 'Фтор', 'symbol': 'F', 'atomic_number': 9, 'atomic_weight': 18.998, 'group': 17, 'period': 2,
             'category': 'Галогены', 'state': 'gas',
             'description': 'Фтор - самый активный неметалл.',
             'fun_facts': 'Фтор добавляют в зубную пасту для защиты от кариеса.'},
            
            {'name': 'Неон', 'symbol': 'Ne', 'atomic_number': 10, 'atomic_weight': 20.180, 'group': 18, 'period': 2,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Неон - инертный газ, используемый в неоновых лампах.',
             'fun_facts': 'Неоновые вывески светятся красно-оранжевым светом.'},
            
            # Период 3
            {'name': 'Натрий', 'symbol': 'Na', 'atomic_number': 11, 'atomic_weight': 22.990, 'group': 1, 'period': 3,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Натрий - мягкий металл, активно реагирующий с водой.',
             'fun_facts': 'Хлорид натрия (NaCl) - это обычная поваренная соль.'},
            
            {'name': 'Магний', 'symbol': 'Mg', 'atomic_number': 12, 'atomic_weight': 24.305, 'group': 2, 'period': 3,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Магний - легкий серебристый металл.',
             'fun_facts': 'Магний горит ярким белым пламенем и используется в фейерверках.'},
            
            {'name': 'Алюминий', 'symbol': 'Al', 'atomic_number': 13, 'atomic_weight': 26.982, 'group': 13, 'period': 3,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Алюминий - легкий, прочный металл.',
             'fun_facts': 'Самый распространенный металл в земной коре.'},
            
            {'name': 'Кремний', 'symbol': 'Si', 'atomic_number': 14, 'atomic_weight': 28.085, 'group': 14, 'period': 3,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Кремний - основа компьютерных чипов.',
             'fun_facts': 'Второй по распространенности элемент в земной коре после кислорода.'},
            
            {'name': 'Фосфор', 'symbol': 'P', 'atomic_number': 15, 'atomic_weight': 30.974, 'group': 15, 'period': 3,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Фосфор - необходим для всех живых организмов.',
             'fun_facts': 'Белый фосфор светится в темноте и самовоспламеняется на воздухе.'},
            
            {'name': 'Сера', 'symbol': 'S', 'atomic_number': 16, 'atomic_weight': 32.06, 'group': 16, 'period': 3,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Сера - желтый неметалл с характерным запахом.',
             'fun_facts': 'Сера используется в производстве спичек и серной кислоты.'},
            
            {'name': 'Хлор', 'symbol': 'Cl', 'atomic_number': 17, 'atomic_weight': 35.45, 'group': 17, 'period': 3,
             'category': 'Галогены', 'state': 'gas',
             'description': 'Хлор - ядовитый газ желто-зеленого цвета.',
             'fun_facts': 'Используется для дезинфекции воды в бассейнах и водопроводе.'},
            
            {'name': 'Аргон', 'symbol': 'Ar', 'atomic_number': 18, 'atomic_weight': 39.948, 'group': 18, 'period': 3,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Аргон - инертный газ, третий по распространенности в атмосфере.',
             'fun_facts': 'Используется в лампах накаливания для предотвращения окисления нити.'},
            
            # Период 4
            {'name': 'Калий', 'symbol': 'K', 'atomic_number': 19, 'atomic_weight': 39.098, 'group': 1, 'period': 4,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Калий - мягкий металл, необходимый для работы нервной системы.',
             'fun_facts': 'Калий настолько мягкий, что его можно резать ножом.'},
            
            {'name': 'Кальций', 'symbol': 'Ca', 'atomic_number': 20, 'atomic_weight': 40.078, 'group': 2, 'period': 4,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Кальций - важнейший элемент для костей и зубов.',
             'fun_facts': '99% кальция в организме находится в костях и зубах.'},
            
            {'name': 'Железо', 'symbol': 'Fe', 'atomic_number': 26, 'atomic_weight': 55.845, 'group': 8, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Железо - основной компонент стали.',
             'fun_facts': 'Железо составляет основу земного ядра.'},
            
            {'name': 'Медь', 'symbol': 'Cu', 'atomic_number': 29, 'atomic_weight': 63.546, 'group': 11, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Медь - отличный проводник электричества.',
             'fun_facts': 'Медь была одним из первых металлов, освоенных человечеством.'},
            
            {'name': 'Цинк', 'symbol': 'Zn', 'atomic_number': 30, 'atomic_weight': 65.38, 'group': 12, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Цинк - важный элемент для иммунной системы.',
             'fun_facts': 'Цинк используется для оцинковки стали, защищая ее от ржавчины.'},
            
            # Дополнительные элементы из периода 4
            {'name': 'Бром', 'symbol': 'Br', 'atomic_number': 35, 'atomic_weight': 79.904, 'group': 17, 'period': 4,
             'category': 'Галогены', 'state': 'liquid',
             'description': 'Бром - единственный неметалл, который при комнатной температуре находится в жидком состоянии.',
             'fun_facts': 'Бром имеет резкий неприятный запах, его название происходит от греческого слова "зловонный".'},
            
            {'name': 'Криптон', 'symbol': 'Kr', 'atomic_number': 36, 'atomic_weight': 83.798, 'group': 18, 'period': 4,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Криптон - инертный газ, используемый в лазерах и лампах.',
             'fun_facts': 'Криптон получил свое название от греческого слова "скрытый", так как долго оставался незамеченным.'},
            
            # Период 5
            {'name': 'Серебро', 'symbol': 'Ag', 'atomic_number': 47, 'atomic_weight': 107.87, 'group': 11, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Серебро - драгоценный металл с наивысшей электропроводностью.',
             'fun_facts': 'Серебро обладает антибактериальными свойствами и используется в медицине.'},
            
            {'name': 'Иод', 'symbol': 'I', 'atomic_number': 53, 'atomic_weight': 126.90, 'group': 17, 'period': 5,
             'category': 'Галогены', 'state': 'solid',
             'description': 'Иод необходим для работы щитовидной железы.',
             'fun_facts': 'При нагревании иод превращается в фиолетовый пар, минуя жидкую фазу.'},
            
            {'name': 'Ксенон', 'symbol': 'Xe', 'atomic_number': 54, 'atomic_weight': 131.29, 'group': 18, 'period': 5,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Ксенон используется в мощных лампах и медицинской анестезии.',
             'fun_facts': 'Ксеноновые фары в автомобилях дают яркий белый свет.'},
            
            # Период 6
            {'name': 'Золото', 'symbol': 'Au', 'atomic_number': 79, 'atomic_weight': 196.97, 'group': 11, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Золото - драгоценный металл, не подверженный коррозии.',
             'fun_facts': 'Золото настолько ковкое, что из одного грамма можно вытянуть проволоку длиной 3 километра.'},
            
            {'name': 'Ртуть', 'symbol': 'Hg', 'atomic_number': 80, 'atomic_weight': 200.59, 'group': 12, 'period': 6,
             'category': 'Переходные металлы', 'state': 'liquid',
             'description': 'Ртуть - единственный металл, который при комнатной температуре находится в жидком состоянии.',
             'fun_facts': 'Ртуть очень ядовита, поэтому ртутные термометры постепенно выходят из употребления.'},
            
            {'name': 'Радон', 'symbol': 'Rn', 'atomic_number': 86, 'atomic_weight': 222.0, 'group': 18, 'period': 6,
             'category': 'Благородные газы', 'state': 'gas',
             'description': 'Радон - радиоактивный благородный газ.',
             'fun_facts': 'Радон является второй по значимости причиной рака легких после курения.'},
            
            # Дополнительные элементы периода 4
            {'name': 'Скандий', 'symbol': 'Sc', 'atomic_number': 21, 'atomic_weight': 44.956, 'group': 3, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Скандий - легкий переходный металл.',
             'fun_facts': 'Скандий используется в сплавах для аэрокосмической промышленности.'},
            
            {'name': 'Титан', 'symbol': 'Ti', 'atomic_number': 22, 'atomic_weight': 47.867, 'group': 4, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Титан - прочный и легкий металл.',
             'fun_facts': 'Титан используется в медицинских имплантах из-за биосовместимости.'},
            
            {'name': 'Ванадий', 'symbol': 'V', 'atomic_number': 23, 'atomic_weight': 50.942, 'group': 5, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Ванадий - твердый металл, используемый в сплавах.',
             'fun_facts': 'Добавление ванадия делает сталь более прочной.'},
            
            {'name': 'Хром', 'symbol': 'Cr', 'atomic_number': 24, 'atomic_weight': 51.996, 'group': 6, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Хром - твердый металл серебристого цвета.',
             'fun_facts': 'Хром используется для хромирования и придания блеска металлам.'},
            
            {'name': 'Марганец', 'symbol': 'Mn', 'atomic_number': 25, 'atomic_weight': 54.938, 'group': 7, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Марганец - важный компонент стали.',
             'fun_facts': 'Марганец необходим для фотосинтеза в растениях.'},
            
            {'name': 'Кобальт', 'symbol': 'Co', 'atomic_number': 27, 'atomic_weight': 58.933, 'group': 9, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Кобальт - магнитный металл.',
             'fun_facts': 'Кобальт используется в производстве аккумуляторов и магнитов.'},
            
            {'name': 'Никель', 'symbol': 'Ni', 'atomic_number': 28, 'atomic_weight': 58.693, 'group': 10, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Никель - коррозионностойкий металл.',
             'fun_facts': 'Никель используется в монетах и нержавеющей стали.'},
            
            {'name': 'Галлий', 'symbol': 'Ga', 'atomic_number': 31, 'atomic_weight': 69.723, 'group': 13, 'period': 4,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Галлий плавится при температуре чуть выше комнатной.',
             'fun_facts': 'Галлий может расплавиться в руке.'},
            
            {'name': 'Германий', 'symbol': 'Ge', 'atomic_number': 32, 'atomic_weight': 72.630, 'group': 14, 'period': 4,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Германий - полупроводник.',
             'fun_facts': 'Германий используется в оптоволоконных кабелях.'},
            
            {'name': 'Мышьяк', 'symbol': 'As', 'atomic_number': 33, 'atomic_weight': 74.922, 'group': 15, 'period': 4,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Мышьяк - ядовитый полуметалл.',
             'fun_facts': 'В малых дозах мышьяк используется в медицине.'},
            
            {'name': 'Селен', 'symbol': 'Se', 'atomic_number': 34, 'atomic_weight': 78.971, 'group': 16, 'period': 4,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Селен - важный микроэлемент для здоровья.',
             'fun_facts': 'Селен используется в фотоэлементах и копировальной технике.'},
            
            # Период 5
            {'name': 'Рубидий', 'symbol': 'Rb', 'atomic_number': 37, 'atomic_weight': 85.468, 'group': 1, 'period': 5,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Рубидий - мягкий щелочной металл.',
             'fun_facts': 'Рубидий самовозгорается на воздухе.'},
            
            {'name': 'Стронций', 'symbol': 'Sr', 'atomic_number': 38, 'atomic_weight': 87.62, 'group': 2, 'period': 5,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Стронций придает красный цвет фейерверкам.',
             'fun_facts': 'Стронций используется в производстве магнитов для холодильников.'},
            
            {'name': 'Иттрий', 'symbol': 'Y', 'atomic_number': 39, 'atomic_weight': 88.906, 'group': 3, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Иттрий используется в светодиодах.',
             'fun_facts': 'Назван в честь шведской деревни Иттербю.'},
            
            {'name': 'Цирконий', 'symbol': 'Zr', 'atomic_number': 40, 'atomic_weight': 91.224, 'group': 4, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Цирконий - коррозионностойкий металл.',
             'fun_facts': 'Цирконий используется в ядерных реакторах.'},
            
            {'name': 'Ниобий', 'symbol': 'Nb', 'atomic_number': 41, 'atomic_weight': 92.906, 'group': 5, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Ниобий - сверхпроводящий металл.',
             'fun_facts': 'Используется в ювелирных изделиях и медицинских имплантах.'},
            
            {'name': 'Молибден', 'symbol': 'Mo', 'atomic_number': 42, 'atomic_weight': 95.95, 'group': 6, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Молибден укрепляет сталь.',
             'fun_facts': 'Важный элемент для жизни, входит в состав ферментов.'},
            
            {'name': 'Технеций', 'symbol': 'Tc', 'atomic_number': 43, 'atomic_weight': 98.0, 'group': 7, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Технеций - первый искусственно полученный элемент.',
             'fun_facts': 'Все изотопы технеция радиоактивны.'},
            
            {'name': 'Рутений', 'symbol': 'Ru', 'atomic_number': 44, 'atomic_weight': 101.07, 'group': 8, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Рутений - твердый платиновый металл.',
             'fun_facts': 'Используется как катализатор в химии.'},
            
            {'name': 'Родий', 'symbol': 'Rh', 'atomic_number': 45, 'atomic_weight': 102.91, 'group': 9, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Родий - один из самых дорогих металлов.',
             'fun_facts': 'Используется в автомобильных катализаторах.'},
            
            {'name': 'Палладий', 'symbol': 'Pd', 'atomic_number': 46, 'atomic_weight': 106.42, 'group': 10, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Палладий поглощает водород.',
             'fun_facts': 'Используется в ювелирных изделиях и электронике.'},
            
            {'name': 'Кадмий', 'symbol': 'Cd', 'atomic_number': 48, 'atomic_weight': 112.41, 'group': 12, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Кадмий - токсичный металл.',
             'fun_facts': 'Используется в никель-кадмиевых батареях.'},
            
            {'name': 'Индий', 'symbol': 'In', 'atomic_number': 49, 'atomic_weight': 114.82, 'group': 13, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Индий - мягкий металл.',
             'fun_facts': 'Используется в сенсорных экранах.'},
            
            {'name': 'Олово', 'symbol': 'Sn', 'atomic_number': 50, 'atomic_weight': 118.71, 'group': 14, 'period': 5,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Олово используется для лужения металлов.',
             'fun_facts': 'Олово не токсично и используется в пищевой промышленности.'},
            
            {'name': 'Сурьма', 'symbol': 'Sb', 'atomic_number': 51, 'atomic_weight': 121.76, 'group': 15, 'period': 5,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Сурьма - хрупкий полуметалл.',
             'fun_facts': 'Используется в огнезащитных материалах.'},
            
            {'name': 'Теллур', 'symbol': 'Te', 'atomic_number': 52, 'atomic_weight': 127.60, 'group': 16, 'period': 5,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Теллур - редкий полуметалл.',
             'fun_facts': 'Используется в солнечных батареях.'},
            
            # Период 6
            {'name': 'Цезий', 'symbol': 'Cs', 'atomic_number': 55, 'atomic_weight': 132.91, 'group': 1, 'period': 6,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Цезий - самый реактивный металл.',
             'fun_facts': 'Используется в атомных часах - самых точных часах в мире.'},
            
            {'name': 'Барий', 'symbol': 'Ba', 'atomic_number': 56, 'atomic_weight': 137.33, 'group': 2, 'period': 6,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Барий придает зеленый цвет фейерверкам.',
             'fun_facts': 'Используется в медицинской рентгенографии.'},
            
            {'name': 'Лантан', 'symbol': 'La', 'atomic_number': 57, 'atomic_weight': 138.91, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Лантан - первый из лантаноидов.',
             'fun_facts': 'Используется в никель-металл-гидридных батареях.'},
            
            {'name': 'Церий', 'symbol': 'Ce', 'atomic_number': 58, 'atomic_weight': 140.12, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Церий - самый распространенный редкоземельный элемент.',
             'fun_facts': 'Используется в самоочищающихся печах.'},
            
            {'name': 'Празеодим', 'symbol': 'Pr', 'atomic_number': 59, 'atomic_weight': 140.91, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Празеодим - редкоземельный металл.',
             'fun_facts': 'Используется в сварочных очках для защиты от ультрафиолета.'},
            
            {'name': 'Неодим', 'symbol': 'Nd', 'atomic_number': 60, 'atomic_weight': 144.24, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Неодим создает сильнейшие постоянные магниты.',
             'fun_facts': 'Неодимовые магниты в 10 раз сильнее обычных.'},
            
            {'name': 'Прометий', 'symbol': 'Pm', 'atomic_number': 61, 'atomic_weight': 145.0, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Прометий - радиоактивный редкоземельный элемент.',
             'fun_facts': 'Не имеет стабильных изотопов.'},
            
            {'name': 'Самарий', 'symbol': 'Sm', 'atomic_number': 62, 'atomic_weight': 150.36, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Самарий используется в магнитах.',
             'fun_facts': 'Назван в честь минерала самарскит.'},
            
            {'name': 'Европий', 'symbol': 'Eu', 'atomic_number': 63, 'atomic_weight': 151.96, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Европий - самый реакционноспособный редкоземельный элемент.',
             'fun_facts': 'Используется в люминофорах телевизоров.'},
            
            {'name': 'Гадолиний', 'symbol': 'Gd', 'atomic_number': 64, 'atomic_weight': 157.25, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Гадолиний - ферромагнитный металл.',
             'fun_facts': 'Используется в МРТ как контрастное вещество.'},
            
            {'name': 'Тербий', 'symbol': 'Tb', 'atomic_number': 65, 'atomic_weight': 158.93, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Тербий используется в люминофорах.',
             'fun_facts': 'Назван в честь деревни Иттербю в Швеции.'},
            
            {'name': 'Диспрозий', 'symbol': 'Dy', 'atomic_number': 66, 'atomic_weight': 162.50, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Диспрозий - магнитный редкоземельный элемент.',
             'fun_facts': 'Используется в магнитах для ветрогенераторов.'},
            
            {'name': 'Гольмий', 'symbol': 'Ho', 'atomic_number': 67, 'atomic_weight': 164.93, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Гольмий обладает сильными магнитными свойствами.',
             'fun_facts': 'Имеет самую высокую магнитную силу среди элементов.'},
            
            {'name': 'Эрбий', 'symbol': 'Er', 'atomic_number': 68, 'atomic_weight': 167.26, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Эрбий используется в оптоволоконных усилителях.',
             'fun_facts': 'Придает розовый цвет стеклу.'},
            
            {'name': 'Тулий', 'symbol': 'Tm', 'atomic_number': 69, 'atomic_weight': 168.93, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Тулий - один из самых редких редкоземельных элементов.',
             'fun_facts': 'Используется в портативных рентгеновских аппаратах.'},
            
            {'name': 'Иттербий', 'symbol': 'Yb', 'atomic_number': 70, 'atomic_weight': 173.05, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Иттербий используется в лазерах.',
             'fun_facts': 'Назван в честь шведской деревни Иттербю.'},
            
            {'name': 'Лютеций', 'symbol': 'Lu', 'atomic_number': 71, 'atomic_weight': 174.97, 'group': 3, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Лютеций - последний из лантаноидов.',
             'fun_facts': 'Один из самых дорогих редкоземельных металлов.'},
            
            {'name': 'Гафний', 'symbol': 'Hf', 'atomic_number': 72, 'atomic_weight': 178.49, 'group': 4, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Гафний похож на цирконий.',
             'fun_facts': 'Используется в ядерных реакторах как поглотитель нейтронов.'},
            
            {'name': 'Тантал', 'symbol': 'Ta', 'atomic_number': 73, 'atomic_weight': 180.95, 'group': 5, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Тантал - очень коррозионностойкий металл.',
             'fun_facts': 'Используется в медицинских имплантах и конденсаторах.'},
            
            {'name': 'Вольфрам', 'symbol': 'W', 'atomic_number': 74, 'atomic_weight': 183.84, 'group': 6, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Вольфрам имеет самую высокую температуру плавления среди металлов.',
             'fun_facts': 'Используется в нитях накаливания лампочек.'},
            
            {'name': 'Рений', 'symbol': 'Re', 'atomic_number': 75, 'atomic_weight': 186.21, 'group': 7, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Рений - один из самых плотных элементов.',
             'fun_facts': 'Используется в реактивных двигателях.'},
            
            {'name': 'Осмий', 'symbol': 'Os', 'atomic_number': 76, 'atomic_weight': 190.23, 'group': 8, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Осмий - самый плотный природный элемент.',
             'fun_facts': 'В два раза плотнее свинца.'},
            
            {'name': 'Иридий', 'symbol': 'Ir', 'atomic_number': 77, 'atomic_weight': 192.22, 'group': 9, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Иридий - один из самых коррозионностойких металлов.',
             'fun_facts': 'Используется в свечах зажигания высокопроизводительных двигателей.'},
            
            {'name': 'Платина', 'symbol': 'Pt', 'atomic_number': 78, 'atomic_weight': 195.08, 'group': 10, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Платина - благородный металл.',
             'fun_facts': 'Используется в ювелирных изделиях и каталитических нейтрализаторах.'},
            
            {'name': 'Свинец', 'symbol': 'Pb', 'atomic_number': 82, 'atomic_weight': 207.2, 'group': 14, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Свинец - тяжелый токсичный металл.',
             'fun_facts': 'Защищает от радиации, используется в рентгеновских кабинетах.'},
            
            {'name': 'Висмут', 'symbol': 'Bi', 'atomic_number': 83, 'atomic_weight': 208.98, 'group': 15, 'period': 6,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Висмут - хрупкий металл с розовым оттенком.',
             'fun_facts': 'Используется в лекарствах для лечения желудка.'},
            
            {'name': 'Полоний', 'symbol': 'Po', 'atomic_number': 84, 'atomic_weight': 209.0, 'group': 16, 'period': 6,
             'category': 'Неметаллы', 'state': 'solid',
             'description': 'Полоний - радиоактивный элемент.',
             'fun_facts': 'Открыт Марией Кюри и назван в честь Польши.'},
            
            {'name': 'Астат', 'symbol': 'At', 'atomic_number': 85, 'atomic_weight': 210.0, 'group': 17, 'period': 6,
             'category': 'Галогены', 'state': 'solid',
             'description': 'Астат - редчайший природный элемент.',
             'fun_facts': 'В земной коре содержится менее 30 граммов астата.'},
            
            # Период 7
            {'name': 'Франций', 'symbol': 'Fr', 'atomic_number': 87, 'atomic_weight': 223.0, 'group': 1, 'period': 7,
             'category': 'Щелочные металлы', 'state': 'solid',
             'description': 'Франций - самый редкий щелочной металл.',
             'fun_facts': 'В любой момент на Земле существует не более 30 граммов франция.'},
            
            {'name': 'Радий', 'symbol': 'Ra', 'atomic_number': 88, 'atomic_weight': 226.0, 'group': 2, 'period': 7,
             'category': 'Щелочноземельные металлы', 'state': 'solid',
             'description': 'Радий - радиоактивный щелочноземельный металл.',
             'fun_facts': 'Открыт Марией и Пьером Кюри.'},
            
            {'name': 'Актиний', 'symbol': 'Ac', 'atomic_number': 89, 'atomic_weight': 227.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Актиний - радиоактивный металл.',
             'fun_facts': 'Светится голубым светом в темноте из-за радиоактивности.'},
            
            {'name': 'Торий', 'symbol': 'Th', 'atomic_number': 90, 'atomic_weight': 232.04, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Торий - потенциальное ядерное топливо.',
             'fun_facts': 'Более распространен, чем уран.'},
            
            {'name': 'Протактиний', 'symbol': 'Pa', 'atomic_number': 91, 'atomic_weight': 231.04, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Протактиний - радиоактивный металл.',
             'fun_facts': 'Один из самых редких элементов.'},
            
            {'name': 'Уран', 'symbol': 'U', 'atomic_number': 92, 'atomic_weight': 238.03, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Уран - основное ядерное топливо.',
             'fun_facts': 'Используется в атомных электростанциях и ядерном оружии.'},
            
            {'name': 'Нептуний', 'symbol': 'Np', 'atomic_number': 93, 'atomic_weight': 237.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Нептуний - первый трансурановый элемент.',
             'fun_facts': 'Назван в честь планеты Нептун.'},
            
            {'name': 'Плутоний', 'symbol': 'Pu', 'atomic_number': 94, 'atomic_weight': 244.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Плутоний - ядерное топливо и оружейный материал.',
             'fun_facts': 'Назван в честь планеты Плутон.'},
            
            {'name': 'Америций', 'symbol': 'Am', 'atomic_number': 95, 'atomic_weight': 243.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Америций используется в детекторах дыма.',
             'fun_facts': 'Назван в честь Америки.'},
            
            {'name': 'Кюрий', 'symbol': 'Cm', 'atomic_number': 96, 'atomic_weight': 247.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Кюрий - радиоактивный элемент.',
             'fun_facts': 'Назван в честь Марии и Пьера Кюри.'},
            
            {'name': 'Берклий', 'symbol': 'Bk', 'atomic_number': 97, 'atomic_weight': 247.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Берклий - синтетический элемент.',
             'fun_facts': 'Назван в честь города Беркли, Калифорния.'},
            
            {'name': 'Калифорний', 'symbol': 'Cf', 'atomic_number': 98, 'atomic_weight': 251.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Калифорний - сильный источник нейтронов.',
             'fun_facts': 'Стоимость 1 грамма около 27 миллионов долларов.'},
            
            {'name': 'Эйнштейний', 'symbol': 'Es', 'atomic_number': 99, 'atomic_weight': 252.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Эйнштейний - синтетический элемент.',
             'fun_facts': 'Назван в честь Альберта Эйнштейна.'},
            
            {'name': 'Фермий', 'symbol': 'Fm', 'atomic_number': 100, 'atomic_weight': 257.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Фермий - радиоактивный элемент.',
             'fun_facts': 'Назван в честь Энрико Ферми.'},
            
            {'name': 'Менделевий', 'symbol': 'Md', 'atomic_number': 101, 'atomic_weight': 258.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Менделевий - синтетический элемент.',
             'fun_facts': 'Назван в честь Дмитрия Менделеева.'},
            
            {'name': 'Нобелий', 'symbol': 'No', 'atomic_number': 102, 'atomic_weight': 259.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Нобелий - синтетический элемент.',
             'fun_facts': 'Назван в честь Альфреда Нобеля.'},
            
            {'name': 'Лоуренсий', 'symbol': 'Lr', 'atomic_number': 103, 'atomic_weight': 262.0, 'group': 3, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Лоуренсий - последний актиноид.',
             'fun_facts': 'Назван в честь Эрнеста Лоуренса.'},
            
            {'name': 'Резерфордий', 'symbol': 'Rf', 'atomic_number': 104, 'atomic_weight': 267.0, 'group': 4, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Резерфордий - синтетический элемент.',
             'fun_facts': 'Назван в честь Эрнеста Резерфорда.'},
            
            {'name': 'Дубний', 'symbol': 'Db', 'atomic_number': 105, 'atomic_weight': 268.0, 'group': 5, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Дубний - синтетический элемент.',
             'fun_facts': 'Назван в честь города Дубна, Россия.'},
            
            {'name': 'Сиборгий', 'symbol': 'Sg', 'atomic_number': 106, 'atomic_weight': 271.0, 'group': 6, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Сиборгий - синтетический элемент.',
             'fun_facts': 'Назван в честь Гленна Сиборга.'},
            
            {'name': 'Борий', 'symbol': 'Bh', 'atomic_number': 107, 'atomic_weight': 272.0, 'group': 7, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Борий - синтетический элемент.',
             'fun_facts': 'Назван в честь Нильса Бора.'},
            
            {'name': 'Хассий', 'symbol': 'Hs', 'atomic_number': 108, 'atomic_weight': 270.0, 'group': 8, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Хассий - синтетический элемент.',
             'fun_facts': 'Назван в честь земли Гессен в Германии.'},
            
            {'name': 'Мейтнерий', 'symbol': 'Mt', 'atomic_number': 109, 'atomic_weight': 276.0, 'group': 9, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Мейтнерий - синтетический элемент.',
             'fun_facts': 'Назван в честь Лизы Мейтнер.'},
            
            {'name': 'Дармштадтий', 'symbol': 'Ds', 'atomic_number': 110, 'atomic_weight': 281.0, 'group': 10, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Дармштадтий - синтетический элемент.',
             'fun_facts': 'Назван в честь города Дармштадт, Германия.'},
            
            {'name': 'Рентгений', 'symbol': 'Rg', 'atomic_number': 111, 'atomic_weight': 280.0, 'group': 11, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Рентгений - синтетический элемент.',
             'fun_facts': 'Назван в честь Вильгельма Рентгена.'},
            
            {'name': 'Коперниций', 'symbol': 'Cn', 'atomic_number': 112, 'atomic_weight': 285.0, 'group': 12, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Коперниций - синтетический элемент.',
             'fun_facts': 'Назван в честь Николая Коперника.'},
            
            {'name': 'Нихоний', 'symbol': 'Nh', 'atomic_number': 113, 'atomic_weight': 284.0, 'group': 13, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Нихоний - синтетический элемент.',
             'fun_facts': 'Первый элемент, открытый в Азии (Япония).'},
            
            {'name': 'Флеровий', 'symbol': 'Fl', 'atomic_number': 114, 'atomic_weight': 289.0, 'group': 14, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Флеровий - синтетический элемент.',
             'fun_facts': 'Назван в честь Георгия Флёрова.'},
            
            {'name': 'Московий', 'symbol': 'Mc', 'atomic_number': 115, 'atomic_weight': 288.0, 'group': 15, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Московий - синтетический элемент.',
             'fun_facts': 'Назван в честь Московской области.'},
            
            {'name': 'Ливерморий', 'symbol': 'Lv', 'atomic_number': 116, 'atomic_weight': 293.0, 'group': 16, 'period': 7,
             'category': 'Переходные металлы', 'state': 'solid',
             'description': 'Ливерморий - синтетический элемент.',
             'fun_facts': 'Назван в честь Ливерморской национальной лаборатории.'},
            
            {'name': 'Теннессин', 'symbol': 'Ts', 'atomic_number': 117, 'atomic_weight': 294.0, 'group': 17, 'period': 7,
             'category': 'Галогены', 'state': 'solid',
             'description': 'Теннессин - синтетический галоген.',
             'fun_facts': 'Назван в честь штата Теннесси, США.'},
            
            {'name': 'Оганесон', 'symbol': 'Og', 'atomic_number': 118, 'atomic_weight': 294.0, 'group': 18, 'period': 7,
             'category': 'Благородные газы', 'state': 'solid',
             'description': 'Оганесон - самый тяжелый элемент таблицы Менделеева.',
             'fun_facts': 'Назван в честь российского физика Юрия Оганесяна.'},
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
                    'category': categories[elem_data['category']],
                    'state': elem_data.get('state', 'solid'),
                    'description': elem_data['description'],
                    'fun_facts': elem_data.get('fun_facts', '')
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Создан элемент: {element.name} ({element.symbol})"))
            else:
                self.stdout.write(f"  Элемент уже существует: {element.name} ({element.symbol})")
    
    def create_reactions(self):
        self.stdout.write("\n3. Создание химических реакций...")
        
        reactions_data = [
            {
                'name': 'Образование воды',
                'formula': '2H₂ + O₂ → 2H₂O',
                'description': 'Водород соединяется с кислородом, образуя воду.',
                'reactants': ['H', 'O'],
                'products': ['H', 'O']
            },
            {
                'name': 'Образование поваренной соли',
                'formula': '2Na + Cl₂ → 2NaCl',
                'description': 'Натрий активно реагирует с хлором, образуя поваренную соль.',
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
                'name': 'Образование аммиака',
                'formula': 'N₂ + 3H₂ → 2NH₃',
                'description': 'Азот соединяется с водородом при высоких температуре и давлении, образуя аммиак.',
                'reactants': ['N', 'H'],
                'products': ['N', 'H']
            },
            {
                'name': 'Образование хлорида кальция',
                'formula': 'Ca + Cl₂ → CaCl₂',
                'description': 'Кальций активно реагирует с хлором, образуя хлорид кальция.',
                'reactants': ['Ca', 'Cl'],
                'products': ['Ca', 'Cl']
            },
            {
                'name': 'Реакция натрия с водой',
                'formula': '2Na + 2H₂O → 2NaOH + H₂',
                'description': 'Натрий бурно реагирует с водой, образуя гидроксид натрия и водород.',
                'reactants': ['Na', 'H', 'O'],
                'products': ['Na', 'O', 'H']
            },
            {
                'name': 'Образование серной кислоты',
                'formula': 'S + O₂ + H₂O → H₂SO₄',
                'description': 'Сера окисляется кислородом и взаимодействует с водой, образуя серную кислоту.',
                'reactants': ['S', 'O', 'H'],
                'products': ['S', 'O', 'H']
            },
            {
                'name': 'Фотосинтез (упрощенно)',
                'formula': '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂',
                'description': 'В процессе фотосинтеза растения превращают углекислый газ и воду в глюкозу и кислород.',
                'reactants': ['C', 'O', 'H'],
                'products': ['C', 'H', 'O']
            },
            {
                'name': 'Ржавление железа',
                'formula': '4Fe + 3O₂ → 2Fe₂O₃',
                'description': 'Железо окисляется кислородом воздуха, образуя ржавчину (оксид железа).',
                'reactants': ['Fe', 'O'],
                'products': ['Fe', 'O']
            },
            {
                'name': 'Образование метана',
                'formula': 'C + 2H₂ → CH₄',
                'description': 'Углерод соединяется с водородом, образуя метан - простейший углеводород.',
                'reactants': ['C', 'H'],
                'products': ['C', 'H']
            },
        ]
        
        for reaction_data in reactions_data:
            # Проверяем наличие реакции с таким именем
            existing_reactions = ChemicalReaction.objects.filter(name=reaction_data['name'])
            
            if existing_reactions.count() > 1:
                # Удаляем дубликаты, оставляя только первую
                for duplicate in existing_reactions[1:]:
                    duplicate.delete()
                reaction = existing_reactions.first()
                created = False
            elif existing_reactions.count() == 1:
                reaction = existing_reactions.first()
                created = False
            else:
                reaction = ChemicalReaction.objects.create(
                    name=reaction_data['name'],
                    reaction_formula=reaction_data['formula'],
                    description=reaction_data['description']
                )
                created = True
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Создана реакция: {reaction.name}"))
                for symbol in reaction_data['reactants']:
                    try:
                        element = Element.objects.get(symbol=symbol)
                        reaction.reactants.add(element)
                    except Element.DoesNotExist:
                        pass
                
                for symbol in reaction_data['products']:
                    try:
                        element = Element.objects.get(symbol=symbol)
                        reaction.products.add(element)
                    except Element.DoesNotExist:
                        pass
            else:
                self.stdout.write(f"  Реакция уже существует: {reaction.name}")
    
    def create_achievements(self):
        self.stdout.write("\n4. Создание достижений...")
        
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
            {
                'name': 'Коллекционер',
                'description': 'Добавьте первый элемент в избранное',
                'achievement_type': 'first_favorite',
                'xp_reward': 20,
                'icon': 'fas fa-star',
                'emoji': '⭐'
            },
            {
                'name': 'Экспериментатор',
                'description': 'Просмотрите первую химическую реакцию',
                'achievement_type': 'first_reaction',
                'xp_reward': 30,
                'icon': 'fas fa-flask',
                'emoji': '⚗️'
            },
            {
                'name': 'Новичок',
                'description': 'Наберите 100 очков опыта',
                'achievement_type': 'xp_100',
                'xp_reward': 50,
                'icon': 'fas fa-level-up-alt',
                'emoji': '📈'
            },
            {
                'name': 'Опытный химик',
                'description': 'Наберите 500 очков опыта',
                'achievement_type': 'xp_500',
                'xp_reward': 100,
                'icon': 'fas fa-chart-line',
                'emoji': '📊'
            },
            {
                'name': 'Знаток таблицы',
                'description': 'Изучите 10 разных элементов',
                'achievement_type': 'elements_10',
                'xp_reward': 75,
                'icon': 'fas fa-book-open',
                'emoji': '📖'
            },
            {
                'name': 'Мастер элементов',
                'description': 'Изучите 30 разных элементов',
                'achievement_type': 'elements_30',
                'xp_reward': 150,
                'icon': 'fas fa-medal',
                'emoji': '🥇'
            },
            {
                'name': 'Отличник',
                'description': 'Пройдите викторину на 100%',
                'achievement_type': 'perfect_quiz',
                'xp_reward': 200,
                'icon': 'fas fa-crown',
                'emoji': '👑'
            },
            {
                'name': 'Марафонец',
                'description': 'Проведите на сайте 30 минут за сеанс',
                'achievement_type': 'session_30min',
                'xp_reward': 50,
                'icon': 'fas fa-clock',
                'emoji': '⏱️'
            },
            {
                'name': 'Постоянный пользователь',
                'description': 'Посещайте сайт 7 дней подряд',
                'achievement_type': 'streak_7',
                'xp_reward': 150,
                'icon': 'fas fa-fire',
                'emoji': '🔥'
            },
        ]
        
        for ach_data in achievements_data:
            # Проверяем наличие достижения с таким типом
            existing = Achievement.objects.filter(achievement_type=ach_data['achievement_type'])
            
            if existing.count() > 1:
                for duplicate in existing[1:]:
                    duplicate.delete()
                achievement = existing.first()
                created = False
            elif existing.count() == 1:
                achievement = existing.first()
                created = False
            else:
                achievement = Achievement.objects.create(**ach_data)
                created = True
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Создано достижение: {achievement.name}"))
            else:
                self.stdout.write(f"  Достижение уже существует: {achievement.name}")
    
    def create_quizzes(self):
        self.stdout.write("\n5. Создание викторин...")
        
        # Викторина 1
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
            self.stdout.write(self.style.SUCCESS(f"[+] Создана викторина: {quiz1.title}"))
            
            questions_data = [
                {
                    'text': 'Какой элемент является самым легким в периодической таблице?',
                    'answers': [('Водород', True), ('Гелий', False), ('Литий', False), ('Углерод', False)],
                    'element': 'H'
                },
                {
                    'text': 'Какой газ составляет большую часть атмосферы Земли?',
                    'answers': [('Кислород', False), ('Азот', True), ('Углекислый газ', False), ('Водород', False)],
                    'element': 'N'
                },
                {
                    'text': 'Какой элемент необходим для дыхания?',
                    'answers': [('Водород', False), ('Азот', False), ('Кислород', True), ('Гелий', False)],
                    'element': 'O'
                },
                {
                    'text': 'Из какого элемента состоят алмазы?',
                    'answers': [('Кремний', False), ('Углерод', True), ('Кислород', False), ('Железо', False)],
                    'element': 'C'
                },
                {
                    'text': 'Какой металл используется в электрических проводах?',
                    'answers': [('Железо', False), ('Алюминий', False), ('Медь', True), ('Золото', False)],
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
            
            self.stdout.write(f"  + Добавлено {len(questions_data)} вопросов")
        else:
            self.stdout.write(f"  Викторина уже существует: {quiz1.title}")
        
        # Викторина 2: Периодическая таблица
        quiz2, created = Quiz.objects.get_or_create(
            title='Периодическая таблица',
            defaults={
                'description': 'Проверьте знание структуры таблицы Менделеева',
                'level': 2,
                'max_points': 60,
                'time_limit': 12
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"[+] Создана викторина: {quiz2.title}"))
            
            questions_data_2 = [
                {
                    'text': 'Сколько периодов в таблице Менделеева?',
                    'answers': [('5', False), ('6', False), ('7', True), ('8', False)],
                    'element': None
                },
                {
                    'text': 'К какой группе относится кислород?',
                    'answers': [('14 группа', False), ('15 группа', False), ('16 группа', True), ('17 группа', False)],
                    'element': 'O'
                },
                {
                    'text': 'Какой металл самый легкий?',
                    'answers': [('Натрий', False), ('Магний', False), ('Литий', True), ('Алюминий', False)],
                    'element': 'Li'
                },
                {
                    'text': 'Какой элемент имеет атомный номер 79?',
                    'answers': [('Серебро', False), ('Золото', True), ('Платина', False), ('Медь', False)],
                    'element': 'Au'
                },
                {
                    'text': 'Какие элементы называют благородными газами?',
                    'answers': [('Группа 1', False), ('Группа 17', False), ('Группа 18', True), ('Группа 2', False)],
                    'element': 'He'
                },
                {
                    'text': 'Какой элемент используется в аккумуляторах телефонов?',
                    'answers': [('Натрий', False), ('Литий', True), ('Калий', False), ('Магний', False)],
                    'element': 'Li'
                },
            ]
            
            for q_data in questions_data_2:
                element = None
                if q_data['element']:
                    try:
                        element = Element.objects.get(symbol=q_data['element'])
                    except Element.DoesNotExist:
                        pass
                
                question = QuizQuestion.objects.create(
                    quiz=quiz2,
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
            
            self.stdout.write(f"  + Добавлено {len(questions_data_2)} вопросов")
        else:
            self.stdout.write(f"  Викторина уже существует: {quiz2.title}")
        
        # Викторина 3: Химические реакции
        quiz3, created = Quiz.objects.get_or_create(
            title='Химические реакции',
            defaults={
                'description': 'Узнайте больше о химических превращениях',
                'level': 3,
                'max_points': 70,
                'time_limit': 15
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"[+] Создана викторина: {quiz3.title}"))
            
            questions_data_3 = [
                {
                    'text': 'Что образуется при горении водорода?',
                    'answers': [('Кислород', False), ('Вода', True), ('Водород', False), ('Углекислый газ', False)],
                    'element': 'H'
                },
                {
                    'text': 'Какой газ выделяется при реакции металлов с кислотой?',
                    'answers': [('Кислород', False), ('Азот', False), ('Водород', True), ('Углекислый газ', False)],
                    'element': 'H'
                },
                {
                    'text': 'Что происходит с железом при контакте с водой и кислородом?',
                    'answers': [('Плавится', False), ('Ржавеет', True), ('Испаряется', False), ('Кристаллизуется', False)],
                    'element': 'Fe'
                },
                {
                    'text': 'Какой цвет имеет пламя при горении магния?',
                    'answers': [('Красный', False), ('Синий', False), ('Ярко-белый', True), ('Желтый', False)],
                    'element': 'Mg'
                },
                {
                    'text': 'Что образуется при соединении натрия и хлора?',
                    'answers': [('Вода', False), ('Поваренная соль', True), ('Сахар', False), ('Сода', False)],
                    'element': 'Na'
                },
                {
                    'text': 'Какой процесс происходит в растениях на свету?',
                    'answers': [('Дыхание', False), ('Фотосинтез', True), ('Горение', False), ('Испарение', False)],
                    'element': 'O'
                },
                {
                    'text': 'Что выделяется при горении углерода?',
                    'answers': [('Вода', False), ('Углекислый газ', True), ('Кислород', False), ('Азот', False)],
                    'element': 'C'
                },
            ]
            
            for q_data in questions_data_3:
                element = None
                if q_data['element']:
                    try:
                        element = Element.objects.get(symbol=q_data['element'])
                    except Element.DoesNotExist:
                        pass
                
                question = QuizQuestion.objects.create(
                    quiz=quiz3,
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
            
            self.stdout.write(f"  + Добавлено {len(questions_data_3)} вопросов")
        else:
            self.stdout.write(f"  Викторина уже существует: {quiz3.title}")