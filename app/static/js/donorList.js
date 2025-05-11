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

document.addEventListener('DOMContentLoaded', () => {
    if (getShouldGetDonorsState()) getDonors();
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        setFalseShouldGetDonorsState();
        handleSearchForm();
    });
    searchDonors();
});

function handleSearchForm() {
    const form = document.getElementById('search-form');
    const formData = new FormData(form);
    const params = {
        surname: formData.get('surname'),
        name: formData.get('name'),
        secondname: formData.get('secondname'),
        address: formData.get('address'),
        phonenumber: formData.get('phonenumber'),
        polis: formData.get('polis'),
        birthday: formData.get('birthday'),
        bloodgroup: formData.get('bloodgroup'),
        rhfactor: formData.get('rhfactor')
    };

    searchDonors(params);
}