document.addEventListener('DOMContentLoaded', function() {
    const deptField = document.querySelector('#id_department');
    // Django Admin wraps fields in a div with a class like 'field-fieldname'
    const subDeptRow = document.querySelector('.field-sub_department');

    function toggleSubDept() {
        if (deptField.value === 'GENERAL') {
            subDeptRow.style.display = 'block'; // Show if General
        } else {
            subDeptRow.style.display = 'none';  // Hide if Industrial/Commercial
        }
    }

    if (deptField && subDeptRow) {
        deptField.addEventListener('change', toggleSubDept);
        toggleSubDept(); // Run immediately when page loads
    }
});