/**
 * Bubble - Основной JavaScript файл
 */

// Утилиты
const Utils = {
    /**
     * Debounce функция для оптимизации частых вызовов
     * @param {Function} func - Функция для вызова
     * @param {number} wait - Время ожидания в мс
     * @returns {Function}
     */
    debounce(func, wait = 300) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Throttle функция для ограничения частоты вызовов
     * @param {Function} func - Функция для вызова
     * @param {number} limit - Минимальный интервал между вызовами в мс
     * @returns {Function}
     */
    throttle(func, limit = 100) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Инициализация всплывающих окон Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Инициализация поиска с debounce
    setupSearchWithDebounce();
    
    // Обработка добавления в избранное через AJAX
    setupFavorites();
    
    // Обработка интерактивной таблицы Менделеева
    setupPeriodicTable();
    
    // Обработка соединения элементов для реакций
    setupReactions();
    
    // Добавляем стили для уведомлений о достижениях
    addAchievementStyles();
    
    // Проверяем новые достижения для авторизованных пользователей
    const isAuthenticated = document.body.classList.contains('user-authenticated');
    if (isAuthenticated) {
        // Проверяем новые достижения сразу при загрузке страницы
        checkNewAchievements();
        setInterval(checkNewAchievements, 60000);
    }

    // === NEW UX IMPROVEMENTS ===
    initPageLoader();
    initToastSystem();
    initScrollTop();
    initFormSpinners();
    initSearchValidation();
    initLazyImages();
});

// ================================
// PAGE LOADER
// ================================
function initPageLoader() {
    const loader = document.getElementById('page-loader');
    if (!loader) return;

    // Показываем loader при переходе по ссылкам
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;
        if (link.target === '_blank') return;
        if (link.href && link.href.startsWith(window.location.origin) && !link.href.includes('#')) {
            loader.classList.add('loading');
        }
    });

    // Скрываем когда страница загружена
    window.addEventListener('pageshow', function() {
        loader.classList.remove('loading');
        loader.classList.add('done');
        setTimeout(() => {
            loader.classList.remove('done');
            loader.style.width = '';
        }, 600);
    });
}

// ================================
// TOAST SYSTEM
// ================================
const ToastManager = {
    icons: {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle',
        debug: 'fas fa-bug'
    },
    titles: {
        success: 'Успешно',
        error: 'Ошибка',
        warning: 'Внимание',
        info: 'Информация',
        debug: 'Debug'
    },

    show(message, type = 'info', duration = 4000) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const normalizedType = this._normalizeType(type);
        const toast = document.createElement('div');
        toast.className = `bubble-toast toast-${normalizedType}`;

        toast.innerHTML = `
            <div class="bubble-toast-icon">
                <i class="${this.icons[normalizedType] || this.icons.info}"></i>
            </div>
            <div class="bubble-toast-body">
                <div class="bubble-toast-title">${this.titles[normalizedType] || 'Уведомление'}</div>
                <p class="bubble-toast-message">${message}</p>
            </div>
            <button class="bubble-toast-close" aria-label="Закрыть"><i class="fas fa-times"></i></button>
            <div class="bubble-toast-progress" style="animation-duration: ${duration}ms"></div>
        `;

        container.appendChild(toast);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => toast.classList.add('show'));
        });

        const close = () => {
            toast.classList.add('hide');
            setTimeout(() => toast.remove(), 400);
        };

        toast.querySelector('.bubble-toast-close').addEventListener('click', close);
        setTimeout(close, duration);
    },

    _normalizeType(type) {
        if (!type) return 'info';
        if (type.includes('success')) return 'success';
        if (type.includes('error') || type.includes('danger')) return 'error';
        if (type.includes('warning')) return 'warning';
        return 'info';
    }
};

function initToastSystem() {
    // Показываем Django messages как toasts
    const messagesContainer = document.getElementById('django-messages');
    if (messagesContainer) {
        const spans = messagesContainer.querySelectorAll('span[data-msg-type]');
        spans.forEach((span, index) => {
            setTimeout(() => {
                ToastManager.show(span.dataset.msgText, span.dataset.msgType);
            }, index * 200);
        });
    }
}

// Глобальный доступ
window.BubbleToast = ToastManager;

// ================================
// SCROLL TO TOP
// ================================
function initScrollTop() {
    const btn = document.getElementById('scroll-top-btn');
    if (!btn) return;

    const onScroll = Utils.throttle(() => {
        btn.classList.toggle('visible', window.scrollY > 300);
    }, 100);

    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ================================
// FORM SPINNERS + DOUBLE SUBMIT PROTECTION
// ================================
function initFormSpinners() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('[type="submit"]');
            if (!submitBtn || submitBtn.classList.contains('btn-loading')) return;

            // Wrap text in span for hiding during loading
            if (!submitBtn.querySelector('.btn-text')) {
                submitBtn.innerHTML = `<span class="btn-text">${submitBtn.innerHTML}</span>`;
            }
            submitBtn.classList.add('btn-loading');
            submitBtn.disabled = true;

            // Safety timeout — разблокировать через 10с
            setTimeout(() => {
                submitBtn.classList.remove('btn-loading');
                submitBtn.disabled = false;
            }, 10000);
        });
    });
}

// ================================
// SEARCH VALIDATION
// ================================
function initSearchValidation() {
    document.querySelectorAll('form[action*="search"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const input = this.querySelector('input[name="q"]');
            if (input && input.value.trim() === '') {
                e.preventDefault();
                input.focus();
                input.classList.add('is-invalid');
                setTimeout(() => input.classList.remove('is-invalid'), 2000);
            }
        });
    });
}

// ================================
// LAZY IMAGE LOAD
// ================================
function initLazyImages() {
    if (!('IntersectionObserver' in window)) {
        // Fallback: mark all as loaded
        document.querySelectorAll('img[loading="lazy"]').forEach(img => img.classList.add('loaded'));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('loaded');
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '50px' });

    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', () => img.classList.add('loaded'));
            observer.observe(img);
        }
    });
}


/**
 * Настраивает функционал добавления элементов в избранное
 */
function setupFavorites() {
    // Обработка кнопок избранного на странице списка элементов
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const elementId = this.getAttribute('data-element-id');
            const isFavorite = this.classList.contains('is-favorite');
            const url = isFavorite 
                ? `/accounts/favorites/remove/${elementId}/`
                : `/accounts/favorites/add/${elementId}/`;
            
            // AJAX запрос для добавления/удаления из избранного
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                if (data.status === 'success') {
                    // Обновляем внешний вид кнопки
                    this.classList.toggle('is-favorite');
                    
                    const icon = this.querySelector('i');
                    if (isFavorite) {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.setAttribute('title', 'Добавить в избранное');
                    } else {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        this.setAttribute('title', 'Удалить из избранного');
                    }
                    
                    // Если есть Tooltip, обновляем его
                    const tooltip = bootstrap.Tooltip.getInstance(this);
                    if (tooltip) {
                        tooltip.dispose();
                        new bootstrap.Tooltip(this);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Обработка кнопок toggle-favorite на странице деталей элемента
    const toggleFavoriteButtons = document.querySelectorAll('.toggle-favorite');
    
    toggleFavoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const elementId = this.getAttribute('data-element-id');
            const isFavorite = this.getAttribute('data-is-favorite') === 'true';
            
            // AJAX запрос для добавления/удаления из избранного
            fetch('/chemistry/api/toggle-favorite-element/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    element_id: elementId
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                if (data.status === 'success') {
                    // Обновляем состояние и текст кнопки
                    if (isFavorite) {
                        this.innerHTML = '<i class="far fa-star me-1"></i> Добавить в избранное';
                        this.classList.remove('bubble-btn');
                        this.classList.add('bubble-btn-outline');
                        this.setAttribute('data-is-favorite', 'false');
                    } else {
                        this.innerHTML = '<i class="fas fa-star me-1"></i> Удалить из избранного';
                        this.classList.remove('bubble-btn-outline');
                        this.classList.add('bubble-btn');
                        this.setAttribute('data-is-favorite', 'true');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
}

/**
 * Настраивает интерактивность таблицы Менделеева
 */
function setupPeriodicTable() {
    const periodicTable = document.querySelector('.periodic-table-container');
    if (!periodicTable) return;
    
    // Фильтрация элементов по категории
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Снимаем активный класс со всех фильтров
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            const categoryId = this.getAttribute('data-category-id');
            
            // Показываем/скрываем элементы в соответствии с фильтром
            const elements = periodicTable.querySelectorAll('.periodic-element');
            
            if (categoryId === 'all') {
                // Показываем все элементы
                elements.forEach(element => {
                    element.classList.remove('filtered-out');
                });
            } else {
                // Показываем только элементы выбранной категории
                elements.forEach(element => {
                    const elementCategoryId = element.getAttribute('data-category-id');
                    if (elementCategoryId === categoryId) {
                        element.classList.remove('filtered-out');
                    } else {
                        element.classList.add('filtered-out');
                    }
                });
            }
        });
    });
    
    // Обработка клика по элементу
    const elements = periodicTable.querySelectorAll('.periodic-element');
    elements.forEach(element => {
        element.addEventListener('click', function() {
            const atomicNumber = this.getAttribute('data-atomic-number');
            if (atomicNumber) {
                window.location.href = `/chemistry/elements/${atomicNumber}/`;
            }
        });
    });
}

/**
 * Настраивает функционал для соединения элементов и проверки реакций
 */
function setupReactions() {
    const reactionArea = document.querySelector('.reaction-area');
    if (!reactionArea) return;
    
    let selectedElements = [];
    const maxSelectedElements = 2;
    
    // Выбор элементов для реакции
    const elements = document.querySelectorAll('.periodic-element, .element-card-small');
    elements.forEach(element => {
        element.addEventListener('click', function() {
            const elementId = this.getAttribute('data-element-id');
            const elementSymbol = this.querySelector('.element-symbol').textContent;
            
            if (selectedElements.some(e => e.id === elementId)) {
                // Если элемент уже выбран, удаляем его из выбранных
                selectedElements = selectedElements.filter(e => e.id !== elementId);
                this.classList.remove('selected-for-reaction');
            } else if (selectedElements.length < maxSelectedElements) {
                // Добавляем элемент в выбранные
                selectedElements.push({
                    id: elementId,
                    symbol: elementSymbol
                });
                this.classList.add('selected-for-reaction');
            }
            
            // Обновляем область реакции
            updateReactionArea(selectedElements);
            
            // Если выбрано два элемента, проверяем возможность реакции
            if (selectedElements.length === maxSelectedElements) {
                checkReaction(selectedElements[0].id, selectedElements[1].id);
            }
        });
    });
    
    // Кнопка сброса выбранных элементов
    const resetButton = document.querySelector('.reset-reaction-btn');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            selectedElements = [];
            elements.forEach(el => el.classList.remove('selected-for-reaction'));
            updateReactionArea(selectedElements);
            
            // Скрываем результат реакции
            const reactionResult = document.querySelector('.reaction-result');
            if (reactionResult) {
                reactionResult.innerHTML = '';
                reactionResult.style.display = 'none';
            }
        });
    }
}

/**
 * Обновляет область, показывающую выбранные элементы для реакции
 */
function updateReactionArea(selectedElements) {
    const reactionArea = document.querySelector('.reaction-area');
    if (!reactionArea) return;
    
    const elementSlots = reactionArea.querySelectorAll('.element-slot');
    
    // Обновляем слоты элементов
    for (let i = 0; i < elementSlots.length; i++) {
        if (selectedElements[i]) {
            elementSlots[i].innerHTML = `<div class="selected-element">${selectedElements[i].symbol}</div>`;
            elementSlots[i].classList.add('filled');
        } else {
            elementSlots[i].innerHTML = '<div class="empty-slot">?</div>';
            elementSlots[i].classList.remove('filled');
        }
    }
}

/**
 * Проверяет возможность реакции между двумя элементами
 */
function checkReaction(element1Id, element2Id) {
    // AJAX запрос для проверки возможности реакции
    fetch(`/chemistry/api/reaction/${element1Id}/${element2Id}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        const reactionResult = document.querySelector('.reaction-result');
        if (reactionResult) {
            if (data.can_react) {
                // Если реакция возможна, показываем информацию о ней
                let reactionsHtml = '<div class="reaction-success">';
                reactionsHtml += '<h3>Реакция возможна!</h3>';
                
                data.reactions.forEach(reaction => {
                    reactionsHtml += `
                        <div class="reaction-card">
                            <h4>${reaction.name}</h4>
                            <div class="reaction-formula">${reaction.formula}</div>
                            <p>${reaction.description}</p>
                            ${reaction.has_video ? 
                                `<a href="/chemistry/reactions/${reaction.id}/" class="btn bubble-btn-sm">Смотреть видео</a>` : ''}
                        </div>
                    `;
                });
                
                reactionsHtml += '</div>';
                reactionResult.innerHTML = reactionsHtml;
            } else {
                // Если реакция невозможна
                reactionResult.innerHTML = `
                    <div class="reaction-failure">
                        <h3>Реакция невозможна</h3>
                        <p>Выбранные элементы не могут взаимодействовать друг с другом.</p>
                    </div>
                `;
            }
            
            reactionResult.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Получает значение CSRF-токена из cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Настройка поиска с debounce для оптимизации
 */
function setupSearchWithDebounce() {
    const searchInputs = document.querySelectorAll('input[type="search"]');
    
    searchInputs.forEach(input => {
        // Добавляем debounce для живого поиска
        const debouncedSearch = Utils.debounce((value) => {
            // Здесь можно добавить живой поиск через AJAX
            console.log('Searching for:', value);
        }, 500);
        
        input.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    });
}

// Функция для добавления и скрытия уведомления о достижении
function showAchievementNotification(achievement) {
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = 'achievement-notification';
    
    // Формируем HTML для уведомления
    let emoji = achievement.emoji || '🏆';
    let icon = achievement.icon || 'fas fa-award';
    
    notification.innerHTML = `
        <div class="achievement-notification-inner">
            <div class="achievement-notification-icon">
                <i class="${icon}"></i>
            </div>
            <div class="achievement-notification-content">
                <div class="achievement-notification-title">
                    ${emoji} ${achievement.name}
                </div>
                <div class="achievement-notification-description">
                    ${achievement.description}
                </div>
                <div class="achievement-notification-xp">
                    +${achievement.xp_reward} XP
                </div>
            </div>
            <button class="achievement-notification-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Добавляем уведомление на страницу
    document.body.appendChild(notification);
    
    // Добавляем класс для анимации появления
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Настраиваем автоматическое скрытие через 5 секунд
    const autoCloseTimeout = setTimeout(() => {
        hideNotification(notification);
    }, 5000);
    
    // Обработчик клика на кнопку закрытия
    const closeButton = notification.querySelector('.achievement-notification-close');
    closeButton.addEventListener('click', () => {
        clearTimeout(autoCloseTimeout);
        hideNotification(notification);
    });
    
    // Функция скрытия уведомления
    function hideNotification(notificationElement) {
        notificationElement.classList.remove('show');
        setTimeout(() => {
            notificationElement.remove();
        }, 300); // 300ms - время анимации скрытия
    }
}

// Добавляем CSS стили для уведомлений
function addAchievementStyles() {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .achievement-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
            transform: translateX(120%);
            transition: transform 0.3s ease-out;
        }
        
        .achievement-notification.show {
            transform: translateX(0);
        }
        
        .achievement-notification-inner {
            display: flex;
            align-items: center;
            background-color: #fff;
            border-left: 4px solid var(--bubble-primary);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 15px;
            position: relative;
        }
        
        .achievement-notification-icon {
            background-color: var(--bubble-primary);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .achievement-notification-icon i {
            font-size: 18px;
        }
        
        .achievement-notification-content {
            flex-grow: 1;
        }
        
        .achievement-notification-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
            color: var(--bubble-primary);
        }
        
        .achievement-notification-description {
            font-size: 14px;
            color: #555;
            margin-bottom: 5px;
        }
        
        .achievement-notification-xp {
            font-size: 13px;
            font-weight: bold;
            color: #28a745;
        }
        
        .achievement-notification-close {
            position: absolute;
            top: 8px;
            right: 8px;
            background: none;
            border: none;
            color: #aaa;
            cursor: pointer;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background-color 0.2s;
        }
        
        .achievement-notification-close:hover {
            background-color: #f5f5f5;
            color: #666;
        }
    `;
    document.head.appendChild(styleElement);
}

// Функция для проверки новых достижений через API
function checkNewAchievements() {
    fetch('/accounts/api/check-new-achievements/')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.new_achievements && data.new_achievements.length > 0) {
                // Показываем уведомления для каждого нового достижения
                data.new_achievements.forEach(achievement => {
                    showAchievementNotification(achievement);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка при проверке новых достижений:', error);
        });
} 