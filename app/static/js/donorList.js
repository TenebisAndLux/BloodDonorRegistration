let selectedRow = null;

function searchDonors() {
    document.getElementById('loading').style.display = 'block';
    const form = document.getElementById('search-form');
    const formData = new FormData(form);
    const params = new URLSearchParams();

    for (const [key, value] of formData) {
        if (value) params.append(key, value);
    }

    const url = `/donor/list/search?${params.toString()}`;
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '';

            if (data.message === 'Donors not found.') {
                donorsTable.innerHTML = '<tr><td colspan="11">Доноры не найдены</td></tr>';
            } else {
                data.forEach(donor => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${donor.institutionname}</td>
                        <td>${donor.passportdata}</td>
                        <td>${donor.surname} ${donor.name} ${donor.secondname}</td>
                        <td>${donor.gender}</td>
                        <td>${donor.birthday}</td>
                        <td>${donor.address}</td>
                        <td>${donor.phonenumber}</td>
                        <td>${donor.polis}</td>
                        <td>${donor.bloodgroup}</td>
                        <td>${donor.rhfactor}</td>
                        <td style="display:flex;gap:10px;align-items:center;">
                            <button onclick="prepareEditModal('${donor.passportdata}', '${donor.institutioncode}')">Изменить</button>
                            <button onclick="openHistoryModal('${donor.passportdata}', '${donor.institutioncode}')">История</button>
                        </td>
                    `;
                    row.addEventListener('click', (e) => {
                        if (e.target.tagName === 'BUTTON') return;
                        if (selectedRow) selectedRow.classList.remove('selected');
                        selectedRow = row;
                        row.classList.add('selected');
                    });
                    donorsTable.appendChild(row);
                });
            }
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '<tr><td colspan="11">Ошибка при загрузке доноров</td></tr>';
            document.getElementById('loading').style.display = 'none';
        });
}

function getDonors() {
    if (!getShouldGetDonorsState()) return;
    document.getElementById('loading').style.display = 'block';
    fetch('/donor/list/get?order=asc')
        .then(response => {
            if (!response.ok) throw new Error('Ошибка загрузки списка доноров');
            return response.json();
        })
        .then(donors => {
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '';

            if (donors.length === 0) {
                donorsTable.innerHTML = `<tr><td colspan="11" style="text-align: center;">Нет данных о донорах</td></tr>`;
            } else {
                donors.forEach(donor => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${donor.institution_name}</td>
                        <td>${donor.passportdata}</td>
                        <td>${donor.surname} ${donor.name} ${donor.secondname || ''}</td>
                        <td>${donor.gender}</td>
                        <td>${donor.birthday}</td>
                        <td>${donor.address}</td>
                        <td>${donor.phonenumber}</td>
                        <td>${donor.polis}</td>
                        <td>${donor.bloodgroup}</td>
                        <td>${donor.rhfactor}</td>
                        <td style="display:flex;gap:10px;align-items:center;">
                            <button onclick="prepareEditModal('${donor.passportdata}', '${donor.institutioncode}')">Изменить</button>
                            <button onclick="openHistoryModal('${donor.passportdata}', '${donor.institutioncode}')">История</button>
                        </td>
                    `;
                    row.addEventListener('click', (e) => {
                        if (e.target.tagName === 'BUTTON') return;
                        if (selectedRow) selectedRow.classList.remove('selected');
                        selectedRow = row;
                        row.classList.add('selected');
                    });
                    donorsTable.appendChild(row);
                });
            }
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
            console.error('Ошибка:', error);
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = `<tr><td colspan="11" style="text-align: center; color: red;">Ошибка загрузки данных</td></tr>`;
            document.getElementById('loading').style.display = 'none';
        });
}

function getSelectedDonor() {
    if (!selectedRow) return null;
    const fio = selectedRow.cells[2].textContent.split(' ');
    return {
        institutionname: selectedRow.cells[0].textContent,
        passportdata: selectedRow.cells[1].textContent,
        surname: fio[0],
        name: fio[1],
        secondname: fio[2] || '',
        gender: selectedRow.cells[3].textContent,
        birthday: selectedRow.cells[4].textContent,
        address: selectedRow.cells[5].textContent,
        phonenumber: selectedRow.cells[6].textContent,
        polis: selectedRow.cells[7].textContent,
        bloodgroup: selectedRow.cells[8].textContent,
        rhfactor: selectedRow.cells[9].textContent
    };
}

document.addEventListener('DOMContentLoaded', () => {
    if (getShouldGetDonorsState()) getDonors();
});

function renderDonorRow(donor) {
    return `
        <tr>
            <td>${donor.institutionName}</td>
            <td>${donor.passportData}</td>
            <td>${donor.secondName} ${donor.name} ${donor.surName || ''}</td>
            <td>${donor.gender === 'M' ? 'М' : 'Ж'}</td>
            <td>${donor.birthday}</td>
            <td>${donor.address || ''}</td>
            <td>${donor.phoneNumber || ''}</td>
            <td>${donor.polis || ''}</td>
            <td>${donor.bloodGroup}</td>
            <td>${donor.rhFactor}</td>
            <td class="actions">
                <button onclick="editDonorModal('${donor.passportData}', ${donor.institutionCode})">✏️</button>
                <button onclick="deleteDonor('${donor.passportData}', ${donor.institutionCode})">🗑️</button>
                <button onclick="openHistoryModal('${donor.passportData}', ${donor.institutionCode})">📜 История</button>
            </td>
        </tr>
    `;
}