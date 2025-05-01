let selectedRow = null;

// Функция для получения и отображения списка доноров
function getDonors() {
    if (!getShouldGetDonorsState()) return;

    fetch('/donor/list/get?order=asc')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка загрузки списка доноров');
            }
            return response.json();
        })
        .then(donors => {
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '';

            if (donors.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = `<td colspan="9" style="text-align: center;">Нет данных о донорах</td>`;
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

                // Обработчик клика для выделения строки
                row.addEventListener('click', (e) => {
                    // Не выделяем если кликнули на кнопку
                    if (e.target.tagName === 'BUTTON') return;

                    if (selectedRow) {
                        selectedRow.classList.remove('selected');
                    }
                    selectedRow = row;
                    row.classList.add('selected');
                });

                donorsTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ошибка:', error);
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = `
                <tr>
                    <td colspan="9" style="text-align: center; color: red;">
                        Ошибка загрузки данных. Пожалуйста, попробуйте позже.
                    </td>
                </tr>
            `;
        });
}

// Получение выбранного донора
function getSelectedDonor() {
    if (!selectedRow) return null;

    return {
        passportdata: selectedRow.cells[0].textContent,
        surname: selectedRow.cells[1].textContent.split(' ')[0],
        name: selectedRow.cells[1].textContent.split(' ')[1],
        secondname: selectedRow.cells[1].textContent.split(' ')[2] || '',
        birthday: selectedRow.cells[2].textContent,
        address: selectedRow.cells[3].textContent,
        phonenumber: selectedRow.cells[4].textContent,
        polis: selectedRow.cells[5].textContent,
        bloodgroup: selectedRow.cells[6].textContent,
        rhfactor: selectedRow.cells[7].textContent
    };
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    if (getShouldGetDonorsState()) {
        getDonors();
    }
});

// Обновление списка при событии reload
document.addEventListener('reload', getDonors);