function addDoctorModal() {
    document.getElementById('addDoctorModal').style.display = 'block';
}

function closeAddModal() {
    document.getElementById('addDoctorModal').style.display = 'none';
}

document.getElementById('addDoctorForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('addDoctorName').value,
        secondname: document.getElementById('addDoctorSecondName').value,
        jobtitle: document.getElementById('addDoctorJobTitle').value,
        role: document.getElementById('addDoctorRole').value,
        login: document.getElementById('addDoctorLogin').value,
        password: document.getElementById('addDoctorPassword').value,
        email: document.getElementById('addDoctorEmail').value
    };

    fetch('/doctor/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            closeAddModal();
            loadDoctors();
            // Очистка формы после успешного добавления
            document.getElementById('addDoctorForm').reset();
        } else {
            alert(data.error || 'Ошибка при добавлении врача');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.error || 'Произошла ошибка при добавлении врача');
    });
});