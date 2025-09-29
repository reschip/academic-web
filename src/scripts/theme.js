// Theme toggle functionality
export function initTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;

    if (!themeToggle) return;

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        
        // Add smooth transition
        body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        // Store preference
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
    }
}

// Smooth scroll for navigation
export function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Header scroll effect
export function initHeaderScroll() {
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        const body = document.body;
        const isDarkMode = body.classList.contains('dark-mode');
        
        if (header) {
            header.style.background = isDarkMode ? '#1a1a1a' : '#fafafa';
            header.style.boxShadow = 'none';
        }
    });
}

// Add hover effects to post cards
export function initPostCardEffects() {
    document.querySelectorAll('.post-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialize all functionality
export function initAll() {
    initTheme();
    initSmoothScroll();
    initHeaderScroll();
    initPostCardEffects();
}
