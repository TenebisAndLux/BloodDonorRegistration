// Открывает модальное окно
function addDonorModal() {
    document.getElementById('addDonorModal').style.display = 'block';
}

// Закрывает модальное окно
function closeAddModal() {
    document.getElementById('addDonorModal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addDonorForm');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(form);  
        const dateOfBirthInput = document.getElementById('addDonorDateOfBirth').valueAsDate;  
        formData.set('addDonorDateOfBirth', dateOfBirthInput.toISOString().split('T')[0]);  
        try {
            const response = await fetch(`/donor/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(Object.fromEntries(formData))
            });
            if (response.ok) {
                closeAddModal();
                getDonors();
                addMedicalHistory('add')
            } else {
                throw new Error(`Error adding donor data.`);
            }
        } catch (error) {
            console.error('Error adding donor data:', error);
        }
    });
});