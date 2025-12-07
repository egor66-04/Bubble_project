/**
 * Интерактивная таблица Менделеева
 * Управление цветами, фильтрацией и визуальными эффектами
 */

// Цветовая палитра для категорий элементов
const CATEGORY_COLORS = {
    'Щелочные металлы': {
        primary: '#FF6B9D',
        gradient: 'linear-gradient(135deg, #FF6B9D 0%, #FF8FB3 100%)',
        shadow: 'rgba(255, 107, 157, 0.4)'
    },
    'Щелочноземельные металлы': {
        primary: '#FFB347',
        gradient: 'linear-gradient(135deg, #FFB347 0%, #FFCC70 100%)',
        shadow: 'rgba(255, 179, 71, 0.4)'
    },
    'Переходные металлы': {
        primary: '#4FACFE',
        gradient: 'linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%)',
        shadow: 'rgba(79, 172, 254, 0.4)'
    },
    'Постпереходные металлы': {
        primary: '#43E97B',
        gradient: 'linear-gradient(135deg, #43E97B 0%, #38F9D7 100%)',
        shadow: 'rgba(67, 233, 123, 0.4)'
    },
    'Металлоиды': {
        primary: '#FA709A',
        gradient: 'linear-gradient(135deg, #FA709A 0%, #FEE140 100%)',
        shadow: 'rgba(250, 112, 154, 0.4)'
    },
    'Неметаллы': {
        primary: '#667EEA',
        gradient: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
        shadow: 'rgba(102, 126, 234, 0.4)'
    },
    'Галогены': {
        primary: '#FEE140',
        gradient: 'linear-gradient(135deg, #FEE140 0%, #FA709A 100%)',
        shadow: 'rgba(254, 225, 64, 0.4)'
    },
    'Благородные газы': {
        primary: '#C471F5',
        gradient: 'linear-gradient(135deg, #C471F5 0%, #FA71CD 100%)',
        shadow: 'rgba(196, 113, 245, 0.4)'
    },
    'Лантаноиды': {
        primary: '#38F9D7',
        gradient: 'linear-gradient(135deg, #38F9D7 0%, #43E97B 100%)',
        shadow: 'rgba(56, 249, 215, 0.4)'
    },
    'Актиноиды': {
        primary: '#F093FB',
        gradient: 'linear-gradient(135deg, #F093FB 0%, #F5576C 100%)',
        shadow: 'rgba(240, 147, 251, 0.4)'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    initializePeriodicTable();
});

function initializePeriodicTable() {
    applyElementColors();
    setupElementHoverEffects();
    setupFilteringSystem();
    animateElementsOnLoad();
}

/**
 * Применение градиентных цветов к элементам
 */
function applyElementColors() {
    const elements = document.querySelectorAll('.element-card');
    
    elements.forEach((element, index) => {
        const categoryName = element.querySelector('.element-inner').style.backgroundColor;
        const inner = element.querySelector('.element-inner');
        
        // Добавляем задержку анимации для плавного появления
        element.style.animationDelay = `${index * 0.015}s`;
        
        // Находим категорию по цвету
        for (const [category, colors] of Object.entries(CATEGORY_COLORS)) {
            if (categoryName && categoryName.toLowerCase().includes(colors.primary.toLowerCase().substring(1))) {
                applyGradientToElement(inner, colors);
                break;
            }
        }
    });
}

/**
 * Применение градиента к элементу
 */
function applyGradientToElement(inner, colors) {
    inner.style.background = colors.gradient;
    inner.style.borderColor = colors.primary;
    
    // Добавляем CSS переменные для эффектов
    inner.style.setProperty('--element-shadow', colors.shadow);
    inner.style.setProperty('--element-color', colors.primary);
}

/**
 * Настройка эффектов при наведении
 */
function setupElementHoverEffects() {
    const elements = document.querySelectorAll('.element-card');
    
    elements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const inner = this.querySelector('.element-inner');
            const shadow = inner.style.getPropertyValue('--element-shadow') || 'rgba(102, 126, 234, 0.4)';
            
            // Усиленная тень при наведении
            this.style.filter = `drop-shadow(0 15px 30px ${shadow})`;
            
            // Увеличение размера символа
            const symbol = this.querySelector('.element-symbol');
            if (symbol) {
                symbol.style.transform = 'scale(1.1)';
            }
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.filter = '';
            
            const symbol = this.querySelector('.element-symbol');
            if (symbol) {
                symbol.style.transform = '';
            }
        });
    });
}

/**
 * Настройка системы фильтрации
 */
function setupFilteringSystem() {
    const categoryItems = document.querySelectorAll('.category-legend-item');
    const stateFilter = document.getElementById('stateFilter');
    const searchInput = document.getElementById('elementSearch');
    
    // Применяем градиенты к легенде
    categoryItems.forEach(item => {
        const categoryName = item.textContent.trim();
        if (CATEGORY_COLORS[categoryName]) {
            item.style.background = CATEGORY_COLORS[categoryName].gradient;
            item.style.color = '#fff';
            item.style.fontWeight = '600';
            item.style.textShadow = '0 1px 2px rgba(0,0,0,0.2)';
        }
    });
    
    // Фильтрация с анимацией
    if (categoryItems) {
        categoryItems.forEach(item => {
            item.addEventListener('click', function() {
                filterElementsWithAnimation();
            });
        });
    }
    
    if (stateFilter) {
        stateFilter.addEventListener('change', filterElementsWithAnimation);
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterElementsWithAnimation, 300));
    }
}

/**
 * Фильтрация с анимацией
 */
function filterElementsWithAnimation() {
    const elements = document.querySelectorAll('.element-card');
    const activeCategory = document.querySelector('.category-legend-item.active');
    const selectedState = document.getElementById('stateFilter')?.value || 'all';
    const searchTerm = document.getElementById('elementSearch')?.value.toLowerCase().trim() || '';
    
    elements.forEach((element, index) => {
        const categoryId = element.dataset.category;
        const state = element.dataset.state;
        const searchData = element.dataset.search;
        
        let visible = true;
        
        // Проверка категории
        if (activeCategory && !activeCategory.classList.contains('all-categories')) {
            visible = visible && (categoryId === activeCategory.dataset.category);
        }
        
        // Проверка состояния
        if (selectedState !== 'all') {
            visible = visible && (state === selectedState);
        }
        
        // Проверка поиска
        if (searchTerm) {
            visible = visible && searchData.includes(searchTerm);
        }
        
        // Применение видимости с анимацией
        if (visible) {
            element.classList.remove('hidden-element');
            element.style.animationDelay = `${index * 0.01}s`;
        } else {
            element.classList.add('hidden-element');
        }
    });
}

/**
 * Анимация элементов при загрузке страницы
 */
function animateElementsOnLoad() {
    const elements = document.querySelectorAll('.element-card');
    
    // Создаем эффект волны при загрузке
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('loaded');
        }, index * 15);
    });
}

/**
 * Debounce функция для оптимизации
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Создание частиц вокруг элемента при клике
 */
function createParticleEffect(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 12; i++) {
        const particle = document.createElement('div');
        particle.className = 'element-particle';
        
        const angle = (Math.PI * 2 * i) / 12;
        const velocity = 2 + Math.random() * 2;
        
        particle.style.left = centerX + 'px';
        particle.style.top = centerY + 'px';
        particle.style.setProperty('--tx', Math.cos(angle) * 50 * velocity + 'px');
        particle.style.setProperty('--ty', Math.sin(angle) * 50 * velocity + 'px');
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
}

// Добавление частиц при клике на элемент
document.addEventListener('click', function(e) {
    const elementCard = e.target.closest('.element-card');
    if (elementCard) {
        createParticleEffect(elementCard);
    }
});