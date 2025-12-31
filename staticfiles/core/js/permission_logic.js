(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // 1. Target the 'user_permissions' section
        const permWrapper = document.querySelector('.field-user_permissions');
        if (!permWrapper) return;

        // 2. Hide the default search box
        const oldFilter = document.getElementById('id_user_permissions_filter');
        if (oldFilter) oldFilter.parentElement.style.display = 'none';

        // 3. Create our Rising Sun Dashboard
        const dashboard = document.createElement('div');
        dashboard.className = 'permission-dashboard';
        dashboard.style.cssText = "display:grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap:10px; padding:15px; background:#1a1a1a; border:2px solid #ff8c00; border-radius:10px; margin-bottom:15px;";

        const categories = [
            { name: 'Admin', filter: 'admin' },
            { name: 'Auth', filter: 'auth' },
            { name: 'Content', filter: 'contenttype' },
            { name: 'Classes', filter: 'student' },
            { name: 'Finance', filter: 'payment' },
            { name: 'Core', filter: 'core' },
            { name: 'Sessions', filter: 'session' }
        ];

        categories.forEach(cat => {
            const label = document.createElement('label');
            label.style.cssText = "color:#ffcc00; font-weight:bold; cursor:pointer; display:flex; align-items:center;";
            label.innerHTML = `<input type="checkbox" style="margin-right:8px;" data-filter="${cat.filter}"> ${cat.name}`;
            dashboard.appendChild(label);
        });

        // Inject Dashboard
        permWrapper.querySelector('.help').after(dashboard);

        // 4. Filtering Logic
        const availableSelect = document.getElementById('id_user_permissions_from');
        dashboard.querySelectorAll('input').forEach(box => {
            box.addEventListener('change', function() {
                const filter = this.getAttribute('data-filter');
                const options = availableSelect.options;

                for (let i = 0; i < options.length; i++) {
                    if (options[i].text.toLowerCase().includes(filter)) {
                        options[i].style.display = this.checked ? 'block' : 'none';
                    }
                }
            });
        });
    });
})();