(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // 1. Target the 'user_permissions' section
        const permWrapper = document.querySelector('.field-user_permissions');
        if (!permWrapper) return;

        // 2. Hide the default Django search filter
        const oldFilter = document.getElementById('id_user_permissions_filter');
        if (oldFilter) {
            oldFilter.parentElement.style.display = 'none';
        }

        // 3. Create the Newhope Category Dashboard
        const dashboard = document.createElement('div');
        dashboard.className = 'permission-dashboard';
        // Styles are already in your admin_custom.css, but we ensure layout here
        dashboard.style.cssText = "display:grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap:8px; padding:12px; background:#1a1a1a; border:2px solid #ff8c00; border-radius:10px; margin-bottom:15px;";

        // Define your school system modules
        const categories = [
            { name: '👤 Admin/Logs', filter: 'admin' },
            { name: '🔑 Auth/Users', filter: 'auth' },
            { name: '🎓 Students', filter: 'student' },
            { name: '💰 Finance/Fees', filter: 'payment' },
            { name: '⚙️ Core System', filter: 'core' },
            { name: '🕒 Sessions', filter: 'session' }
        ];

        categories.forEach(cat => {
            const label = document.createElement('label');
            label.style.cssText = "color:#ffcc00; font-weight:bold; cursor:pointer; display:flex; align-items:center; font-size:13px;";
            label.innerHTML = `<input type="checkbox" style="margin-right:8px;" data-filter="${cat.filter}"> ${cat.name}`;
            dashboard.appendChild(label);
        });

        // Inject the dashboard above the selection boxes
        const helpText = permWrapper.querySelector('.help');
        if (helpText) helpText.after(dashboard);

        // 4. Multi-Filter Logic
        const availableSelect = document.getElementById('id_user_permissions_from');
        
        dashboard.querySelectorAll('input').forEach(box => {
            box.addEventListener('change', function() {
                const activeFilters = Array.from(dashboard.querySelectorAll('input:checked'))
                                          .map(cb => cb.getAttribute('data-filter'));
                
                const options = availableSelect.options;

                for (let i = 0; i < options.length; i++) {
                    const optText = options[i].text.toLowerCase();
                    
                    if (activeFilters.length === 0) {
                        // If nothing is checked, show everything
                        options[i].style.display = 'block';
                    } else {
                        // Show if the option matches ANY of the checked categories
                        const matches = activeFilters.some(filter => optText.includes(filter));
                        options[i].style.display = matches ? 'block' : 'none';
                    }
                }
            });
        });
    });
})();