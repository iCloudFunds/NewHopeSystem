document.addEventListener('DOMContentLoaded', function() {
    const deptField = document.querySelector('#id_department');
    const subDeptRow = document.querySelector('.field-sub_department');

    function toggleSubDept() {
        if (deptField.value === 'GENERAL') {
            subDeptRow.style.display = 'block';
        } else {
            subDeptRow.style.display = 'none';
        }
    }

    deptField.addEventListener('change', toggleSubDept);
    toggleSubDept(); // Run on page load
});