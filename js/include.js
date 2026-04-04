// js/include.js

function includeHTML() {
    const elements = document.querySelectorAll('[data-include]');
    let loadedCount = 0;

    // If no elements to include, just run layout fix once
    if(elements.length === 0) {
        triggerLayoutFix();
        return;
    }

    elements.forEach(el => {
        const file = el.getAttribute('data-include');
        if (file) {
            fetch(file)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.text();
                })
                .then(data => {
                    el.innerHTML = data;
                    el.removeAttribute('data-include');

                    // Specific logic for header
                    if (file.includes('header')) {
                        attachHeaderEvents();
                    }

                    loadedCount++;
                    // If all includes are done, force layout fix
                    if(loadedCount === elements.length) {
                        triggerLayoutFix();
                    }
                })
                .catch(error => console.error('Error loading include:', error));
        }
    });
}

function attachHeaderEvents() {
    const donateBtn = document.getElementById('donateBtn');
    if (donateBtn) {
        // Remove existing listeners to prevent duplicates if re-loaded
        const newBtn = donateBtn.cloneNode(true);
        donateBtn.parentNode.replaceChild(newBtn, donateBtn);
        newBtn.addEventListener('click', () => {
            window.open('https://paystack.com/pay/zylotech-support', '_blank');
        });
    }
}

// This function forces the app to recognize the new height of header/footer
function triggerLayoutFix() {
    // Dispatch a custom event that the main page listens for
    window.dispatchEvent(new Event('includesLoaded'));

    // Also manually trigger resize which usually fixes canvas issues
    window.dispatchEvent(new Event('resize'));
}

// Load includes when DOM is ready
document.addEventListener('DOMContentLoaded', includeHTML);