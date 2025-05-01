// Функции для кнопки выхода
function showLogoutButton() {
    document.querySelector(".exit-button").style.display = "block";
}

function hideLogoutButton() {
    setTimeout(function () {
        if (!document.querySelector(".name-container:hover") && !document.querySelector(".exit-button:hover")) {
            document.querySelector(".exit-button").style.display = "none";
        }
    }, 500);
}

// Функция для загрузки данных текущего врача
// Обновленный код для index_scripts.js
function loadCurrentDoctor() {
    fetch('/doctor/current')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка загрузки данных врача');
            }
            return response.json();
        })
        .then(data => {
            // Устанавливаем имя врача
            const doctorNameElement = document.getElementById('doctor-name');
            if (data.surname && data.name) {
                const initials = `${data.name.charAt(0)}.${data.secondname ? data.secondname.charAt(0) + '.' : ''}`;
                doctorNameElement.textContent = `${data.surname} ${initials}`;
            }

            // Устанавливаем название учреждения
            const hospitalNameElement = document.getElementById('hospital-name');
            if (data.institutionname) {
                hospitalNameElement.textContent = data.institutionname;
                hospitalNameElement.dataset.institutionCode = data.institutioncode; // Сохраняем код учреждения
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            document.getElementById('doctor-name').textContent = 'Неизвестный пользователь';
            document.getElementById('hospital-name').textContent = 'Медицинское учреждение';
        });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentDoctor();

    // Проверяем, нужно ли загружать список доноров сразу
    if (localStorage.getItem('shouldGetDonors') !== 'false') {
        getDonors();
    }
});