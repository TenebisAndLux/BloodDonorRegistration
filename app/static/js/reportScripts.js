// Функция генерации отчета
function generateReport(reportType) {
    // Здесь будет логика формирования отчета на основе выбранных параметров
    const previewContent = document.getElementById('preview-content');

    // Временная заглушка для демонстрации
    let reportHtml = '<h4>Отчет ' + reportType + '</h4><p>Сформирован: ' + new Date().toLocaleString() + '</p>';

    switch(reportType) {
        case 1:
            const institution = document.getElementById('institution-select').value;
            const date = document.getElementById('report1-date').value;
            reportHtml += '<p>Учреждение: ' + institution + '</p>';
            reportHtml += '<p>На дату: ' + date + '</p>';
            reportHtml += generateSampleDonorData();
            break;
        case 2:
            reportHtml += generateSampleBloodSupplyData();
            break;
        // Остальные типы отчетов...
    }

    previewContent.innerHTML = reportHtml;
}

// Функция экспорта отчета
function exportReport(reportType, format) {
    alert('Экспорт отчета ' + reportType + ' в формате ' + format.toUpperCase());
    // Здесь будет логика экспорта
}

// Вспомогательные функции для генерации демо-данных
function generateSampleDonorData() {
    return `
        <table class="report-table">
            <thead>
                <tr>
                    <th>ФИО</th>
                    <th>Группа крови</th>
                    <th>Дата последней сдачи</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Иванов И.И.</td>
                    <td>A+</td>
                    <td>15.10.2023</td>
                </tr>
                <tr>
                    <td>Петрова А.С.</td>
                    <td>B-</td>
                    <td>10.10.2023</td>
                </tr>
            </tbody>
        </table>
    `;
}

function generateSampleBloodSupplyData() {
    return `
        <table class="report-table">
            <thead>
                <tr>
                    <th>Группа крови</th>
                    <th>Резус-фактор</th>
                    <th>Объем (л)</th>
                    <th>Срок годности</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>A</td>
                    <td>+</td>
                    <td>15.5</td>
                    <td>01.11.2023</td>
                </tr>
                <tr>
                    <td>B</td>
                    <td>-</td>
                    <td>8.2</td>
                    <td>25.10.2023</td>
                </tr>
            </tbody>
        </table>
    `;
}