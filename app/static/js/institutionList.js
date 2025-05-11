document.addEventListener('DOMContentLoaded', function() {
    loadInstitutions();

    // Обработка формы поиска
    const searchForm = document.getElementById('search-form');
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        searchInstitutions();
    });

    // Обработка кнопки очистки
    searchForm.addEventListener('reset', function() {
        setTimeout(() => loadInstitutions(), 0);
    });
});

function loadInstitutions(filters = {}) {
    const tbody = document.getElementById('institutions-list');
    tbody.innerHTML = '<tr><td colspan="6">Загрузка...</td></tr>';

    fetch('/medical_institution/list/all')
        .then(response => {
            if (!response.ok) throw new Error('Ошибка загрузки данных');
            return response.json();
        })
        .then(data => {
            tbody.innerHTML = '';

            if (data.error) {
                tbody.innerHTML = `<tr><td colspan="6">${data.error}</td></tr>`;
                return;
            }

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6">Нет данных</td></tr>';
                return;
            }

            data.forEach(inst => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${inst.nameofinstitution || ''}</td>
                    <td>${inst.typeofinstitution || ''}</td>
                    <td>${inst.address || ''}</td>
                    <td>${inst.contactphonenumber || ''}</td>
                    <td>${inst.email || ''}</td>
                    <td>
                        <button onclick="openEditInstitutionModal(${inst.institutioncode})">Изменить</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке учреждений:', error);
            tbody.innerHTML = '<tr><td colspan="6">Ошибка загрузки данных</td></tr>';
        });
}

function searchInstitutions() {
    const formData = {
        nameofinstitution: document.getElementById('nameofinstitution').value,
        typeofinstitution: document.getElementById('typeofinstitution').value,
        address: document.getElementById('address').value,
        contactphonenumber: document.getElementById('contactphonenumber').value
    };

    fetch('/medical_institution/list/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка поиска');
        return response.json();
    })
    .then(data => {
        const tbody = document.getElementById('institutions-list');
        tbody.innerHTML = '';

        if (data.error) {
            tbody.innerHTML = `<tr><td colspan="6">${data.error}</td></tr>`;
            return;
        }

        data.forEach(inst => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${inst.nameofinstitution || ''}</td>
                <td>${inst.typeofinstitution || ''}</td>
                <td>${inst.address || ''}</td>
                <td>${inst.contactphonenumber || ''}</td>
                <td>${inst.email || ''}</td>
                <td>
                    <button onclick="openEditInstitutionModal(${inst.institutioncode})">Изменить</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Ошибка поиска:', error);
        const tbody = document.getElementById('institutions-list');
        tbody.innerHTML = `<tr><td colspan="6">Ошибка поиска: ${error.message}</td></tr>`;
    });
}