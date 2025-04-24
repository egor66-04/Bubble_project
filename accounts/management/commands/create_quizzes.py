from django.core.management.base import BaseCommand
from accounts.models import Quiz, QuizQuestion, QuizAnswer
from chemistry.models import Element

class Command(BaseCommand):
    help = 'Создает викторины и тесты для проекта'

    def handle(self, *args, **options):
        # Удаляем старые викторины
        Quiz.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Старые викторины удалены'))

        # Получаем элементы для связывания с вопросами
        try:
            h = Element.objects.get(symbol='H')
            o = Element.objects.get(symbol='O')
            c = Element.objects.get(symbol='C')
            na = Element.objects.get(symbol='Na')
            fe = Element.objects.get(symbol='Fe')
            he = Element.objects.get(symbol='He')
        except Element.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не все необходимые элементы существуют в базе данных'))
            return

        # Создаем викторины
        q1 = Quiz.objects.create(
            title='Основы химических элементов',
            description='Базовые вопросы по основным химическим элементам',
            level=1,
            is_active=True
        )

        q2 = Quiz.objects.create(
            title='Металлы и их свойства',
            description='Тест на знание металлов и их характеристик',
            level=2,
            is_active=True
        )

        q3 = Quiz.objects.create(
            title='Неметаллы и их свойства',
            description='Вопросы о неметаллах и их особенностях',
            level=2,
            is_active=True
        )

        q4 = Quiz.objects.create(
            title='Химические реакции: основы',
            description='Базовые знания о химических реакциях',
            level=3,
            is_active=True
        )

        q5 = Quiz.objects.create(
            title='Продвинутая химия',
            description='Сложные вопросы для настоящих химиков!',
            level=5,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Викторины созданы'))

        # Создаем вопросы и ответы для первой викторины
        # Викторина 1: Основы химических элементов
        q1_1 = QuizQuestion.objects.create(
            quiz=q1,
            question_text='Что такое атомный номер элемента?',
            related_element=None,
            points=2
        )
        
        QuizAnswer.objects.create(question=q1_1, answer_text='Количество протонов в ядре атома', is_correct=True)
        QuizAnswer.objects.create(question=q1_1, answer_text='Количество нейтронов в ядре атома', is_correct=False)
        QuizAnswer.objects.create(question=q1_1, answer_text='Сумма протонов и нейтронов в ядре атома', is_correct=False)
        QuizAnswer.objects.create(question=q1_1, answer_text='Количество электронов в атоме', is_correct=False)

        q1_2 = QuizQuestion.objects.create(
            quiz=q1,
            question_text='Какой химический символ у водорода?',
            related_element=h,
            points=1
        )
        
        QuizAnswer.objects.create(question=q1_2, answer_text='H', is_correct=True)
        QuizAnswer.objects.create(question=q1_2, answer_text='Hy', is_correct=False)
        QuizAnswer.objects.create(question=q1_2, answer_text='W', is_correct=False)
        QuizAnswer.objects.create(question=q1_2, answer_text='Hd', is_correct=False)

        q1_3 = QuizQuestion.objects.create(
            quiz=q1,
            question_text='Какой элемент имеет атомный номер 8?',
            related_element=o,
            points=1
        )
        
        QuizAnswer.objects.create(question=q1_3, answer_text='Кислород', is_correct=True)
        QuizAnswer.objects.create(question=q1_3, answer_text='Азот', is_correct=False)
        QuizAnswer.objects.create(question=q1_3, answer_text='Углерод', is_correct=False)
        QuizAnswer.objects.create(question=q1_3, answer_text='Фтор', is_correct=False)

        # Викторина 2: Металлы и их свойства
        q2_1 = QuizQuestion.objects.create(
            quiz=q2,
            question_text='Какой из этих элементов является металлом?',
            related_element=None,
            points=1
        )
        
        QuizAnswer.objects.create(question=q2_1, answer_text='Натрий', is_correct=True)
        QuizAnswer.objects.create(question=q2_1, answer_text='Хлор', is_correct=False)
        QuizAnswer.objects.create(question=q2_1, answer_text='Кислород', is_correct=False)
        QuizAnswer.objects.create(question=q2_1, answer_text='Азот', is_correct=False)

        q2_2 = QuizQuestion.objects.create(
            quiz=q2,
            question_text='Какое свойство наиболее характерно для металлов?',
            related_element=None,
            points=2
        )
        
        QuizAnswer.objects.create(question=q2_2, answer_text='Электропроводность', is_correct=True)
        QuizAnswer.objects.create(question=q2_2, answer_text='Хрупкость', is_correct=False)
        QuizAnswer.objects.create(question=q2_2, answer_text='Низкая плотность', is_correct=False)
        QuizAnswer.objects.create(question=q2_2, answer_text='Газообразное состояние при комнатной температуре', is_correct=False)

        # Викторина 3: Неметаллы и их свойства
        q3_1 = QuizQuestion.objects.create(
            quiz=q3,
            question_text='Какой из этих элементов является неметаллом?',
            related_element=None,
            points=1
        )
        
        QuizAnswer.objects.create(question=q3_1, answer_text='Кислород', is_correct=True)
        QuizAnswer.objects.create(question=q3_1, answer_text='Железо', is_correct=False)
        QuizAnswer.objects.create(question=q3_1, answer_text='Натрий', is_correct=False)
        QuizAnswer.objects.create(question=q3_1, answer_text='Кальций', is_correct=False)

        q3_2 = QuizQuestion.objects.create(
            quiz=q3,
            question_text='Что из перечисленного НЕ является свойством неметаллов?',
            related_element=None,
            points=2
        )
        
        QuizAnswer.objects.create(question=q3_2, answer_text='Пластичность', is_correct=True)
        QuizAnswer.objects.create(question=q3_2, answer_text='Хрупкость', is_correct=False)
        QuizAnswer.objects.create(question=q3_2, answer_text='Низкая теплопроводность', is_correct=False)
        QuizAnswer.objects.create(question=q3_2, answer_text='Способность образовывать анионы', is_correct=False)

        # Викторина 4: Химические реакции: основы
        q4_1 = QuizQuestion.objects.create(
            quiz=q4,
            question_text='Какая формула представляет реакцию образования воды?',
            related_element=None,
            points=2
        )
        
        QuizAnswer.objects.create(question=q4_1, answer_text='2H₂ + O₂ → 2H₂O', is_correct=True)
        QuizAnswer.objects.create(question=q4_1, answer_text='H₂ + O → H₂O', is_correct=False)
        QuizAnswer.objects.create(question=q4_1, answer_text='H + O₂ → HO₂', is_correct=False)
        QuizAnswer.objects.create(question=q4_1, answer_text='2H + O → H₂O', is_correct=False)

        q4_2 = QuizQuestion.objects.create(
            quiz=q4,
            question_text='Что происходит при реакции горения углерода?',
            related_element=c,
            points=2
        )
        
        QuizAnswer.objects.create(question=q4_2, answer_text='Образуется углекислый газ и выделяется энергия', is_correct=True)
        QuizAnswer.objects.create(question=q4_2, answer_text='Образуется вода и углекислый газ', is_correct=False)
        QuizAnswer.objects.create(question=q4_2, answer_text='Образуется угарный газ и поглощается энергия', is_correct=False)
        QuizAnswer.objects.create(question=q4_2, answer_text='Углерод разлагается на более простые элементы', is_correct=False)

        # Викторина 5: Продвинутая химия
        q5_1 = QuizQuestion.objects.create(
            quiz=q5,
            question_text='Какой тип гибридизации характерен для атома углерода в молекуле метана (CH₄)?',
            related_element=c,
            points=3
        )
        
        QuizAnswer.objects.create(question=q5_1, answer_text='sp³', is_correct=True)
        QuizAnswer.objects.create(question=q5_1, answer_text='sp²', is_correct=False)
        QuizAnswer.objects.create(question=q5_1, answer_text='sp', is_correct=False)
        QuizAnswer.objects.create(question=q5_1, answer_text='dsp³', is_correct=False)

        q5_2 = QuizQuestion.objects.create(
            quiz=q5,
            question_text='Какое свойство делает благородные газы такими химически инертными?',
            related_element=he,
            points=3
        )
        
        QuizAnswer.objects.create(question=q5_2, answer_text='Полностью заполненные внешние электронные оболочки', is_correct=True)
        QuizAnswer.objects.create(question=q5_2, answer_text='Высокая электроотрицательность', is_correct=False)
        QuizAnswer.objects.create(question=q5_2, answer_text='Низкая электроотрицательность', is_correct=False)
        QuizAnswer.objects.create(question=q5_2, answer_text='Высокая энергия ионизации', is_correct=False)

        self.stdout.write(self.style.SUCCESS('Вопросы и ответы для викторин созданы')) 