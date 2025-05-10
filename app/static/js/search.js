async function searchDonors(params = {}) {
    const searchParams = new URLSearchParams();

    Object.keys(params).forEach(key => {
        if (params[key]) {
            searchParams.append(key, params[key]);
        }
    });

    try {
        const response = await fetch('/donor/list/search?' + searchParams.toString());
        if (!response.ok) {
            throw new Error('Ошибка сети');
        }
        const donors = await response.json();

        const donorsTable = document.getElementById('donors');
        donorsTable.innerHTML = '';

        if (donors.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="9" style="text-align: center;">Ничего не найдено</td>`;
            donorsTable.appendChild(row);
            return;
        }

        donors.forEach(donor => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${donor.passportdata}</td>
                <td>${donor.surname} ${donor.name} ${donor.secondname || ''}</td>
                <td>${donor.birthday}</td>
                <td>${donor.address}</td>
                <td>${donor.phonenumber}</td>
                <td>${donor.polis}</td>
                <td>${donor.bloodgroup}</td>
                <td>${donor.rhfactor}</td>
                <td>
                    <button onclick="prepareEditModal('${donor.passportdata}', '${donor.institutioncode}')">Редактировать</button>
                </td>
            `;

            row.addEventListener('click', (e) => {
                if (e.target.tagName !== 'BUTTON') {
                    document.querySelectorAll('#donors tr').forEach(r => r.classList.remove('selected'));
                    row.classList.add('selected');
                }
            });

            donorsTable.appendChild(row);
        });

    } catch (error) {
        console.error('Ошибка при поиске доноров:', error);
        const donorsTable = document.getElementById('donors');
        donorsTable.innerHTML = `
            <tr>
                <td colspan="9" style="text-align: center; color: red;">
                    Ошибка при загрузке данных. Пожалуйста, попробуйте позже.
                </td>
            </tr>
        `;
    }
}

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

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        setFalseShouldGetDonorsState();
        handleSearchForm();
    });
    searchDonors();
});