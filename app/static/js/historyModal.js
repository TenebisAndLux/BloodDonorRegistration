let currentHistoryData = null;

function openHistoryModal(passportData, institutionCode) {
    fetch(`/donor/history?passport=${passportData}&institution=${institutionCode}`)
        .then(response => response.json())
        .then(data => {
            currentHistoryData = data;
            const modal = document.getElementById('historyModal');
            const medicalHistoryContent = document.getElementById('medicalHistoryContent');
            const bloodCollectionHistory = document.getElementById('bloodCollectionHistory');

            // Заполняем данные MedicalHistory
            document.getElementById('historyNumber').textContent = data.medicalHistory.historynumber || 'Нет данных';
            document.getElementById('passportDetails').textContent = data.medicalHistory.passportdetails || 'Нет данных';
            document.getElementById('dateOfLastExamination').textContent = data.medicalHistory.dateoflastexamination || 'Нет данных';
            document.getElementById('analysisResults').value = data.medicalHistory.analysisresults || '';
            document.getElementById('banOnDonation').checked = data.medicalHistory.banondonation || false;

            // Если есть запрет на донацию, выделяем визуально
            if (data.medicalHistory.banondonation) {
                medicalHistoryContent.classList.add('ban-warning');
            } else {
                medicalHistoryContent.classList.remove('ban-warning');
            }

            // Заполняем таблицу истории сборов крови
            let html = '';
            data.bloodCollections.forEach(item => {
                html += `
                    <tr>
                        <td>${item.date}</td>
                        <td>${item.type}</td>
                        <td>${item.volume} мл</td>
                        <td>${item.doctor}</td>
                        <td><textarea class="history-notes" data-id='${JSON.stringify(item.id)}'>${item.notes}</textarea></td>
                    </tr>
                `;
            });
            bloodCollectionHistory.innerHTML = html;

            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Ошибка загрузки истории:', error);
            alert('Не удалось загрузить историю донора');
        });
}

function closeHistoryModal() {
    document.getElementById('historyModal').style.display = 'none';
}

function saveHistory() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const updatedData = {
        historynumber: currentHistoryData.medicalHistory.historynumber,
        analysisresults: document.getElementById('analysisResults').value,
        banondonation: document.getElementById('banOnDonation').checked,
        bloodCollections: []
    };

    // Собираем обновленные результаты обследований
    document.querySelectorAll('.history-notes').forEach(textarea => {
        const id = JSON.parse(textarea.dataset.id);
        console.log(id);
        if (!id.bloodsupplycollectiontypecode || !id.bloodbankinstitutioncode || !id.numberstock || !id.number) {
            console.error('Invalid id format:', id);
            alert('Ошибка: некорректный формат id коллекции');
            return;
        }
        updatedData.bloodCollections.push({
            id: id,
            notes: textarea.value
        });
    });

    fetch('/donor/history/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'X-CSRF-Token': csrfToken
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('История успешно сохранена');
            closeHistoryModal();
        } else {
            alert(data.error || 'Ошибка при сохранении');
        }
    })
    .catch(error => {
        console.error('Ошибка сохранения:', error);
        alert('Не удалось сохранить изменения');
    });
}