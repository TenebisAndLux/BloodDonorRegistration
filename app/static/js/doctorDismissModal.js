function closeDismissModal() {
    document.getElementById('dismissModal').style.display = 'none';
}

function confirmDismissal() {
    const institutionCode = document.getElementById('dismissModal').dataset.institutionCode;
    const serviceNumber = document.getElementById('dismissModal').dataset.serviceNumber;
    const transferTo = document.getElementById('transferToDoctor').value;

    if (!transferTo) {
        alert('Пожалуйста, выберите врача для передачи записей');
        return;
    }

    const [transferInstitutionCode, transferServiceNumber] = transferTo.split('|');

    fetch('/doctor/dismiss', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
            institutioncode: institutionCode,
            servicenumber: serviceNumber,
            transfer_institutioncode: transferInstitutionCode,
            transfer_servicenumber: transferServiceNumber
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeDismissModal();
            loadDoctors();
        } else {
            alert(data.message || 'Ошибка при увольнении врача');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при увольнении врача');
    });
}