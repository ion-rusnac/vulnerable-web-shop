/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

document.addEventListener('DOMContentLoaded', () => {
    const cartBadge = document.querySelector('.badge');
    const addToCartButtons = document.querySelectorAll('.btn-outline-primary, .btn-outline-dark');

    let cartCount = 0;

    addToCartButtons.forEach(button => {
        if (button.textContent.trim() === 'Add to Cart') {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                cartCount++;
                cartBadge.textContent = cartCount;

                // Simple feedback
                const originalText = button.textContent;
                button.textContent = 'Added!';
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-success');
                button.disabled = true;

                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-primary');
                    button.disabled = false;
                }, 1000);
            });
        }
    });
});