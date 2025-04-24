(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Инициализация всплывающих подсказок
        $('[data-toggle="tooltip"]').tooltip();
        
        // Функция предварительного просмотра изображения реакции перед загрузкой
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                
                reader.onload = function(e) {
                    var preview = $('<img>').attr({
                        'src': e.target.result,
                        'class': 'reaction-image-preview',
                        'style': 'max-width: 200px; max-height: 150px; margin-top: 10px; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
                    });
                    
                    // Удаляем предыдущий предпросмотр, если он существует
                    $('.reaction-image-preview').remove();
                    
                    // Добавляем новый предпросмотр
                    $(input).after(preview);
                };
                
                reader.readAsDataURL(input.files[0]);
            }
        }
        
        // Применяем функцию предпросмотра к загрузке изображения
        $('input[type="file"][name$="image"]').change(function() {
            readURL(this);
        });
        
        // Подсветка строк таблицы при наведении
        $('.app-chemistry.model-chemicalreaction .results table tbody tr').hover(
            function() {
                $(this).addClass('highlight-row');
            },
            function() {
                $(this).removeClass('highlight-row');
            }
        );
        
        // Функция для форматирования формулы реакции
        function formatReactionFormula() {
            var formulaInput = $('input[name="reaction_formula"]');
            var formula = formulaInput.val();
            
            // Если есть стрелка, форматируем формулу
            if (formula.includes('->') || formula.includes('→')) {
                // Заменяем простую стрелку на красивую
                formula = formula.replace('->', '→');
                
                // Добавляем пробелы вокруг плюсов и стрелки если их нет
                formula = formula.replace(/\+/g, ' + ').replace(/\s+\+\s+/g, ' + ');
                formula = formula.replace(/→/g, ' → ').replace(/\s+→\s+/g, ' → ');
                
                // Убираем повторяющиеся пробелы
                formula = formula.replace(/\s+/g, ' ').trim();
                
                // Обновляем значение в поле
                formulaInput.val(formula);
                
                // Добавляем визуальное оформление
                var formattedDisplay = $('<div>')
                    .addClass('formatted-reaction')
                    .html(
                        formula.replace(/→/g, '<span style="color: #fd7e14; font-weight: bold;">→</span>')
                              .replace(/\+/g, '<span style="color: #35847d;">+</span>')
                    )
                    .css({
                        'font-family': 'monospace',
                        'font-size': '16px',
                        'margin-top': '10px',
                        'padding': '8px 12px',
                        'background-color': '#f8f9fa',
                        'border-radius': '5px',
                        'border-left': '4px solid #4a6fa5'
                    });
                
                // Удаляем предыдущую версию
                $('.formatted-reaction').remove();
                
                // Добавляем отформатированное отображение
                formulaInput.after(formattedDisplay);
            }
        }
        
        // Вызываем форматирование при загрузке страницы и при изменении
        $('input[name="reaction_formula"]').on('change keyup', formatReactionFormula);
        setTimeout(formatReactionFormula, 500); // Задержка для работы на загрузке формы
        
        // Улучшение интерфейса для выбора элементов
        function enhanceElementSelectors() {
            // Добавляем кнопки для быстрого переключения между реагентами и продуктами
            if ($('.field-reactants').length && $('.field-products').length) {
                var switchButton = $('<button>')
                    .attr({
                        'type': 'button',
                        'class': 'button',
                        'style': 'margin: 10px 0; background-color: #4a6fa5; color: white;'
                    })
                    .text('Переключить на продукты')
                    .click(function(e) {
                        e.preventDefault();
                        
                        // Переключаем видимость между реагентами и продуктами
                        if ($(this).text() === 'Переключить на продукты') {
                            $('.field-reactants').hide();
                            $('.field-products').show();
                            $(this).text('Переключить на реагенты');
                        } else {
                            $('.field-reactants').show();
                            $('.field-products').hide();
                            $(this).text('Переключить на продукты');
                        }
                    });
                
                // Добавляем кнопку после первого блока
                $('.field-reactants').after(switchButton);
                
                // Скрываем блок продуктов по умолчанию для упрощения интерфейса
                $('.field-products').hide();
            }
        }
        
        // Вызываем функцию улучшения селекторов элементов
        setTimeout(enhanceElementSelectors, 500);
        
        // Добавляем кнопку для быстрого сохранения формы
        if ($('.submit-row').length) {
            var quickSaveBtn = $('<input>').attr({
                'type': 'submit',
                'value': 'Быстрое сохранение',
                'name': '_continue',
                'class': 'default',
                'style': 'margin-right: 10px; background-color: #4a6fa5;'
            });
            
            $('.submit-row').prepend(quickSaveBtn);
        }
        
        // Добавляем стили для подсветки строк и других элементов интерфейса
        $('<style>')
            .prop('type', 'text/css')
            .html(`
                .highlight-row {
                    background-color: rgba(74, 111, 165, 0.1) !important;
                }
                .app-chemistry.model-chemicalreaction .results table tbody tr:hover {
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .field-get_reactants, .field-get_products {
                    text-align: center;
                    font-family: monospace;
                }
                label[for="id_video"], label[for="id_image"] {
                    font-weight: 600;
                    margin-top: 15px;
                    display: block;
                }
            `)
            .appendTo('head');
    });
})(django.jQuery); 