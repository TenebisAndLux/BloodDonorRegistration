function addMedicalHistory() {
    const selectedRow = document.querySelector('tr.selected');
    const donorId = parseInt(selectedRow.querySelector('td:first-child').innerText);
    const lastExaminationDate = new Date().toISOString();
    const testResults = 'Normal';
    const donationBan = testResults === 'Normal' ? false : true;
    
    fetch('/medical_history/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            donor_id: donorId,
            last_examination_date: lastExaminationDate,
            test_results: testResults,
            donation_ban: donationBan
        })
    })
    .then(() => {
        getMedicalHistory();
    })
    .catch(error => console.error(error));
}