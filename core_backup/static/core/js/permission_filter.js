document.addEventListener('DOMContentLoaded', function() {
    const permHeader = document.querySelector('.field-user_permissions h2');
    if (!permHeader) return;

    // Create the Category Container
    const container = document.createElement('div');
    container.className = 'permission-categories';
    container.innerHTML = `
        <div class="category-item"><input type="checkbox" data-filter="student"> Student Mgmt</div>
        <div class="category-item"><input type="checkbox" data-filter="feepayment"> Bursary/Fees</div>
        <div class="category-item"><input type="checkbox" data-filter="user"> User/Staff Admin</div>
        <div class="category-item"><input type="checkbox" data-filter="module"> System Control</div>
    `;
    
    permHeader.after(container);

    const checkboxes = container.querySelectorAll('input');
    const availableList = document.querySelector('#id_user_permissions_from');

    checkboxes.forEach(box => {
        box.addEventListener('change', function() {
            const filterText = this.getAttribute('data-filter');
            const options = availableList.options;

            for (let i = 0; i < options.length; i++) {
                if (options[i].text.toLowerCase().includes(filterText)) {
                    options[i].style.display = this.checked ? 'block' : 'none';
                    // If checked, move to "Chosen" automatically if desired
                    if (this.checked) options[i].selected = true;
                }
            }
            // Trigger Django's built-in "Move" button click to move selected items
            document.querySelector('#id_user_permissions_add_link').click();
        });
    });
});