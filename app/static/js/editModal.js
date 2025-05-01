// Подготавливает модальное окно редактирования с данными выбранного донора
async function prepareEditModal(passportData, institutionCode) {
    try {
        const response = await fetch(`/donor/search/${passportData}/${institutionCode}`);
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных донора');
        }
        
        const donor = await response.json();
        
        // Заполняем форму данными донора
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
        
        // Открываем модальное окно
        document.getElementById('editDonorModal').style.display = 'block';
    } catch (error) {
        console.error('Ошибка при загрузке данных донора:', error);
        alert('Не удалось загрузить данные донора. Пожалуйста, попробуйте позже.');
    }
}

// Закрывает модальное окно редактирования
function closeEditModal() {
    document.getElementById('editDonorModal').style.display = 'none';
}

// Обработчик отправки формы редактирования
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('editDonorForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        // Получаем данные из формы
        const formData = {
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

        try {
            const response = await fetch(`/donor/edit/${formData.passportdata}/${formData.institutioncode}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка при обновлении данных донора');
            }

            // Закрываем модальное окно и обновляем список
            closeEditModal();
            getDonors();
            
            // Показываем уведомление об успехе
            alert('Данные донора успешно обновлены!');
            
        } catch (error) {
            console.error('Ошибка при обновлении данных донора:', error);
            alert(`Ошибка: ${error.message}`);
        }
    });
});

// Вспомогательная функция для валидации данных при редактировании
function validateEditDonorData(data) {
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