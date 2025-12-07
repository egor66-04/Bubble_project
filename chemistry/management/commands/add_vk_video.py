from django.core.management.base import BaseCommand
from chemistry.models import Video


class Command(BaseCommand):
    help = 'Добавляет образовательные видео с VK Video'

    def handle(self, *args, **options):
        # Для получения embed кода VK Video:
        # 1. Откройте видео на VK
        # 2. Нажмите "Поделиться" -> "Встроить на сайт"
        # 3. Скопируйте предоставленный VK iframe код
        
        videos_data = [
            {
                'title': 'Фиксики - Все серии подряд (сборник 26)',
                'embed_code': '<iframe src="https://vkvideo.ru/video_ext.php?oid=-183506164&id=456239442&hash=ef9976b5b4c5fc7a&hd=3" width="1280" height="720" allow="autoplay; encrypted-media; fullscreen; picture-in-picture; screen-wake-lock;" frameborder="0" allowfullscreen></iframe>',
                'description': 'Образовательный мультсериал про маленьких человечков, которые живут внутри техники и чинят её.',
                'order': 1,
            },
        ]
        
        for video_data in videos_data:
            video, created = Video.objects.get_or_create(
                title=video_data['title'],
                defaults={
                    'embed_code': video_data['embed_code'],
                    'description': video_data.get('description', ''),
                    'order': video_data.get('order', 0),
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Добавлено видео: {video.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Видео уже существует: {video.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nВсего видео в базе: {Video.objects.count()}')
        )