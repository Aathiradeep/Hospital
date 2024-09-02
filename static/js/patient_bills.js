document.addEventListener('DOMContentLoaded', function() {
    // Sorting functionality
    const headers = document.querySelectorAll('.billing-table th');
    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            const table = header.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const isAscending = header.classList.contains('asc');

            rows.sort((rowA, rowB) => {
                const cellA = rowA.children[index].textContent.trim();
                const cellB = rowB.children[index].textContent.trim();
                return (isAscending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA));
            });

            rows.forEach(row => tbody.appendChild(row));

            headers.forEach(h => h.classList.remove('asc', 'desc'));
            header.classList.add(isAscending ? 'desc' : 'asc');
        });
    });
});
