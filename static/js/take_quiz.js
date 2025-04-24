document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quiz-form');
    const questionCards = document.querySelectorAll('.question-card');
    const progressBar = document.getElementById('quiz-progress-bar');
    const quizSummary = document.getElementById('quiz-summary');
    const answeredCount = document.getElementById('answered-count');
    const questionStatusList = document.querySelectorAll('.question-status');
    const backToQuizBtn = document.getElementById('back-to-quiz');
    const finishQuizBtn = document.querySelector('.finish-quiz');
    const warningModalElement = document.getElementById('warningModal');
    
    // Получаем время теста из атрибута data-time-limit
    const quizTimeLimitElement = document.getElementById('quiz-timer');
    let timeLeft = parseInt(quizTimeLimitElement.getAttribute('data-time-limit')) * 60; // в секундах
    
    const timerDisplay = document.getElementById('quiz-timer');
    const minutesDisplay = document.getElementById('minutes');
    const secondsDisplay = document.getElementById('seconds');
    
    // Инициализируем модальное окно Bootstrap
    let warningModal;
    if (typeof bootstrap !== 'undefined') {
        warningModal = new bootstrap.Modal(warningModalElement);
    } else {
        console.error('Bootstrap не найден. Модальное окно не будет работать.');
    }
    
    function startTimer() {
        const timerInterval = setInterval(function() {
            timeLeft--;
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                submitQuiz();
            } else {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                
                minutesDisplay.textContent = minutes.toString().padStart(2, '0');
                secondsDisplay.textContent = seconds.toString().padStart(2, '0');
                
                // Предупреждение, когда осталось мало времени
                if (timeLeft <= 60) {
                    timerDisplay.classList.add('quiz-timer-warning');
                }
            }
        }, 1000);
    }
    
    // Начинаем таймер при загрузке страницы
    startTimer();
    
    // Обработчики для кнопок навигации - заменяем старые кнопки на новые с новыми обработчиками
    document.querySelectorAll('.next-question').forEach(button => {
        // Создаем новую кнопку, чтобы удалить все предыдущие обработчики
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        // Добавляем новый обработчик
        newButton.addEventListener('click', function(event) {
            console.log('Next button clicked');
            
            const currentCard = this.closest('.question-card');
            const currentIndex = parseInt(currentCard.dataset.questionIndex);
            const nextIndex = parseInt(this.dataset.nextQuestion);
            
            // Проверяем, выбран ли ответ
            const questionId = currentCard.dataset.questionId;
            const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
            
            if (!answered) {
                event.preventDefault();
                if (warningModal) {
                    warningModal.show();
                } else {
                    alert('Пожалуйста, выберите ответ перед тем, как продолжить.');
                }
                return false;
            }
            
            // Переходим к следующему вопросу
            showQuestion(nextIndex);
            updateProgress();
        });
    });
    
    document.querySelectorAll('.prev-question').forEach(button => {
        // Создаем новую кнопку, чтобы удалить все предыдущие обработчики
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        // Добавляем новый обработчик
        newButton.addEventListener('click', function() {
            const prevQuestionIndex = parseInt(this.dataset.prevQuestion);
            showQuestion(prevQuestionIndex);
            updateProgress();
        });
    });
    
    // Обработчик для кнопки "Завершить тест"
    if (finishQuizBtn) {
        // Создаем новую кнопку, чтобы удалить все предыдущие обработчики
        const newFinishBtn = finishQuizBtn.cloneNode(true);
        finishQuizBtn.parentNode.replaceChild(newFinishBtn, finishQuizBtn);
        
        // Добавляем новый обработчик
        newFinishBtn.addEventListener('click', function() {
            const lastQuestionIndex = questionCards.length - 1;
            const questionId = questionCards[lastQuestionIndex].dataset.questionId;
            const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
            
            if (!answered) {
                // Показываем предупреждение, если ответ не выбран
                if (warningModal) {
                    warningModal.show();
                } else {
                    alert('Пожалуйста, выберите ответ перед тем, как продолжить.');
                }
                return;
            }
            
            updateProgress();
            
            // Скрываем все вопросы и показываем сводку
            questionCards.forEach(card => {
                card.classList.add('d-none');
            });
            
            quizSummary.classList.remove('d-none');
        });
    }
    
    // Показать определенный вопрос
    function showQuestion(index) {
        questionCards.forEach(card => {
            card.classList.add('d-none');
        });
        
        questionCards[index].classList.remove('d-none');
        
        // Проверяем активацию кнопки "Далее" при переключении вопроса
        checkNextButtonState(index);
    }
    
    // Проверка и активация кнопки "Далее"
    function checkNextButtonState(questionIndex) {
        const questionId = questionCards[questionIndex].dataset.questionId;
        const nextButton = questionCards[questionIndex].querySelector('.next-question');
        
        if (nextButton) {
            const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
            nextButton.disabled = !answered;
        }
    }
    
    // Обновить прогресс прохождения теста
    function updateProgress() {
        const answeredQuestions = countAnsweredQuestions();
        const progressPercent = Math.round((answeredQuestions / questionCards.length) * 100);
        
        progressBar.style.width = `${progressPercent}%`;
        progressBar.setAttribute('aria-valuenow', progressPercent);
        progressBar.textContent = `${progressPercent}%`;
        
        // Обновляем статусы ответов в сводке
        updateQuestionStatusList();
    }
    
    // Подсчет отвеченных вопросов
    function countAnsweredQuestions() {
        let count = 0;
        
        questionCards.forEach(card => {
            const questionId = card.dataset.questionId;
            const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
            
            if (answered) {
                count++;
            }
        });
        
        answeredCount.textContent = count;
        return count;
    }
    
    // Обновление статусов вопросов в сводке
    function updateQuestionStatusList() {
        questionStatusList.forEach(status => {
            const questionIndex = status.dataset.questionIndex;
            const questionId = questionCards[questionIndex].dataset.questionId;
            const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
            
            const statusIcon = status.querySelector('.question-answered-status');
            
            if (answered) {
                statusIcon.classList.remove('not-answered');
                statusIcon.classList.add('answered');
                statusIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
            } else {
                statusIcon.classList.remove('answered');
                statusIcon.classList.add('not-answered');
                statusIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
            }
        });
    }
    
    // Обработчик клика по индикатору вопроса
    questionStatusList.forEach(status => {
        // Создаем новый элемент, чтобы удалить все предыдущие обработчики
        const newStatus = status.cloneNode(true);
        status.parentNode.replaceChild(newStatus, status);
        
        // Добавляем новый обработчик
        newStatus.addEventListener('click', function() {
            const questionIndex = this.dataset.questionIndex;
            showQuestion(parseInt(questionIndex));
            quizSummary.classList.add('d-none');
            updateProgress();
        });
    });
    
    // Обработчик для кнопки "Вернуться к тесту"
    if (backToQuizBtn) {
        // Создаем новую кнопку, чтобы удалить все предыдущие обработчики
        const newBackBtn = backToQuizBtn.cloneNode(true);
        backToQuizBtn.parentNode.replaceChild(newBackBtn, backToQuizBtn);
        
        // Добавляем новый обработчик
        newBackBtn.addEventListener('click', function() {
            quizSummary.classList.add('d-none');
            
            // Показываем первый неотвеченный вопрос или последний вопрос
            let firstUnansweredIndex = 0;
            let found = false;
            
            questionCards.forEach((card, index) => {
                if (!found) {
                    const questionId = card.dataset.questionId;
                    const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
                    
                    if (!answered) {
                        firstUnansweredIndex = index;
                        found = true;
                    }
                }
            });
            
            if (!found) {
                firstUnansweredIndex = questionCards.length - 1;
            }
            
            showQuestion(firstUnansweredIndex);
        });
    }
    
    // Обработчик изменения ответов
    document.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener('change', function() {
            const questionCard = this.closest('.question-card');
            const questionIndex = parseInt(questionCard.dataset.questionIndex);
            
            // Активируем кнопку "Далее" после выбора ответа
            const nextButton = questionCard.querySelector('.next-question');
            if (nextButton) {
                nextButton.disabled = false;
            }
            
            updateProgress();
        });
    });
    
    // Функция отправки формы
    function submitQuiz() {
        quizForm.submit();
    }
    
    // Инициализация прогресса и состояния кнопок
    updateProgress();
    questionCards.forEach((card, index) => {
        checkNextButtonState(index);
    });
    
    console.log('Quiz script initialized successfully!');
}); 