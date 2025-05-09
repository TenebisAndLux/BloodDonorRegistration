function addMedicalHistory(type) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    let donorId;

    if (type === 'edit') {
        const selectedRow = document.querySelector('tr.selected');
        const donorIdInput = selectedRow.querySelector('td:first-child');
        donorId = parseInt(donorIdInput.innerText);

        const lastExaminationDate = new Date().toISOString();
        const testResults = 'Normal';
        const donationBan = testResults !== 'Normal';

        fetch('/medical_history/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
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
        .catch(error => {
            console.error(error);
            alert('Не удалось добавить историю. id:' + donorId);
        });

    } else {
        fetch('/donor/list/get/last')
            .then(response => response.json())
            .then(data => {
                donorId = data.last_id;
                const lastExaminationDate = new Date().toISOString();
                const testResults = 'Normal';
                const donationBan = testResults !== 'Normal';

                return fetch('/medical_history/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': csrfToken
                    },
                    body: JSON.stringify({
                        donor_id: donorId,
                        last_examination_date: lastExaminationDate,
                        test_results: testResults,
                        donation_ban: donationBan
                    })
                });
            })
            .then(() => {
                getMedicalHistory();
            })
            .catch(error => {
                console.error(error);
                alert('Не удалось добавить историю. id:' + donorId);
            });
    }
}
