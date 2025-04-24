(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Инициализация всплывающих подсказок
        $('[data-toggle="tooltip"]').tooltip();
        
        // Функция предварительного просмотра изображения перед загрузкой
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                
                reader.onload = function(e) {
                    var preview = $('<img>').attr({
                        'src': e.target.result,
                        'class': 'element-image-preview',
                        'style': 'max-width: 100px; max-height: 100px; margin-top: 10px; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
                    });
                    
                    // Удаляем предыдущий предпросмотр, если он существует
                    $('.element-image-preview').remove();
                    
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
        $('.app-chemistry.model-element .results table tbody tr').hover(
            function() {
                $(this).addClass('highlight-row');
            },
            function() {
                $(this).removeClass('highlight-row');
            }
        );
        
        // Улучшение взаимодействия с категориями элементов
        $('select[name="category"]').on('change', function() {
            var selectedOption = $(this).find('option:selected');
            var categoryColor = selectedOption.data('color') || '#cccccc';
            
            // Изменяем цвет границы выбранной категории
            $(this).css('border-left', '4px solid ' + categoryColor);
        });
        
        // Динамическое обновление формулы реакции
        function updateReactionFormula() {
            var reactants = [];
            var products = [];
            
            // Собираем реагенты
            $('.field-reactants select option:selected').each(function() {
                reactants.push($(this).text().split(' ')[0]); // Берем только символ элемента
            });
            
            // Собираем продукты
            $('.field-products select option:selected').each(function() {
                products.push($(this).text().split(' ')[0]); // Берем только символ элемента
            });
            
            // Формируем формулу реакции
            var formula = reactants.join(' + ') + ' → ' + products.join(' + ');
            
            // Обновляем поле формулы реакции если оно пустое
            var formulaInput = $('input[name="reaction_formula"]');
            if (formulaInput.val() === '') {
                formulaInput.val(formula);
            }
        }
        
        // Обновляем формулу при изменении реагентов или продуктов
        $('.field-reactants select, .field-products select').on('change', updateReactionFormula);
        
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
        
        // Добавляем стили для подсветки строк
        $('<style>')
            .prop('type', 'text/css')
            .html(`
                .highlight-row {
                    background-color: rgba(74, 111, 165, 0.1) !important;
                }
                .app-chemistry.model-element .results table tbody tr:hover {
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
            `)
            .appendTo('head');
    });
})(django.jQuery); 