async function prepareEditModal(passportData, institutionCode) {
    document.getElementById('loading').style.display = 'block';
    try {
        const response = await fetch(`/donor/search/${passportData}/${institutionCode}`);
        if (!response.ok) throw new Error('Ошибка загрузки данных донора');

        const donor = await response.json();

        // Сохраняем старые значения
        document.getElementById('editOldDonorPassportData').value = donor.passportdata;
        document.getElementById('editOldDonorInstitutionCode').value = donor.institutioncode;

        // Заполняем текущие значения
        document.getElementById('editDonorPassportData').value = donor.passportdata;
        document.getElementById('editDonorInstitutionCode').value = donor.institutioncode;
        document.getElementById('editDonorName').value = donor.name;
        document.getElementById('editDonorSecondName').value = donor.secondname;
        document.getElementById('editDonorSurname').value = donor.surname;
        document.getElementById('editDonorBirthday').value = donor.birthday;
        document.getElementById('editDonorGender').value = donor.gender;
        document.getElementById('editDonorAddress').value = donor.address;
        document.getElementById('editDonorPhoneNumber').value = donor.phonenumber;
        document.getElementById('editDonorPolis').value = donor.polis;
        document.getElementById('editDonorBloodGroup').value = donor.bloodgroup;
        document.getElementById('editDonorRhFactor').value = donor.rhfactor;

        document.getElementById('editDonorModal').style.display = 'block';
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить данные донора.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function closeEditModal() {
    document.getElementById('editDonorModal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('editDonorForm');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        document.getElementById('loading').style.display = 'block';

        const formData = {
            old_passportdata: document.getElementById('editOldDonorPassportData').value,
            old_institutioncode: document.getElementById('editOldDonorInstitutionCode').value,
            passportdata: document.getElementById('editDonorPassportData').value,
            institutioncode: document.getElementById('editDonorInstitutionCode').value,
            name: document.getElementById('editDonorName').value,
            secondname: document.getElementById('editDonorSecondName').value,
            surname: document.getElementById('editDonorSurname').value,
            birthday: document.getElementById('editDonorBirthday').value,
            gender: document.getElementById('editDonorGender').value,
            address: document.getElementById('editDonorAddress').value,
            phonenumber: document.getElementById('editDonorPhoneNumber').value,
            polis: document.getElementById('editDonorPolis').value,
            bloodgroup: document.getElementById('editDonorBloodGroup').value,
            rhfactor: document.getElementById('editDonorRhFactor').value
        };

        const errors = validateEditDonorData(formData);
        if (errors) {
            alert('Ошибки валидации:\n' + errors.join('\n'));
            document.getElementById('loading').style.display = 'none';
            return;
        }

        try {
            const response = await fetch('/donor/edit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка при обновлении данных донора');
            }

            const result = await response.json();
            closeEditModal();
            searchDonors(); // Обновление таблицы
            alert(result.message || 'Данные донора успешно обновлены!');
        } catch (error) {
            console.error('Ошибка:', error);
            alert(`Ошибка: ${error.message}`);
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    });
});

function validateEditDonorData(data) {
    const requiredFields = ['passportdata', 'name', 'secondname', 'birthday', 'bloodgroup', 'rhfactor'];
    const errors = [];

    requiredFields.forEach(field => {
        if (!data[field]) errors.push(`Поле "${field}" обязательно для заполнения`);
    });

    if (!/^\d+$/.test(data.passportdata)) errors.push('Паспортные данные должны содержать только цифры');
    if (data.phonenumber && !/^\+?\d{7,15}$/.test(data.phonenumber)) errors.push('Неверный формат телефона');
    return errors.length ? errors : null;
}