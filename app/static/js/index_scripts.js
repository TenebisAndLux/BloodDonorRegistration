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

function loadCurrentDoctor() {
    document.getElementById('loading').style.display = 'block';
    fetch('/doctor/current')
        .then(response => {
            if (!response.ok) throw new Error('Ошибка загрузки данных врача');
            return response.json();
        })
        .then(data => {
            const doctorNameElement = document.getElementById('doctor-name');
            const hospitalNameElement = document.getElementById('hospital-name');

            if (data.secondname && data.name) {
                    const initials = `${data.name.charAt(0)}.`;
                    doctorNameElement.textContent = `${data.secondname} ${initials}`;
            } else {
                doctorNameElement.textContent = 'Неизвестный пользователь';
            }
            if (data.institutionname) {
                hospitalNameElement.textContent = data.institutionname;
                hospitalNameElement.dataset.institutionCode = data.institutioncode;
            } else {
                hospitalNameElement.textContent = 'Медицинское учреждение';
            }
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
            console.error('Ошибка:', error);
            document.getElementById('doctor-name').textContent = 'Ошибка загрузки';
            document.getElementById('hospital-name').textContent = 'Ошибка загрузки';
            document.getElementById('loading').style.display = 'none';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    loadCurrentDoctor();
    if (localStorage.getItem('shouldGetDonors') !== 'false') getDonors();
});