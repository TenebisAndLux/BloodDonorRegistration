function getMedicalHistory() {
    fetch('/medical_history/get')
        .then(response => response.json())
        .then(medical_history => {
            const medicalHistoryTable = document.getElementById('donors-history');
            medicalHistoryTable.innerHTML = '';
            for (const donor of medical_history) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donor.donor_id}</td>
                    <td>${donor.hospital_affiliation}</td>
                    <td>${donor.first_name} ${donor.last_name}</td>
                    <td>${donor.insurance_data}</td>
                    <td>${donor.test_results}</td>
                    <td>${donor.donation_ban ? 'Да' : 'Нет'}</td>
                    <td>${donor.last_examination_date}</td>
                `;
                medicalHistoryTable.appendChild(row);
            }
        })
        .catch(error => console.error(error));
}

document.addEventListener('DOMContentLoaded', getMedicalHistory);
document.addEventListener('reload', getMedicalHistory);