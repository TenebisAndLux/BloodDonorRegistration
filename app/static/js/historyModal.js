function openHistoryModal(passportData, institutionCode) {
    fetch(`/donor/history?passport=${passportData}&institution=${institutionCode}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('historyModal');
            const content = document.getElementById('historyContent');

            let html = `
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Дата забора</th>
                            <th>Тип забора</th>
                            <th>Объем</th>
                            <th>Врач</th>
                            <th>Результаты обследования</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.history.forEach(item => {
                html += `
                    <tr>
                        <td>${item.date}</td>
                        <td>${item.type}</td>
                        <td>${item.volume} мл</td>
                        <td>${item.doctor}</td>
                        <td><textarea class="history-notes">${item.notes}</textarea></td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            content.innerHTML = html;
            modal.style.display = 'block';
        });
}

function closeHistoryModal() {
    document.getElementById('historyModal').style.display = 'none';
}

function saveHistory() {
    closeHistoryModal();
}