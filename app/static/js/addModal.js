function addDonorModal() {
    document.getElementById('addDonorForm').reset();
    document.getElementById('addDonorModal').style.display = 'block';
}

function closeAddModal() {
    document.getElementById('addDonorModal').style.display = 'none';
    document.getElementById('error-message') && (document.getElementById('error-message').textContent = '');
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addDonorForm');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        document.getElementById('loading').style.display = 'block';

        const formData = {
            passportdata: document.getElementById('addDonorPassportData').value,
            institutioncode: document.getElementById('hospital-name').dataset.institutionCode || 1,
            name: document.getElementById('addDonorName').value,
            secondname: document.getElementById('addDonorSecondName').value,
            surname: document.getElementById('addDonorSurname').value,
            birthday: document.getElementById('addDonorBirthday').value,
            gender: document.getElementById('addDonorGender').value,
            address: document.getElementById('addDonorAddress').value,
            phonenumber: document.getElementById('addDonorPhoneNumber').value,
            polis: document.getElementById('addDonorPolis').value,
            bloodgroup: document.getElementById('addDonorBloodGroup').value,
            rhfactor: document.getElementById('addDonorRhFactor').value
        };

        const errors = validateDonorData(formData);
        if (errors) {
            alert('Ошибки валидации:\n' + errors.join('\n'));
            document.getElementById('loading').style.display = 'none';
            return;
        }

        try {
            const response = await fetch('/donor/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка при добавлении донора');
            }

            const result = await response.json();
            closeAddModal();
            searchDonors(); // Обновление таблицы с учетом текущих фильтров
            alert(`Донор успешно добавлен! ID: ${result.id}`);
        } catch (error) {
            console.error('Ошибка:', error);
            if (error.message.includes('duplicate') || error.message.includes('уже существует')) {
                alert('Донор с таким паспортом уже существует.');
            } else {
                alert(`Ошибка: ${error.message}`);
            }
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    });
});

function validateDonorData(data) {
    const requiredFields = ['passportdata', 'name', 'secondname', 'birthday', 'bloodgroup', 'rhfactor'];
    const errors = [];

    requiredFields.forEach(field => {
        if (!data[field]) errors.push(`Поле "${field}" обязательно для заполнения`);
    });

    if (!/^\d+$/.test(data.passportdata)) errors.push('Паспортные данные должны содержать только цифры');
    if (data.phonenumber && !/^\+?\d{7,15}$/.test(data.phonenumber)) errors.push('Неверный формат телефона');
    return errors.length ? errors : null;
}