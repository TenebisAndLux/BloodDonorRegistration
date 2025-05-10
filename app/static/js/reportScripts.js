async function generateReport(reportType) {
    const formId = `report${reportType}-form`;
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const previewId = `preview-content-${reportType}`;
    const preview = document.getElementById(previewId);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    // Добавляем флаг предпросмотра
    formData.append('preview', 'true');

    try {
        // Показываем загрузку
        preview.innerHTML = '<p class="loading">Генерация предпросмотра...</p>';

        // Запрос на предпросмотр
        const previewResponse = await fetch(`/reports/generate_report_${reportType}`, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken
            },
            body: formData
        });

        if (!previewResponse.ok) {
            throw new Error(`Ошибка HTTP: ${previewResponse.status}`);
        }

        const previewData = await previewResponse.json();

        // Отображаем предпросмотр
        preview.innerHTML = `
            <div class="report-preview">
                <h4>Предпросмотр отчета</h4>
                ${reportType === 1 ? `
                    <p><strong>Донор:</strong> ${previewData.donor_name}</p>
                    <p><strong>Учреждение:</strong> ${previewData.institution}</p>
                    <p><strong>Дата сдачи крови:</strong> ${previewData.collection_date}</p>
                    <p><strong>Объем крови:</strong> ${previewData.blood_volume} мл</p>
                ` : `
                    <p><strong>Учреждение:</strong> ${previewData.institution}</p>
                    <p><strong>Период:</strong> ${previewData.period}</p>
                    <p><strong>Количество доноров:</strong> ${previewData.total_donors}</p>
                `}
                <button onclick="downloadFullReport(${reportType})">Скачать полный отчет</button>
            </div>
        `;

    } catch (error) {
        console.error('Ошибка:', error);
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка при генерации отчета: ${error.message}</p>
                <button onclick="generateReport(${reportType})">Повторить</button>
            </div>
        `;
    }
}

async function downloadFullReport(reportType) {
    const formId = `report${reportType}-form`;
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const previewId = `preview-content-${reportType}`;
    const preview = document.getElementById(previewId);

    try {
        // Убираем флаг предпросмотра для получения файла
        formData.delete('preview');

        // Показываем загрузку
        preview.innerHTML = '<p class="loading">Подготовка файла для скачивания...</p>';

        const response = await fetch(`/reports/generate_report_${reportType}`, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Автоматическое скачивание
        const a = document.createElement('a');
        a.href = url;
        a.download = `report_${reportType}_${new Date().toISOString().slice(0,10)}.docx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Обновляем предпросмотр
        preview.innerHTML += `
            <div class="report-success">
                <p>Файл успешно скачан!</p>
            </div>
        `;

    } catch (error) {
        console.error('Ошибка:', error);
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка при скачивании отчета: ${error.message}</p>
                <button onclick="downloadFullReport(${reportType})">Повторить</button>
            </div>
        `;
    }
}