function closeEditModal() {
    document.getElementById('editDoctorModal').style.display = 'none';
}

document.getElementById('editDoctorForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        institutioncode: document.getElementById('editDoctorInstitutionCode').value,
        servicenumber: document.getElementById('editDoctorServiceNumber').value,
        name: document.getElementById('editDoctorName').value,
        secondname: document.getElementById('editDoctorSecondName').value,
        jobtitle: document.getElementById('editDoctorJobTitle').value,
        role: document.getElementById('editDoctorRole').value,
        login: document.getElementById('editDoctorLogin').value,
        password: document.getElementById('editDoctorPassword').value,
        email: document.getElementById('editDoctorEmail').value
    };

    fetch('/doctor/edit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeEditModal();
            loadDoctors();
        } else {
            alert(data.message || 'Ошибка при редактировании врача');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при редактировании врача');
    });
});