(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Инициализация всплывающих подсказок
        $('[data-toggle="tooltip"]').tooltip();
        
        // Функция предварительного просмотра аватара перед загрузкой
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                
                reader.onload = function(e) {
                    var preview = $('<img>').attr({
                        'src': e.target.result,
                        'class': 'avatar-preview',
                        'style': 'max-width: 80px; max-height: 80px; margin-top: 10px; border-radius: 50%; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
                    });
                    
                    // Удаляем предыдущий предпросмотр, если он существует
                    $('.avatar-preview').remove();
                    
                    // Добавляем новый предпросмотр
                    $(input).after(preview);
                };
                
                reader.readAsDataURL(input.files[0]);
            }
        }
        
        // Применяем функцию предпросмотра к загрузке аватара
        $('input[type="file"][name="avatar"]').change(function() {
            readURL(this);
        });
        
        // Подсветка строк таблицы при наведении
        $('.app-accounts.model-user .results table tbody tr, .app-accounts.model-achievement .results table tbody tr').hover(
            function() {
                $(this).addClass('highlight-row');
            },
            function() {
                $(this).removeClass('highlight-row');
            }
        );
        
        // Динамический расчет уровня на основе XP
        $('input[name="xp_points"]').on('change keyup', function() {
            var xp = parseInt($(this).val()) || 0;
            var level = Math.floor(Math.sqrt(xp / 100));
            
            // Обновляем поле уровня
            $('input[name="level"]').val(level);
        });
        
        // Добавляем кнопку для быстрого сохранения формы пользователя
        if ($('.submit-row').length && $('.app-accounts.model-user').length) {
            var quickSaveBtn = $('<input>').attr({
                'type': 'submit',
                'value': 'Быстрое сохранение',
                'name': '_continue',
                'class': 'default',
                'style': 'margin-right: 10px; background-color: #35847d;'
            });
            
            $('.submit-row').prepend(quickSaveBtn);
        }
        
        // Добавляем поиск по выпадающим спискам
        $('.app-accounts select[size="1"]').each(function() {
            $(this).attr('data-live-search', 'true');
            
            // Пытаемся инициализировать bootstrap-select если он доступен
            if (typeof $.fn.selectpicker !== 'undefined') {
                $(this).selectpicker({
                    liveSearch: true,
                    liveSearchPlaceholder: 'Поиск...',
                    size: 10
                });
            }
        });
        
        // Улучшенное отображение достижений в админке
        function addAchievementIcons() {
            $('.field-icon_display').each(function() {
                var iconClass = $(this).text().trim();
                if (iconClass && !iconClass.startsWith('-')) {
                    // Находим иконку и заменяем текст на визуальное представление
                    var iconDisplay = $('<i>').addClass(iconClass).css({
                        'font-size': '1.5em',
                        'margin-right': '10px'
                    });
                    $(this).html(iconDisplay).append(iconClass);
                }
            });
        }
        
        // Вызываем функцию добавления иконок при загрузке страницы
        addAchievementIcons();
        
        // Улучшенное отображение эмодзи в админке
        function enhanceEmojiDisplay() {
            $('.field-emoji').each(function() {
                var emoji = $(this).text().trim();
                if (emoji && emoji !== '-') {
                    $(this).css({
                        'font-size': '1.5em',
                        'text-align': 'center'
                    });
                }
            });
        }
        
        // Вызываем функцию улучшения отображения эмодзи
        enhanceEmojiDisplay();
        
        // Добавляем стили для подсветки строк
        $('<style>')
            .prop('type', 'text/css')
            .html(`
                .highlight-row {
                    background-color: rgba(53, 132, 125, 0.1) !important;
                }
                .app-accounts .results table tbody tr:hover {
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .field-level_badge, .field-achievement_type_badge, .field-subscription_status {
                    text-align: center;
                }
            `)
            .appendTo('head');
    });
})(django.jQuery); 