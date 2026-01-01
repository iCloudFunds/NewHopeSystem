document.addEventListener('DOMContentLoaded', function() {
    // 1. Find the password field
    const passwordField = document.querySelector('#id_password');
    
    if (passwordField) {
        // 2. Create the checkbox and label
        const container = document.createElement('div');
        container.className = 'show-password-container';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'show-password-check';
        
        const label = document.createElement('label');
        label.setAttribute('for', 'show-password-check');
        label.innerText = 'Show Password';
        
        container.appendChild(checkbox);
        container.appendChild(label);
        
        // 3. Insert it right after the password field
        passwordField.parentNode.insertBefore(container, passwordField.nextSibling);
        
        // 4. Toggle logic
        checkbox.addEventListener('change', function() {
            passwordField.type = this.checked ? 'text' : 'password';
        });
    }
});