document.addEventListener('DOMContentLoaded', function() {
    const favoriteButton = document.getElementById('favorite-button');
    if (favoriteButton) {
        favoriteButton.addEventListener('click', function() {
            const elementId = this.dataset.elementId;
            
            fetch('/chemistry/api/toggle-favorite-element/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    element_id: elementId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.is_favorite) {
                        favoriteButton.innerHTML = '<i class="fas fa-star me-1"></i> В избранном';
                        favoriteButton.classList.remove('bubble-btn-outline');
                        favoriteButton.classList.add('btn-warning');
                    } else {
                        favoriteButton.innerHTML = '<i class="far fa-star me-1"></i> В избранное';
                        favoriteButton.classList.remove('btn-warning');
                        favoriteButton.classList.add('bubble-btn-outline');
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    }
    
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
}); 