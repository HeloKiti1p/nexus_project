let currentPage = 1;          // Текущая загруженная страница (первая уже загружена)
let loading = false;          // Флаг, чтобы не загружать одновременно несколько страниц
let hasNext = true;           // Есть ли ещё страницы для загрузки

const trigger = document.getElementById('scroll-trigger');
const container = document.querySelector('.posts-container');

async function loadMorePosts() {
    if (loading || !hasNext) return;
    loading = true;
    
    try {
        const response = await fetch(`/load_posts/?page=${currentPage + 1}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        
        if (data.html) {
            container.insertAdjacentHTML('beforeend', data.html);
            currentPage++;
            hasNext = data.has_next;
        }
    } catch (error) {
        console.error('Ошибка загрузки постов:', error);
    } finally {
        loading = false;
    }
}

const observer = new IntersectionObserver(async (entries) => {
    for (let entry of entries) {
        if (entry.isIntersecting) {
            await loadMorePosts();
        }
    }
}, { threshold: 0.1 });

observer.observe(trigger);

document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const liked = this.classList.contains('liked');

            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.classList.add('liked');
                    this.querySelector('i').classList.remove('bi-heart');
                    this.querySelector('i').classList.add('bi-heart-fill');
                } else {
                    this.classList.remove('liked');
                    this.querySelector('i').classList.remove('bi-heart-fill');
                    this.querySelector('i').classList.add('bi-heart');
                }
                this.querySelector('.like-count').textContent = data.total_likes;
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });

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
// После вставки новых постов снова ищем кнопки лайков и добавляем обработчики
document.querySelectorAll('.like-button:not(.bound)').forEach(button => {
    button.classList.add('bound');
    button.addEventListener('click', likeHandler);
});