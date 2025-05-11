function loadDoctors() {
    fetch('/doctor/list/all')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('doctors-list');
            tableBody.innerHTML = '';

            data.forEach(doctor => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${doctor.secondname} ${doctor.name}</td>
                    <td>${doctor.servicenumber}</td>
                    <td>${doctor.jobtitle}</td>
                    <td>${doctor.role}</td>
                    <td>${doctor.login}</td>
                    <td>${doctor.email}</td>
                    <td>${doctor.institutionname}</td>
                    <td class="action-buttons">
                        <button onclick="editDoctor(${doctor.institutioncode}, ${doctor.servicenumber})">Изменить</button>
                        <button onclick="dismissDoctor(${doctor.institutioncode}, ${doctor.servicenumber}, '${doctor.secondname} ${doctor.name}')">Уволить</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function searchDoctors() {
    const formData = {
        name: document.getElementById('name').value,
        secondname: document.getElementById('secondname').value,
        servicenumber: document.getElementById('servicenumber').value,
        jobtitle: document.getElementById('jobtitle').value
    };

    fetch('/doctor/list/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка поиска');
        }
        return response.json();
    })
    .then(data => {
        const tableBody = document.getElementById('doctors-list');
        tableBody.innerHTML = '';

        data.forEach(doctor => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${doctor.secondname} ${doctor.name}</td>
                <td>${doctor.servicenumber}</td>
                <td>${doctor.jobtitle}</td>
                <td>${doctor.role}</td>
                <td>${doctor.login}</td>
                <td>${doctor.email}</td>
                <td>${doctor.institutionname}</td>
                <td class="action-buttons">
                    <button onclick="editDoctor(${doctor.institutioncode}, ${doctor.servicenumber})">Изменить</button>
                    <button onclick="dismissDoctor(${doctor.institutioncode}, ${doctor.servicenumber}, '${doctor.secondname} ${doctor.name}')">Уволить</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function editDoctor(institutionCode, serviceNumber) {
    fetch(`/doctor/get?institutioncode=${institutionCode}&servicenumber=${serviceNumber}`)
        .then(response => response.json())
        .then(doctor => {
            document.getElementById('editDoctorInstitutionCode').value = doctor.institutioncode;
            document.getElementById('editDoctorServiceNumber').value = doctor.servicenumber;
            document.getElementById('editDoctorName').value = doctor.name;
            document.getElementById('editDoctorSecondName').value = doctor.secondname;
            document.getElementById('editDoctorJobTitle').value = doctor.jobtitle;
            document.getElementById('editDoctorRole').value = doctor.role;
            document.getElementById('editDoctorLogin').value = doctor.login;
            document.getElementById('editDoctorEmail').value = doctor.email;

            document.getElementById('editDoctorModal').style.display = 'block';
        });
}

function dismissDoctor(institutionCode, serviceNumber, doctorName) {
    document.getElementById('dismissDoctorName').textContent = doctorName;
    document.getElementById('dismissModal').dataset.institutionCode = institutionCode;
    document.getElementById('dismissModal').dataset.serviceNumber = serviceNumber;

    fetch('/doctor/list/all')
        .then(response => response.json())
        .then(doctors => {
            const select = document.getElementById('transferToDoctor');
            select.innerHTML = '<option value="">Выберите врача</option>';

            doctors.forEach(doctor => {
                if (!(doctor.institutioncode === institutionCode && doctor.servicenumber === serviceNumber)) {
                    const option = document.createElement('option');
                    option.value = `${doctor.institutioncode}|${doctor.servicenumber}`;
                    option.textContent = `${doctor.secondname} ${doctor.name} (${doctor.servicenumber})`;
                    select.appendChild(option);
                }
            });

            document.getElementById('dismissModal').style.display = 'block';
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        searchDoctors();
    });

    // Обработка кнопки очистки
    form.addEventListener('reset', () => {
        setTimeout(() => searchDoctors(), 0);
    });

    searchDoctors();
});