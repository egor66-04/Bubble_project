/**
 * Bubble TTS (Text-to-Speech) Module
 * Озвучивание элементов страницы с возможностью переключения и сохранения состояния
 */
(function() {
    // Состояние озвучивания
    const ttsState = {
        enabled: false,
        speaking: false,
        currentElement: null,
        synth: window.speechSynthesis,
        voice: null,
        lang: 'ru-RU'
    };

    // DOM элементы
    const ttsToggleBtn = document.getElementById('tts-toggle');
    
    // Инициализация
    function init() {
        if (!ttsState.synth) {
            console.error('Browser does not support speech synthesis');
            if (ttsToggleBtn) {
                ttsToggleBtn.style.display = 'none';
            }
            return;
        }
        
        // Загружаем сохраненное состояние
        loadState();
        
        // Обновляем активное состояние кнопки
        updateButtonState();
        
        // Добавляем обработчики событий
        setupEventListeners();
        
        // Получаем доступные голоса
        loadVoices();
    }
    
    // Получение доступных голосов
    function loadVoices() {
        // Для Chrome голоса могут быть загружены не сразу
        let voices = ttsState.synth.getVoices();
        
        if (voices.length === 0) {
            ttsState.synth.addEventListener('voiceschanged', () => {
                voices = ttsState.synth.getVoices();
                selectRussianVoice(voices);
            });
        } else {
            selectRussianVoice(voices);
        }
    }
    
    // Выбор русского голоса
    function selectRussianVoice(voices) {
        // Ищем русский голос
        const russianVoice = voices.find(voice => 
            voice.lang.includes('ru-RU') || voice.lang.includes('ru')
        );
        
        // Если русский голос не найден, пытаемся использовать дефолтный
        ttsState.voice = russianVoice || voices.find(voice => voice.default) || voices[0];
        
        console.log('Selected TTS voice:', ttsState.voice ? ttsState.voice.name : 'None available');
    }
    
    // Настройка обработчиков событий
    function setupEventListeners() {
        // Переключение состояния озвучивания
        if (ttsToggleBtn) {
            ttsToggleBtn.addEventListener('click', toggleTTS);
        }
        
        // Озвучивание при наведении
        document.addEventListener('mouseover', handleElementHover);
        
        // Остановка озвучивания при уходе курсора
        document.addEventListener('mouseout', handleElementLeave);
        
        // Остановка озвучивания при прокрутке
        document.addEventListener('scroll', () => {
            if (ttsState.speaking) {
                ttsState.synth.cancel();
                ttsState.speaking = false;
                if (ttsState.currentElement) {
                    ttsState.currentElement.classList.remove('tts-highlight');
                    ttsState.currentElement = null;
                }
            }
        }, { passive: true });
    }
    
    // Обработка наведения на элемент
    function handleElementHover(event) {
        if (!ttsState.enabled || ttsState.speaking) return;
        
        const element = event.target;
        
        // Получаем текст для озвучивания
        const textToSpeak = getElementText(element);
        
        // Если текст есть, озвучиваем его
        if (textToSpeak && textToSpeak.trim().length > 1) {
            ttsState.currentElement = element;
            element.classList.add('tts-highlight');
            speakText(textToSpeak);
        }
    }
    
    // Обработка ухода курсора с элемента
    function handleElementLeave(event) {
        if (!ttsState.enabled || !ttsState.speaking) return;
        
        const element = event.target;
        
        // Если это активный элемент, останавливаем речь
        if (element === ttsState.currentElement) {
            ttsState.synth.cancel();
            ttsState.speaking = false;
            element.classList.remove('tts-highlight');
            ttsState.currentElement = null;
        }
    }
    
    // Получение текста элемента для озвучивания
    function getElementText(element) {
        // Если это инпут или текстовая область, берем значение или плейсхолдер
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            return element.value || element.placeholder || '';
        }
        
        // Если это кнопка, ссылка или элемент с атрибутом aria-label
        if (element.getAttribute('aria-label')) {
            return element.getAttribute('aria-label');
        }
        
        // Для элементов с alt текстом (изображения)
        if (element.alt) {
            return element.alt;
        }
        
        // Если это интерактивный элемент (кнопка, ссылка), берем его текст
        if (element.tagName === 'BUTTON' || element.tagName === 'A' || 
            element.tagName === 'LABEL' || element.role === 'button') {
            return element.textContent || '';
        }
        
        // Для заголовков и параграфов
        if (['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'LI', 'TH', 'TD', 'SPAN'].includes(element.tagName)) {
            return element.textContent || '';
        }
        
        // Для карточек элементов периодической таблицы
        if (element.classList.contains('element-card') || 
            element.classList.contains('element-inner') ||
            element.classList.contains('element-card-result') ||
            element.classList.contains('element-card-result-header')) {
            const symbol = element.querySelector('.element-symbol');
            const name = element.querySelector('.element-name');
            if (symbol && name) {
                return `Элемент ${name.textContent}, символ ${symbol.textContent}`;
            }
        }
        
        // Для других интерактивных элементов, которые могут иметь текст
        if (element.textContent && element.textContent.trim().length < 150 && 
            (element.onclick || element.role || 
             element.classList.contains('btn') || 
             element.classList.contains('card') ||
             element.classList.contains('bubble-card'))) {
            return element.textContent || '';
        }
        
        return null;
    }
    
    // Озвучивание текста
    function speakText(text) {
        if (!ttsState.enabled || !ttsState.synth) return;
        
        // Останавливаем предыдущее озвучивание
        ttsState.synth.cancel();
        
        // Создаем новый экземпляр речи
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Устанавливаем голос и язык
        utterance.voice = ttsState.voice;
        utterance.lang = ttsState.lang;
        utterance.rate = 1.0;  // Скорость речи
        utterance.pitch = 1.0; // Высота голоса
        
        // Обработчики событий
        utterance.onstart = () => {
            ttsState.speaking = true;
        };
        
        utterance.onend = () => {
            ttsState.speaking = false;
            if (ttsState.currentElement) {
                ttsState.currentElement.classList.remove('tts-highlight');
                ttsState.currentElement = null;
            }
        };
        
        utterance.onerror = (event) => {
            console.error('TTS Error:', event);
            ttsState.speaking = false;
            if (ttsState.currentElement) {
                ttsState.currentElement.classList.remove('tts-highlight');
                ttsState.currentElement = null;
            }
        };
        
        // Запускаем озвучивание
        ttsState.synth.speak(utterance);
    }
    
    // Переключение состояния озвучивания
    function toggleTTS() {
        ttsState.enabled = !ttsState.enabled;
        
        // Сохраняем состояние
        saveState();
        
        // Обновляем отображение кнопки
        updateButtonState();
        
        // Оповещаем пользователя
        notifyUser();
    }
    
    // Обновление состояния кнопки
    function updateButtonState() {
        if (!ttsToggleBtn) return;
        
        if (ttsState.enabled) {
            ttsToggleBtn.classList.add('active');
            ttsToggleBtn.setAttribute('aria-pressed', 'true');
            ttsToggleBtn.querySelector('i').className = 'fas fa-volume-up';
        } else {
            ttsToggleBtn.classList.remove('active');
            ttsToggleBtn.setAttribute('aria-pressed', 'false');
            ttsToggleBtn.querySelector('i').className = 'fas fa-volume-mute';
        }
    }
    
    // Оповещение пользователя о включении/выключении озвучивания
    function notifyUser() {
        if (ttsState.enabled) {
            speakText('Озвучивание включено');
        } else {
            // Останавливаем текущее озвучивание
            ttsState.synth.cancel();
            ttsState.speaking = false;
            
            if (ttsState.currentElement) {
                ttsState.currentElement.classList.remove('tts-highlight');
                ttsState.currentElement = null;
            }
        }
    }
    
    // Сохранение состояния в localStorage
    function saveState() {
        localStorage.setItem('bubbleTtsEnabled', ttsState.enabled.toString());
    }
    
    // Загрузка состояния из localStorage
    function loadState() {
        const savedState = localStorage.getItem('bubbleTtsEnabled');
        if (savedState !== null) {
            ttsState.enabled = savedState === 'true';
        }
    }
    
    // Инициализация при загрузке страницы
    document.addEventListener('DOMContentLoaded', init);
})();

// Добавляем стили для подсветки озвучиваемых элементов
(function() {
    const style = document.createElement('style');
    style.textContent = `
        .tts-highlight {
            outline: 2px solid var(--bubble-primary, #3498db) !important;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.5) !important;
            position: relative;
            z-index: 1;
        }
    `;
    document.head.appendChild(style);
})(); 