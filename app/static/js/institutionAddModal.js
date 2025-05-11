function openAddInstitutionModal() {
    document.getElementById('addInstitutionForm').reset();
    document.getElementById('addInstitutionModal').style.display = 'block';
}

function closeAddInstitutionModal() {
    document.getElementById('addInstitutionModal').style.display = 'none';
}

document.getElementById('addInstitutionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        nameofinstitution: document.getElementById('addInstitutionName').value,
        typeofinstitution: document.getElementById('addInstitutionType').value,
        address: document.getElementById('addInstitutionAddress').value,
        contactphonenumber: document.getElementById('addInstitutionPhone').value,
        email: document.getElementById('addInstitutionEmail').value
    };

    fetch('/medical_institution/add', {
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
            closeAddInstitutionModal();
            loadInstitutions();
        } else {
            alert(data.error || 'Ошибка при добавлении учреждения');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.error || 'Произошла ошибка при добавлении учреждения');
    });
});