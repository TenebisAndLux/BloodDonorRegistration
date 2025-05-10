async function generateReport(reportType) {
    const formId = `report${reportType}-form`;
    const form = document.getElementById(formId);
    const previewId = `preview-content-${reportType}`;
    const preview = document.getElementById(previewId);
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

    if (!form || !preview || !csrfToken) {
        console.error('Не найдены необходимые элементы формы или CSRF-токен');
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка: Форма или CSRF-токен не найдены</p>
                <button onclick="generateReport(${reportType})">Повторить</button>
            </div>
        `;
        return;
    }

    const formData = new FormData(form);
    formData.append('preview', 'true');

    try {
        // Блокируем кнопку для предотвращения повторных запросов
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) submitButton.disabled = true;

        preview.innerHTML = '<p class="loading">Генерация предпросмотра...</p>';

        const previewResponse = await fetch(`/reports/generate_report_${reportType}`, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken
            },
            body: formData,
            signal: AbortSignal.timeout(10000) // Тайм-аут 10 секунд
        });

        const previewData = await previewResponse.json();

        if (!previewResponse.ok || previewData.error) {
            throw new Error(previewData.error || `Ошибка HTTP: ${previewResponse.status}`);
        }

        // Экранирование данных для предотвращения XSS
        const escapeHtml = (str) => {
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        };

        preview.innerHTML = `
        <div class="report-preview">
            <h4>Предпросмотр отчета</h4>
            ${reportType === 1 ? `
                <p><strong>Донор:</strong> ${escapeHtml(previewData.donor_name)}</p>
                <p><strong>Учреждение:</strong> ${escapeHtml(previewData.institution)}</p>
                <p><strong>Дата сдачи крови:</strong> ${escapeHtml(previewData.collection_date)}</p>
                <p><strong>Объем крови:</strong> ${escapeHtml(previewData.blood_volume)} мл</p>
            ` : `
                <p><strong>Учреждение:</strong> ${escapeHtml(previewData.institution)}</p>
                <p><strong>Период:</strong> ${escapeHtml(previewData.period)}</p>
                <p><strong>Количество доноров:</strong> ${escapeHtml(String(previewData.total_donors))}</p>
            `}
            <button onclick="downloadFullReport(${reportType})">Скачать полный отчет</button>
        </div>
    `;

    } catch (error) {
        console.error('Ошибка:', error);
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка при генерации отчета: ${escapeHtml(error.message)}</p>
                <button onclick="generateReport(${reportType})">Повторить</button>
            </div>
        `;
    } finally {
        // Разблокируем кнопку
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) submitButton.disabled = false;
    }
}

async function downloadFullReport(reportType) {
    const formId = `report${reportType}-form`;
    const form = document.getElementById(formId);
    const previewId = `preview-content-${reportType}`;
    const preview = document.getElementById(previewId);
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

    if (!form || !preview || !csrfToken) {
        console.error('Не найдены необходимые элементы формы или CSRF-токен');
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка: Форма или CSRF-токен не найдены</p>
                <button onclick="downloadFullReport(${reportType})">Повторить</button>
            </div>
        `;
        return;
    }

    const formData = new FormData(form);
    formData.delete('preview');

    try {
        // Блокируем кнопку для предотвращения повторных запросов
        const downloadButton = preview.querySelector('button');
        if (downloadButton) downloadButton.disabled = true;

        preview.innerHTML = '<p class="loading">Подготовка файла для скачивания...</p>';

        const response = await fetch(`/reports/generate_report_${reportType}`, {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken
            },
            body: formData,
            signal: AbortSignal.timeout(10000) // Тайм-аут 10 секунд
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `Ошибка HTTP: ${response.status}`);
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

        // Освобождение URL
        URL.revokeObjectURL(url);

        // Обновляем предпросмотр
        preview.innerHTML = `
            <div class="report-success">
                <p>Файл успешно скачан!</p>
                <button onclick="generateReport(${reportType})">Сгенерировать новый отчет</button>
            </div>
        `;

    } catch (error) {
        console.error('Ошибка:', error);
        preview.innerHTML = `
            <div class="report-preview-error">
                <p>Ошибка при скачивании отчета: ${escapeHtml(error.message)}</p>
                <button onclick="downloadFullReport(${reportType})">Повторить</button>
            </div>
        `;
    } finally {
        // Разблокируем кнопку
        const downloadButton = preview.querySelector('button');
        if (downloadButton) downloadButton.disabled = false;
    }
}

// Вспомогательная функция для экранирования HTML
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}