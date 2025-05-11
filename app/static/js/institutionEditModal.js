function openEditInstitutionModal(institutioncode) {
    fetch(`/medical_institution/${institutioncode}`)
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при получении данных учреждения');
            return response.json();
        })
        .then(data => {
            document.getElementById('editInstitutionCode').value = data.institutioncode;
            document.getElementById('editInstitutionName').value = data.nameofinstitution;
            document.getElementById('editInstitutionType').value = data.typeofinstitution;
            document.getElementById('editInstitutionAddress').value = data.address;
            document.getElementById('editInstitutionPhone').value = data.contactphonenumber;
            document.getElementById('editInstitutionEmail').value = data.email;

            document.getElementById('editInstitutionModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Не удалось загрузить данные учреждения');
        });
}

function closeEditInstitutionModal() {
    document.getElementById('editInstitutionModal').style.display = 'none';
}

document.getElementById('editInstitutionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const institutioncode = document.getElementById('editInstitutionCode').value;
    const formData = {
        nameofinstitution: document.getElementById('editInstitutionName').value,
        typeofinstitution: document.getElementById('editInstitutionType').value,
        address: document.getElementById('editInstitutionAddress').value,
        contactphonenumber: document.getElementById('editInstitutionPhone').value,
        email: document.getElementById('editInstitutionEmail').value
    };

    fetch(`/medical_institution/${institutioncode}`, {
        method: 'PUT',
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
            closeEditInstitutionModal();
            loadInstitutions();
        } else {
            alert(data.error || 'Ошибка при обновлении учреждения');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.error || 'Произошла ошибка при обновлении учреждения');
    });
});