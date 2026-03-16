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