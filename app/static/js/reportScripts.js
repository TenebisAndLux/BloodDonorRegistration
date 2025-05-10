function generateReport(reportType) {
    let formId = `report${reportType}-form`;
    let form = document.getElementById(formId);
    let formData = new FormData(form);
    let previewId = `preview-content-${reportType}`;
    let preview = document.getElementById(previewId);

    // Показываем загрузку
    preview.innerHTML = '<p class="loading">Генерация отчета...</p>';

    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/reports/generate_report_${reportType}`, true);
    xhr.setRequestHeader('X-CSRF-TOKEN', formData.get('csrf_token'));
    xhr.responseType = 'blob';

    xhr.onload = function() {
        if (xhr.status === 200) {
            let blob = new Blob([xhr.response], {
                type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            });

            // Обновляем предпросмотр
            preview.innerHTML = `
                <div class="report-preview-success">
                    <p>Отчет успешно сгенерирован!</p>
                    <button onclick="downloadReport(${reportType})">Скачать отчет</button>
                </div>
            `;

            // Сохраняем blob для последующего скачивания
            sessionStorage.setItem(`report_${reportType}_blob`, URL.createObjectURL(blob));
        } else {
            preview.innerHTML = `
                <div class="report-preview-error">
                    <p>Ошибка при генерации отчета (код ${xhr.status})</p>
                    <button onclick="generateReport(${reportType})">Повторить</button>
                </div>
            `;
        }
    };

    xhr.onerror = function() {
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка связи с сервером</p>
                <button onclick="generateReport(${reportType})">Повторить</button>
            </div>
        `;
    };

    xhr.send(formData);
}

function downloadReport(reportType) {
    let blobUrl = sessionStorage.getItem(`report_${reportType}_blob`);
    if (blobUrl) {
        let link = document.createElement('a');
        link.href = blobUrl;
        link.download = `report_${reportType}_${new Date().toISOString().slice(0,10)}.docx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}