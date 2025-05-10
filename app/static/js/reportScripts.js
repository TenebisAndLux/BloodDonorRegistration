function generateReport(reportType) {
    let formId = `report${reportType}-form`;
    let form = document.getElementById(formId);
    let formData = new FormData(form);
    let previewId = `preview-content-${reportType}`;
    let preview = document.getElementById(previewId);
    let csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    // Показываем загрузку
    preview.innerHTML = '<p class="loading">Генерация отчета...</p>';

    fetch(`/reports/generate_report_${reportType}`, {
        method: 'POST',
        headers: {
            'X-CSRF-Token': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.blob();
    })
    .then(blob => {
        // Обновляем предпросмотр
        preview.innerHTML = `
            <div class="report-preview-success">
                <p>Отчет успешно сгенерирован!</p>
                <button onclick="downloadReport(${reportType})">Скачать отчет</button>
            </div>
        `;

        // Сохраняем blob для последующего скачивания
        let blobUrl = URL.createObjectURL(blob);
        sessionStorage.setItem(`report_${reportType}_blob`, blobUrl);
    })
    .catch(error => {
        console.error('Ошибка генерации отчета:', error);
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка при генерации отчета: ${error.message}</p>
                <button onclick="generateReport(${reportType})">Повторить</button>
            </div>
        `;
    });
}

function downloadReport(reportType) {
    let blobUrl = sessionStorage.getItem(`report_${reportType}_blob`);
    if (blobUrl) {
        let link = document.createElement('a');
        link.href = blobUrl;
        link.download = `report_${reportType}_${new Date().toISOString().slice(0, 10)}.docx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        sessionStorage.removeItem(`report_${reportType}_blob`);
        URL.revokeObjectURL(blobUrl);
    }
}