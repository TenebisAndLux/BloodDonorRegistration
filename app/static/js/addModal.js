// Открывает модальное окно добавления донора
function addDonorModal() {
    // Сброс формы перед открытием
    document.getElementById('addDonorForm').reset();
    document.getElementById('addDonorModal').style.display = 'block';
}

// Закрывает модальное окно
function closeAddModal() {
    document.getElementById('addDonorModal').style.display = 'none';
}

// Инициализация формы добавления донора
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addDonorForm');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Получаем данные из формы
        const formData = {
            passportdata: document.getElementById('addDonorPassportData').value,
            institutioncode: document.getElementById('hospital-name').dataset.institutionCode || 1, // Получаем из скрытого поля или по умолчанию
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

        try {
            const response = await fetch('/donor/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка при добавлении донора');
            }

            const result = await response.json();

            // Закрываем модальное окно и обновляем список
            closeAddModal();
            getDonors();

            // Показываем уведомление об успехе
            alert(`Донор успешно добавлен! ID: ${result.id}`);

        } catch (error) {
            console.error('Ошибка при добавлении донора:', error);
            alert(`Ошибка: ${error.message}`);
        }
    });
});

// Вспомогательная функция для валидации данных
function validateDonorData(data) {
    const requiredFields = ['passportdata', 'name', 'secondname', 'birthday', 'bloodgroup', 'rhfactor'];
    const errors = [];

    requiredFields.forEach(field => {
        if (!data[field]) {
            errors.push(`Поле ${field} обязательно для заполнения`);
        }
    });

    if (isNaN(data.passportdata)) {
        errors.push('Паспортные данные должны быть числом');
    }

    return errors.length ? errors : null;
}