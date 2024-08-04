document.addEventListener('DOMContentLoaded', () => {
    const aboutLink = document.getElementById('aboutLink');
    const aboutPopup = document.getElementById('aboutPopup');
    const closeBtn = document.querySelector('.popup .close');

    if (aboutLink && aboutPopup && closeBtn) {
        aboutLink.addEventListener('click', (e) => {
            e.preventDefault();
            aboutPopup.style.display = 'block';
        });

        closeBtn.addEventListener('click', () => {
            aboutPopup.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target === aboutPopup) {
                aboutPopup.style.display = 'none';
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const openSearchBtn = document.getElementById('openSearchBtn');
    const searchModal = document.getElementById('searchModal');
    const closeSearchBtn = searchModal.querySelector('.close');

    if (openSearchBtn && searchModal && closeSearchBtn) {
        openSearchBtn.addEventListener('click', () => {
            searchModal.style.display = 'block';
        });

        closeSearchBtn.addEventListener('click', () => {
            searchModal.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target === searchModal) {
                searchModal.style.display = 'none';
            }
        });

        window.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                searchModal.style.display = 'none';
            }
        });
    }
});
